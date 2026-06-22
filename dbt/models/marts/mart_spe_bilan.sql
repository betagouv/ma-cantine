{{ config(materialized='table') }}

-- Tableau bilan SPE : 1 ligne par (annee, perimetre)
-- Inclut les périmètres line_ministry ET les sous-totaux groupe (UNION ALL)
-- sort_order suit la nomenclature officielle Vue 1 (22 lignes)
-- /!\ les libellés périmètres inconnus sont à vérifier (affaires_etrangeres, armees, etc.)

with overrides_spe as (
    select * from (values
        ('19691861900012', 'economie', false),
        ('19572647600011', 'economie', false),
        ('21400312100172', null,       true),
        ('26760171400087', null,       true)
    ) as t(siret, line_ministry_force, exclure)
),

-- Cantines SPE avec overrides appliqués (reclassements + exclusions)
canteens_spe as (
    select
        coalesce(o.line_ministry_force, c.line_ministry)    as line_ministry,
        c.creation_date
    from {{ ref('stg_canteens') }} c
    left join overrides_spe o on o.siret = c.siret
    where c.line_ministry is not null
      and c.line_ministry != ''
      and coalesce(o.exclure, false) = false
),

spe_years as (
    select distinct year as annee
    from {{ ref('stg_teledeclarations') }}
    where line_ministry is not null and line_ministry != ''
),

inscriptions_by_ministry as (
    select
        c.line_ministry                                      as perimetre,
        'line_ministry'                                      as type_perimetre,
        y.annee,
        count(*)                                             as nb_inscrites
    from canteens_spe c
    cross join spe_years y
    where c.creation_date <= make_date(y.annee::int + 1, 4, 29)
    group by c.line_ministry, y.annee
),

inscriptions_by_groupe as (
    select
        case
            when perimetre in ('ecologie', 'mer')                             then 'MTE'
            when perimetre in ('jeunesse', 'enseignement_superieur', 'sport') then 'MEJSESR'
            when perimetre in ('justice_hors_pjj', 'justice_pjj')             then 'Justice'
            when perimetre in ('travail', 'sante')                            then 'Ministères sociaux'
            when perimetre in ('interieur', 'administration_territoriale')    then 'Périmètre intérieur'
        end                                                                    as perimetre,
        'groupe'                                                               as type_perimetre,
        annee,
        sum(nb_inscrites)                                                      as nb_inscrites
    from inscriptions_by_ministry
    where perimetre in (
        'ecologie', 'mer',
        'jeunesse', 'enseignement_superieur', 'sport',
        'justice_hors_pjj', 'justice_pjj',
        'travail', 'sante',
        'interieur', 'administration_territoriale'
    )
    group by 1, annee
),

inscriptions as (
    select perimetre, type_perimetre, annee, nb_inscrites from inscriptions_by_ministry
    union all
    select perimetre, type_perimetre, annee, nb_inscrites from inscriptions_by_groupe
    union all
    select 'TOTAL', 'total', annee, sum(nb_inscrites)
    from inscriptions_by_ministry
    group by annee
),

waste as (
    select annee, perimetre_key, nb_canteens_avec_mesure, total_mass_kg, total_meal_count,
           nb_niveau_3, nb_niveau_2, nb_niveau_1, nb_non_atteint, gaspi_g_par_couvert
    from {{ ref('int_spe_waste') }}
    union all
    select
        annee,
        'TOTAL'                                                                         as perimetre_key,
        sum(nb_canteens_avec_mesure)                                                    as nb_canteens_avec_mesure,
        sum(total_mass_kg)                                                              as total_mass_kg,
        sum(total_meal_count)                                                           as total_meal_count,
        sum(nb_niveau_3)                                                                as nb_niveau_3,
        sum(nb_niveau_2)                                                                as nb_niveau_2,
        sum(nb_niveau_1)                                                                as nb_niveau_1,
        sum(nb_non_atteint)                                                             as nb_non_atteint,
        round((sum(total_mass_kg) * 1000 / nullif(sum(total_meal_count), 0))::numeric, 1) as gaspi_g_par_couvert
    from {{ ref('int_spe_waste') }}
    where perimetre_key not in ('MTE', 'MEJSESR', 'Justice', 'Ministères sociaux', 'Périmètre intérieur')
    group by annee
),

