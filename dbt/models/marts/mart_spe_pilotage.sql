-- Pilotage de la campagne de télédéclaration pour les RSPE (tableau de bord Metabase).
-- Une ligne par restaurant du périmètre État et par année de données, Armées incluses
-- (est_armees sépare le tableau commun du tableau Armées). n-1 = la ligne de l'année précédente.
-- Restaurant, tutelle et gestionnaires : état du jour (mart_cantines), pas celui figé dans la TD.
-- Les chiffres diffèrent donc du bilan SPE (mart_spe_bilan, figé au 29/04 n+1).
-- Indicateurs de la mesure 10 : repris de mart_teledeclarations, vides sans TD retenue.
-- Cibles absentes : les questions Metabase les lisent dans la table téléversée par la DGAL
-- (modèle 3737), pour qu'une correction apparaisse tout de suite. Le calendrier téléversé
-- (modèle 3738) sert au jour de campagne.
-- Adresses des gestionnaires : sans les comptes de l'équipe ma cantine (is_staff ou is_dev).

with perimetre as (
    select * from {{ ref('int_spe_perimetre') }}
),

cantines as (
    select * from {{ ref('mart_cantines') }}
),

statuts as (
    select * from {{ ref('int_campagne_statut') }}
),

teledeclarations as (
    select * from {{ ref('mart_teledeclarations') }}
),

-- Gestionnaires par cantine, sans les comptes de l'équipe ma cantine : rattachés à de
-- nombreux restaurants pour l'accompagnement, ils ne sont pas à relancer
gestionnaires as (
    select
        m.canteen_id,
        string_agg(u.email, ', ' order by u.email)         as adresses
    from {{ ref('stg_canteen_managers') }} as m
    inner join {{ ref('stg_users') }} as u on m.user_id = u.user_id
    where
        not coalesce(u.is_staff, false)
        and not coalesce(u.is_dev, false)
    group by m.canteen_id
),

campagnes as (
    select * from {{ ref('stg_spe_campagnes') }}
),

-- date du run de nuit, à l'heure de Paris
aujourdhui as (
    select (now() at time zone 'Europe/Paris')::date       as jour
)

select
    -- restaurant
    c.id                                                        as canteen_id,
    c.siret,
    c.nom,
    c.groupe_id,
    g.nom                                                       as groupe_nom,
    c.type_production,
    c.type_gestion,
    {{ libelle_type_production('c.type_production') }}          as type_production_lib,
    {{ libelle_type_gestion('c.type_gestion') }}                as type_gestion_lib,
    c.nbre_repas_jour,
    c.nbre_repas_an,
    c.date_creation::date                                       as date_inscription,  -- UTC

    -- périmètre
    p.perimetre_key,
    p.perimetre_lib,
    p.pole_ministeriel,
    p.ordre_affichage,
    p.est_armees,

    -- secteur : les libellés ne contiennent pas de virgule (macro libelles_secteurs)
    c.secteurs,
    case when c.secteurs like '%,%' then 'Secteurs multiples' else c.secteurs end
                                                                as secteur,

    -- géographie
    c.code_insee_commune,
    c.libelle_commune,
    c.departement,
    c.departement_lib,
    c.region,
    c.region_lib,

    -- gestionnaires hors équipe ma cantine ; relance d'un satellite : les gestionnaires de son
    -- groupe, sinon les siens
    gc.adresses                                                 as adresses_gestionnaires,
    coalesce(gg.adresses, gc.adresses)                          as adresses_relance,

    -- statut de l'année
    s.annee,
    s.statut_td,
    s.teledeclaration_id,
    s.date_teledeclaration,
    s.date_debut_saisie,
    s.date_modification_saisie,
    s.td_complete,
    s.td_generee_par_groupe,
    s.en_cours_via_groupe,
    s.td_deposee_non_retenue,

    -- jour de campagne : 1 = jour d'ouverture (calendrier de la DGAL) ; vide sans calendrier
    s.date_teledeclaration - cal.date_ouverture + 1             as jour_campagne_teledeclaration,
    (select jour from aujourdhui) - cal.date_ouverture + 1      as jour_campagne_aujourdhui,
    -- le restaurant avait-il télédéclaré l'année précédente à ce même jour de campagne ?
    case
        when cal.date_ouverture is null or cal_n1.date_ouverture is null then null
        else coalesce(
            s1.date_teledeclaration - cal_n1.date_ouverture + 1
            <= (select jour from aujourdhui) - cal.date_ouverture + 1,
            false
        )
    end                                                         as teledeclare_n1_au_meme_jour,

    -- mesure 10 : valeurs à réagréger (somme / somme dans Metabase)
    t.valeur_totale,
    t.valeur_bio_agg,
    t.valeur_egalim_agg,
    t.valeur_viandes_et_poissons,
    t.valeur_viandes_et_poissons_egalim,

    -- objectifs, seuils selon la zone (même règle que les atteint_* de mart_teledeclarations)
    t.atteint_bio,
    t.atteint_egalim,
    t.atteint_viandes_et_poissons_egalim,
    case
        when t.teledeclaration_id is null           then null
        when t.cantine_departement = '976'          then 'Mayotte : 5 % dont 2 % de bio'
        when t.cantine_objectif_zone_geo = 'droms'  then 'DROM : 20 % dont 5 % de bio'
        else                                             'Métropole : 50 % dont 20 % de bio'
    end                                                         as seuil_applicable,

    -- végétarien, diversification
    t.choix_multiple,
    t.atteint_vege_quotidien,
    t.td_volet_diversification_complet,

    -- gaspillage (filtre 10 à 500 g par couvert déjà appliqué dans mart_teledeclarations)
    t.gaspi_total_mass_kg,
    t.gaspi_meal_count,
    t.gaspi_g_par_couvert,
    -- niveau ADEME sur le ratio non arrondi, comme int_spe_waste_by_canteen
    case
        when coalesce(t.gaspi_meal_count, 0) = 0                            then null
        when t.gaspi_total_mass_kg * 1000 / t.gaspi_meal_count <= 47        then 'Niveau 3'
        when t.gaspi_total_mass_kg * 1000 / t.gaspi_meal_count <= 74        then 'Niveau 2'
        when t.gaspi_total_mass_kg * 1000 / t.gaspi_meal_count <= 95        then 'Niveau 1'
        else                                                                     'Non atteint'
    end                                                         as niveau_ademe

from perimetre as p
inner join cantines as c on p.canteen_id = c.id
left join cantines as g on c.groupe_id = g.id
inner join statuts as s on p.canteen_id = s.canteen_id
-- teledeclaration_id n'est pas unique (satellites déclarés par un groupe) : jointure sur la cantine aussi
left join teledeclarations as t
    on s.canteen_id = t.canteen_id and s.teledeclaration_id = t.teledeclaration_id
left join gestionnaires as gc on c.id = gc.canteen_id
left join gestionnaires as gg on c.groupe_id = gg.canteen_id
left join campagnes as cal on s.annee = cal.annee
left join campagnes as cal_n1 on s.annee - 1 = cal_n1.annee
-- statut de l'année précédente, pour la comparaison au même jour de campagne
left join statuts as s1 on s.canteen_id = s1.canteen_id and s.annee - 1 = s1.annee
