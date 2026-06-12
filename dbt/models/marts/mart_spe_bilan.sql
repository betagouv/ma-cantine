{{ config(materialized='table') }}

-- Tableau bilan SPE : 1 ligne par (annee, perimetre)
-- Inclut les périmètres line_ministry ET les sous-totaux groupe (UNION ALL)
-- sort_order suit la nomenclature officielle Vue 1 (22 lignes)
-- /!\ les libellés périmètres inconnus sont à vérifier (affaires_etrangeres, armees, etc.)

with inscriptions as (
    select * from {{ ref('int_spe_inscriptions') }}
),

waste as (
    select * from {{ ref('int_spe_waste') }}
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
        (8,  'economie',                    'Économie et finances',                        'MACP',               false),
        (9,  'transformation',              'Fonction Publique',                           'MACP',               false),
        (10, 'MACP',                        'TOTAL MACP',                                  'MACP',               true),
        (11, 'jeunesse',                    'Éducation nationale',                         'MEJSESR',            false),
        (12, 'enseignement_superieur',      'Enseignement supérieur et recherche',         'MEJSESR',            false),
        (13, 'sport',                       'Sports',                                      'MEJSESR',            false),
        (14, 'MEJSESR',                     'TOTAL MEJSESR',                               'MEJSESR',            true),
        (15, 'justice_hors_pjj',            'Justice hors PJJ',                            'Justice',            false),
        (16, 'justice_pjj',                 'Justice PJJ',                                 'Justice',            false),
        (17, 'Justice',                     'TOTAL Justice',                               'Justice',            true),
        (18, 'interieur',                   'Intérieur',                                   'Intérieur + ATE',    false),
        (19, 'administration_territoriale', 'Administration territoriale de l''État (ATE)', 'Intérieur + ATE',  false),
        (20, 'Intérieur + ATE',             'TOTAL Intérieur + ATE',                       'Intérieur + ATE',   true),
        (21, 'premier_ministre',            'Premier ministre',                            null,                 false),
        (22, 'agriculture',                 'Agriculture',                                 null,                 false),
        (23, 'travail',                     'Travail',                                     'Ministères sociaux', false),
        (24, 'sante',                       'Santé',                                       'Ministères sociaux', false),
        (25, 'Ministères sociaux',          'TOTAL Ministères sociaux',                    'Ministères sociaux', true)
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
        ('MTE',                           62,   'Cible ferme'),
        ('affaires_etrangeres',            3,   'Cible ferme'),
        ('armee',                        244,   'Cible ferme'),
        ('autorites_independantes',      null,  'Non renseignée'),
        ('culture',                       18,   'Cible ferme'),
        ('economie',                     169,   'Cible ferme'),
        ('MACP',                         169,   'Précision en cours'),
        ('jeunesse',                      20,   'Cible ferme'),
        ('enseignement_superieur',       439,   'Précision en cours'),
        ('sport',                         22,   'Cible ferme'),
        ('MEJSESR',                      481,   'Précision en cours'),
        ('justice_hors_pjj',             290,   'Cible ferme'),
        ('justice_pjj',                   92,   'Cible ferme'),
        ('Justice',                      382,   'Cible ferme'),
        ('interieur',                    207,   'Précision en cours'),
        ('administration_territoriale',   96,   'Précision en cours'),
        ('Intérieur + ATE',              303,   'Précision en cours'),
        ('premier_ministre',               5,   'Cible ferme'),
        ('agriculture',                   10,   'Cible ferme'),
        ('travail',                      null,  'Non renseignée'),
        ('sante',                        null,  'Non renseignée'),
        ('Ministères sociaux',           138,   'Cible ferme'),
        ('transformation',               null,  'Non renseignée')
    ) as t(perimetre_key, cible_etablissements, fiabilite_cible)
),

-- Agrégations par line_ministry
stats as (
    select
        annee,
        cantine_line_ministry                                                       as perimetre_key,
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
    where cantine_line_ministry is not null
      and cantine_secteur != 'administration_etablissement_public'
    group by annee, cantine_line_ministry
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

all_stats as (
    select * from stats
    union all
    select * from stats_groupe
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
    w.niveau_ademe,

    -- cible établissements (fallback sur nb_inscrites si pas de cible officielle)
    coalesce(c.cible_etablissements, i.nb_inscrites)                                 as cible_etablissements,
    case
        when c.cible_etablissements is null then 'Non renseignée'
        else c.fiabilite_cible
    end                                                                              as fiabilite_cible,

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
order by s.annee, r.sort_order