-- Référentiel périmètres : sort_order, clé DB, libellé affiché, groupe, est_total_groupe
-- La clé DB doit correspondre exactement aux valeurs de cantine_line_ministry / cantine_groupe_spe
ref_perimetre as (
    select *
    from (values
        (1,  'mer',                         'Mer',                                         'MTE',                false),
        (2,  'ecologie',                    'Environnement',                               'MTE',                false),
        (3,  'MTE',                         'TOTAL MTE',                                   'MTE',                true),
        (4,  'affaires_etrangeres',         'Affaires étrangères',                         null,                 false),
        (5,  'armee',                       'Armées',                                      null,                 false),
        (6,  'autorites_independantes',     'AAI',                                         null,                 false),
        (7,  'culture',                     'Culture',                                     null,                 false),
        (8,  'economie',                    'Économie et finances',                        null,                 false),
        (9,  'transformation',              'Fonction Publique',                           null,                 false),
        (10, 'jeunesse',                    'Éducation nationale',                         'MEJSESR',            false),
        (11, 'enseignement_superieur',      'Enseignement supérieur et recherche',         'MEJSESR',            false),
        (12, 'sport',                       'Sports',                                      'MEJSESR',            false),
        (13, 'MEJSESR',                     'TOTAL MEJSESR',                               'MEJSESR',            true),
        (14, 'justice_hors_pjj',            'Justice hors PJJ',                            'Justice',            false),
        (15, 'justice_pjj',                 'Justice PJJ',                                 'Justice',            false),
        (16, 'Justice',                     'TOTAL Justice',                               'Justice',            true),
        (17, 'interieur',                   'Intérieur',                                   'Périmètre intérieur',    false),
        (18, 'administration_territoriale', 'Administration territoriale de l''État (ATE)', 'Périmètre intérieur',  false),
        (19, 'Périmètre intérieur',         'TOTAL Périmètre intérieur',                   'Périmètre intérieur',   true),
        (20, 'premier_ministre',            'Premier ministre',                            null,                 false),
        (21, 'agriculture',                 'Agriculture',                                 null,                 false),
        (22, 'travail',                     'Travail',                                     'Ministères sociaux', false),
        (23, 'sante',                       'Santé',                                       'Ministères sociaux', false),
        (24, 'Ministères sociaux',          'TOTAL Ministères sociaux',                    'Ministères sociaux', true),
        (25, 'TOTAL',                       'TOTAL GÉNÉRAL',                               null,                 true)
    ) as t(sort_order, perimetre_key, perimetre_lib, groupe_spe, est_total_groupe)
),

ref_perimetre_with_groupe as (
    select
        sort_order,
        perimetre_key,
        perimetre_lib,
        groupe_spe,
        est_total_groupe,
        coalesce(groupe_spe, perimetre_lib) as groupe_lib
    from ref_perimetre
),

ref_cibles as (
    select * from (values
        ('ecologie',                      57,   'Cible ferme'),
        ('mer',                            5,   'Cible ferme'),
        ('affaires_etrangeres',            3,   'Cible ferme'),
        ('armee',                        244,   'Cible ferme'),
        ('autorites_independantes',      null,  'Non renseignée'),
        ('culture',                       18,   'Cible ferme'),
        ('economie',                     169,   'Cible ferme'),
        ('jeunesse',                      20,   'Cible ferme'),
        ('enseignement_superieur',       439,   'Précision en cours'),
        ('sport',                         22,   'Cible ferme'),
        ('justice_hors_pjj',             290,   'Cible ferme'),
        ('justice_pjj',                   92,   'Cible ferme'),
        ('interieur',                    207,   'Précision en cours'),
        ('administration_territoriale',   107,   'Précision en cours'),
        ('premier_ministre',               5,   'Cible ferme'),
        ('agriculture',                   10,   'Cible ferme'),
        ('travail',                      116,   'Précision en cours'),
        ('sante',                        23,    'Précision en cours'),
        ('transformation',               null,  'Non renseignée')
    ) as t(perimetre_key, cible_etablissements, fiabilite_cible)
),

