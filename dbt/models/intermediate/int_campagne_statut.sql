-- Statut de télédéclaration de chaque cantine active, pour chaque année de données.
-- Une ligne par (canteen_id, annee), toutes cantines : sert au pilotage SPE et servira au
-- pilotage général de la campagne.
-- Années : toutes celles des diagnostics, aucune écrite en dur ; une nouvelle année apparaît
-- dès son premier brouillon. Population : cantines actives aujourd'hui, pour toutes les années.
-- Statut, dans cet ordre :
--   Télédéclaré : TD retenue dans mart_teledeclarations (mêmes règles que l'observatoire ; couvre
--                 les satellites dont la TD a été générée par leur groupe ou leur cuisine centrale) ;
--   En cours    : diagnostic de l'année en brouillon ou rouvert en correction, sur la cantine ou
--                 sur son groupe ;
--   À relancer  : sinon.
-- Les dates permettent de recalculer le statut à une date passée dans Metabase (filtre « État au »).

with cantines as (
    select
        id                                          as canteen_id,
        groupe_id
    from {{ ref('mart_cantines') }}
),

annees as (
    select distinct year                            as annee
    from {{ ref('stg_diagnostics') }}
),

teledeclarations as (
    -- une TD retenue par cantine et par année (1 TD = 1 site) ; distinct on pour garantir le grain
    select distinct on (canteen_id, annee)
        canteen_id,
        annee,
        teledeclaration_id,
        date_teledeclaration,
        teledeclaration_mode,
        cantine_is_filled,
        cantine_generated_from_groupe_diagnostic
    from {{ ref('mart_teledeclarations') }}
    order by canteen_id, annee, date_teledeclaration
),

diagnostics as (
    select
        canteen_id,
        year                                                                        as annee,
        bool_or(status in ('DRAFT', 'CORRECTION'))                                  as a_saisie_en_cours,
        bool_or(status = 'SUBMITTED')                                               as a_td_deposee,
        min(creation_date)                                                          as date_premier_diagnostic,
        max(modification_date) filter (where status in ('DRAFT', 'CORRECTION'))    as date_modification_saisie
    from {{ ref('stg_diagnostics') }}
    group by canteen_id, year
)

select
    c.canteen_id,
    a.annee,
    case
        when t.canteen_id is not null                       then 'Télédéclaré'
        when coalesce(dc.a_saisie_en_cours, false)
            or coalesce(dg.a_saisie_en_cours, false)        then 'En cours'
        else                                                     'À relancer'
    end                                                                         as statut_td,
    t.teledeclaration_id,
    (t.date_teledeclaration at time zone 'Europe/Paris')::date                  as date_teledeclaration,
    t.teledeclaration_mode,
    t.cantine_is_filled                                                         as td_complete,
    coalesce(t.cantine_generated_from_groupe_diagnostic, false)                 as td_generee_par_groupe,
    t.canteen_id is null
    and not coalesce(dc.a_saisie_en_cours, false)
    and coalesce(dg.a_saisie_en_cours, false)                                   as en_cours_via_groupe,
    -- TD déposée mais écartée de mart_teledeclarations (valeurs aberrantes, valeur totale vide…)
    t.canteen_id is null and coalesce(dc.a_td_deposee, false)                   as td_deposee_non_retenue,
    -- least / greatest ignorent les null : cantine ou groupe, le premier connu
    (
        least(dc.date_premier_diagnostic, dg.date_premier_diagnostic)
        at time zone 'Europe/Paris'
    )::date                                                                     as date_debut_saisie,
    (
        greatest(dc.date_modification_saisie, dg.date_modification_saisie)
        at time zone 'Europe/Paris'
    )::date                                                                     as date_modification_saisie
from cantines as c
cross join annees as a
left join teledeclarations as t
    on c.canteen_id = t.canteen_id and a.annee = t.annee
left join diagnostics as dc
    on c.canteen_id = dc.canteen_id and a.annee = dc.annee
left join diagnostics as dg
    on c.groupe_id = dg.canteen_id and a.annee = dg.annee