-- Cibles dynamiques pour les sous-totaux groupe ET le TOTAL GÉNÉRAL
-- = sum(coalesce(cible_officielle, nb_inscrites)) des line_ministry composants
cible_groupes as (
    -- Sous-totaux groupe : agréger uniquement les ministères appartenant au groupe
    select
        r.groupe_spe                                                           as perimetre_key,
        i.annee,
        sum(coalesce(c.cible_etablissements, i.nb_inscrites))                  as cible_etablissements
    from inscriptions_by_ministry i
    left join ref_cibles c on c.perimetre_key = i.perimetre
    join ref_perimetre_with_groupe r on r.perimetre_key = i.perimetre
    where r.est_total_groupe = false
      and r.groupe_spe is not null
    group by r.groupe_spe, i.annee

    union all

    -- TOTAL GÉNÉRAL : tous les line_ministry
    select
        'TOTAL'                                                                as perimetre_key,
        i.annee,
        sum(coalesce(c.cible_etablissements, i.nb_inscrites))                  as cible_etablissements
    from inscriptions_by_ministry i
    left join ref_cibles c on c.perimetre_key = i.perimetre
    group by i.annee
),

-- Agrégations par line_ministry
stats as (
    select
        annee,
        coalesce(o.line_ministry_force, cantine_line_ministry)                      as perimetre_key,
        count(*)                                                                    as nb_td,
        sum(valeur_totale)                                                          as valeur_totale,
        sum(valeur_bio_agg)                                                         as valeur_bio_agg,
        sum(valeur_egalim_agg)                                                      as valeur_egalim_agg,
        sum(valeur_viandes_volailles)                                               as vv,
        sum(valeur_viandes_volailles_egalim)                                        as vv_egalim,
        sum(valeur_produits_de_la_mer)                                              as pdm,
        sum(valeur_produits_de_la_mer_egalim)                                       as pdm_egalim,
        sum(total_origine_france)                                                   as total_france,
        sum(valeur_viandes_volailles_france)                                        as vv_france,
        sum(atteint_bio::int)                                                       as nb_bio,
        sum(atteint_egalim::int)                                                    as nb_egalim,
        sum(atteint_bio_et_egalim::int)                                             as nb_bio_et_egalim,
        sum(atteint_viandes_et_poissons_egalim::int)                                as nb_vp_egalim,
        sum(atteint_3_objectifs::int)                                               as nb_3_obj,
        -- #15 représentativité V&P : TD avec viandes ET poissons EGalim renseignés
        sum(case when valeur_viandes_volailles_egalim > 0
                  and valeur_produits_de_la_mer_egalim > 0
                 then 1 else 0 end)                                                 as nb_td_vp_renseignes,
        -- #16 représentativité EGalim : TD avec volet EGalim renseigné
        sum(case when valeur_egalim_agg is not null then 1 else 0 end)                     as nb_td_egalim_renseignes,
        -- végétarien : dénominateur = cantines avec choix multiple
        sum(choix_multiple::int)                                                            as nb_choix_multiple,
        sum(atteint_vege_quotidien::int)                                                    as nb_vege_quotidien,
        -- diversification : dénominateur = nb_inscrites
        sum(td_volet_diversification_complet::int)                                          as nb_td_diversification_complet
    from {{ ref('mart_teledeclarations') }}
    left join overrides_spe o on o.siret = cantine_siret
    where cantine_line_ministry is not null
      and (cantine_secteur != 'administration_etablissement_public' or cantine_line_ministry != 'administration_territoriale')
      and coalesce(o.exclure, false) = false
    group by annee, coalesce(o.line_ministry_force, cantine_line_ministry)
),

-- Sous-totaux par groupe (somme des line_ministry appartenant au groupe)
stats_groupe as (
    select
        s.annee,
        r.groupe_spe                                                                as perimetre_key,
        sum(s.nb_td)                                                                as nb_td,
        sum(s.valeur_totale)                                                        as valeur_totale,
        sum(s.valeur_bio_agg)                                                       as valeur_bio_agg,
        sum(s.valeur_egalim_agg)                                                    as valeur_egalim_agg,
        sum(s.vv)                                                                   as vv,
        sum(s.vv_egalim)                                                            as vv_egalim,
        sum(s.pdm)                                                                  as pdm,
        sum(s.pdm_egalim)                                                           as pdm_egalim,
        sum(s.total_france)                                                         as total_france,
        sum(s.vv_france)                                                            as vv_france,
        sum(s.nb_bio)                                                               as nb_bio,
        sum(s.nb_egalim)                                                            as nb_egalim,
        sum(s.nb_bio_et_egalim)                                                     as nb_bio_et_egalim,
        sum(s.nb_vp_egalim)                                                         as nb_vp_egalim,
        sum(s.nb_3_obj)                                                             as nb_3_obj,
        sum(s.nb_td_vp_renseignes)                                                  as nb_td_vp_renseignes,
        sum(s.nb_td_egalim_renseignes)                                              as nb_td_egalim_renseignes,
        sum(s.nb_choix_multiple)                                                    as nb_choix_multiple,
        sum(s.nb_vege_quotidien)                                                    as nb_vege_quotidien,
        sum(s.nb_td_diversification_complet)                                        as nb_td_diversification_complet
    from stats s
    join ref_perimetre_with_groupe r on r.perimetre_key = s.perimetre_key
    where r.groupe_spe is not null
      and r.est_total_groupe = false
    group by s.annee, r.groupe_spe
),

-- Total global : somme des line_ministry uniquement (pas de double compte avec stats_groupe)
stats_total as (
    select
        annee,
        'TOTAL'                                      as perimetre_key,
        sum(nb_td)                                   as nb_td,
        sum(valeur_totale)                           as valeur_totale,
        sum(valeur_bio_agg)                          as valeur_bio_agg,
        sum(valeur_egalim_agg)                       as valeur_egalim_agg,
        sum(vv)                                      as vv,
        sum(vv_egalim)                               as vv_egalim,
        sum(pdm)                                     as pdm,
        sum(pdm_egalim)                              as pdm_egalim,
        sum(total_france)                            as total_france,
        sum(vv_france)                               as vv_france,
        sum(nb_bio)                                  as nb_bio,
        sum(nb_egalim)                               as nb_egalim,
        sum(nb_bio_et_egalim)                        as nb_bio_et_egalim,
        sum(nb_vp_egalim)                            as nb_vp_egalim,
        sum(nb_3_obj)                                as nb_3_obj,
        sum(nb_td_vp_renseignes)                     as nb_td_vp_renseignes,
        sum(nb_td_egalim_renseignes)                 as nb_td_egalim_renseignes,
        sum(nb_choix_multiple)                       as nb_choix_multiple,
        sum(nb_vege_quotidien)                       as nb_vege_quotidien,
        sum(nb_td_diversification_complet)           as nb_td_diversification_complet
    from stats s
    join ref_perimetre_with_groupe r on r.perimetre_key = s.perimetre_key
    where r.est_total_groupe = false
    group by s.annee
),

all_stats as (
    select * from stats
    union all
    select * from stats_groupe
    union all
    select * from stats_total
)

select
    r.sort_order,
    r.perimetre_key,
    r.perimetre_lib,
    r.groupe_spe,
    r.groupe_lib,
    r.est_total_groupe,
    s.annee,

    -- dénominateur
    coalesce(i.nb_inscrites, 0)                                                     as nb_inscrites,

    -- #1 / #2 : taux TD (nb TD / cible ou nb inscrits au 29 avril n+1)
    s.nb_td                                                                         as nb_teledeclarations,
    round((100.0 * s.nb_td / nullif(coalesce(c.cible_etablissements, i.nb_inscrites), 0))::numeric, 1) as taux_td_pct,

    -- #4 part EGalim (bio inclus)
    round((100.0 * s.valeur_egalim_agg / nullif(s.valeur_totale, 0))::numeric, 1)  as part_egalim_pct,

    -- #5 part bio
    round((100.0 * s.valeur_bio_agg / nullif(s.valeur_totale, 0))::numeric, 1)     as part_bio_pct,

    -- #6 part origine France
    round((100.0 * s.total_france / nullif(s.valeur_totale, 0))::numeric, 1)       as part_france_pct,

    -- #7 part V+P EGalim (viandes/volailles + pêche cumulés)
    round((100.0 * (s.vv_egalim + s.pdm_egalim) / nullif(s.vv + s.pdm, 0))::numeric, 1) as part_vp_egalim_pct,

    -- #8 part viandes/volailles EGalim uniquement
    round((100.0 * s.vv_egalim / nullif(s.vv, 0))::numeric, 1)                     as part_vv_egalim_pct,

    -- #9 part viandes/volailles origine France
    round((100.0 * s.vv_france / nullif(s.vv, 0))::numeric, 1)                     as part_vv_france_pct,

    -- #3 objectifs par cantine (% sur cible ou nb inscrits)
    s.nb_bio                                                                        as nb_cantines_atteint_bio,
    round((100.0 * s.nb_bio         / nullif(coalesce(c.cible_etablissements, i.nb_inscrites), 0))::numeric, 1) as taux_atteint_bio_pct,
    s.nb_egalim                                                                     as nb_cantines_atteint_egalim,
    round((100.0 * s.nb_egalim      / nullif(coalesce(c.cible_etablissements, i.nb_inscrites), 0))::numeric, 1) as taux_atteint_egalim_pct,
    s.nb_bio_et_egalim                                                              as nb_cantines_atteint_bio_et_egalim,
    round((100.0 * s.nb_bio_et_egalim / nullif(coalesce(c.cible_etablissements, i.nb_inscrites), 0))::numeric, 1) as taux_atteint_bio_et_egalim_pct,
    s.nb_vp_egalim                                                                  as nb_cantines_atteint_vp_egalim,
    round((100.0 * s.nb_vp_egalim   / nullif(coalesce(c.cible_etablissements, i.nb_inscrites), 0))::numeric, 1) as taux_atteint_vp_egalim_pct,
    s.nb_3_obj                                                                      as nb_cantines_atteint_3_objectifs,
    round((100.0 * s.nb_3_obj       / nullif(coalesce(c.cible_etablissements, i.nb_inscrites), 0))::numeric, 1) as taux_atteint_3_objectifs_pct,

    -- #15 représentativité V&P renseignés
    s.nb_td_vp_renseignes                                                           as nb_td_vp_renseignes,
    round((100.0 * s.nb_td_vp_renseignes / nullif(coalesce(c.cible_etablissements, i.nb_inscrites), 0))::numeric, 1) as taux_td_vp_renseignes_pct,

    -- #16 représentativité EGalim renseigné
    s.nb_td_egalim_renseignes                                                       as nb_td_egalim_renseignes,
    round((100.0 * s.nb_td_egalim_renseignes / nullif(coalesce(c.cible_etablissements, i.nb_inscrites), 0))::numeric, 1) as taux_td_egalim_renseignes_pct,

    -- végétarien : offre quotidienne parmi les cantines à choix multiple
    s.nb_choix_multiple                                                             as nb_cantines_choix_multiple,
    s.nb_vege_quotidien                                                             as nb_cantines_vege_quotidien,
    round((100.0 * s.nb_vege_quotidien / nullif(s.nb_choix_multiple, 0))::numeric, 1) as taux_vege_quotidien_pct,

    -- diversification : volet complet / cible ou nb inscrits
    s.nb_td_diversification_complet                                                 as nb_td_diversification_complet,
    round((100.0 * s.nb_td_diversification_complet / nullif(coalesce(c.cible_etablissements, i.nb_inscrites), 0))::numeric, 1) as taux_td_diversification_complet_pct,

    -- gaspillage alimentaire
    w.nb_canteens_avec_mesure                                                       as nb_canteens_mesure_gaspi,
    round((100.0 * w.nb_canteens_avec_mesure / nullif(coalesce(c.cible_etablissements, i.nb_inscrites), 0))::numeric, 1) as taux_representativite_gaspi_pct,
    w.gaspi_g_par_couvert,
    w.nb_niveau_3                                                                   as nb_cantines_niveau_3_ademe,
    w.nb_niveau_2                                                                   as nb_cantines_niveau_2_ademe,
    w.nb_niveau_1                                                                   as nb_cantines_niveau_1_ademe,
    w.nb_non_atteint                                                                as nb_cantines_non_atteint_ademe,

    -- cible établissements : valeur officielle pour les line_ministry,
    -- dynamique (sum des composants) pour les groupes et TOTAL GÉNÉRAL
    case
        when r.est_total_groupe
            then cg.cible_etablissements
        else coalesce(c.cible_etablissements, i.nb_inscrites)
    end                                                                              as cible_etablissements,
    case
        when r.est_total_groupe                then null
        when c.cible_etablissements is null    then 'Non renseignée'
        else c.fiabilite_cible
    end                                                                              as fiabilite_cible,
    case
        when c.fiabilite_cible = 'Cible ferme' then 'Dernière Bilatérale'
        else null
    end                                                                              as source_cible,

    -- taux d'inscription : null si pas de cible officielle
    round((100.0 * i.nb_inscrites / nullif(c.cible_etablissements, 0))::numeric, 1) as taux_inscription_pct

from all_stats s
join ref_perimetre_with_groupe r on r.perimetre_key = s.perimetre_key
left join inscriptions i
    on i.perimetre = r.perimetre_key
    and i.annee    = s.annee
left join waste w
    on w.perimetre_key = r.perimetre_key
    and w.annee        = s.annee
left join ref_cibles c
    on c.perimetre_key = r.perimetre_key
left join cible_groupes cg
    on cg.perimetre_key = r.perimetre_key
    and cg.annee        = s.annee
order by s.annee, r.sort_order
