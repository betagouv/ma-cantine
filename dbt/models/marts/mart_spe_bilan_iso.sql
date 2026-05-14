{{ config(materialized='table') }}

-- Vue 4 : Comparaison sur échantillon isométrique (intersection stricte)
-- ISO 2 ans : cantines ayant TD en n-1 ET en n — classification figée sur n-1
-- ISO 3 ans : cantines ayant TD en n-2, n-1 ET n — classification figée sur n-2
-- nb_td identique sur toutes les années comparées (isométrique par construction)

with base as (
    select
        canteen_id,
        annee,
        cantine_line_ministry,
        valeur_totale,
        valeur_bio_agg,
        valeur_egalim_agg,
        valeur_viandes_volailles,
        valeur_viandes_volailles_egalim,
        valeur_produits_de_la_mer,
        valeur_produits_de_la_mer_egalim,
        total_origine_france,
        valeur_viandes_volailles_france,
        atteint_bio,
        atteint_egalim,
        atteint_bio_et_egalim,
        atteint_viandes_et_poissons_egalim,
        atteint_3_objectifs,
        choix_multiple,
        atteint_vege_quotidien,
        td_volet_diversification_complet
    from {{ ref('mart_teledeclarations') }}
),

-- Années consécutives par cantine (toutes les TD valides, sans filtre line_ministry)
td_years as (
    select
        canteen_id,
        annee,
        lag(annee, 1) over (partition by canteen_id order by annee) as prev_1,
        lag(annee, 2) over (partition by canteen_id order by annee) as prev_2
    from (select distinct canteen_id, annee from base) t
),

-- Echantillon ISO : classification = line_ministry de l'année n (annee_ref)
-- Repêchage : cantines sans line_ministry les années précédentes mais classées en n
iso_sample as (
    select
        t.canteen_id,
        t.annee                             as annee_ref,
        '2ans'::text                        as iso_type,
        b_n.cantine_line_ministry           as perimetre_key
    from td_years t
    join base b_n
        on b_n.canteen_id = t.canteen_id
        and b_n.annee = t.annee
    where t.prev_1 = t.annee - 1
      and b_n.cantine_line_ministry is not null

    union all

    select
        t.canteen_id,
        t.annee                             as annee_ref,
        '3ans'::text                        as iso_type,
        b_n.cantine_line_ministry           as perimetre_key
    from td_years t
    join base b_n
        on b_n.canteen_id = t.canteen_id
        and b_n.annee = t.annee
    where t.prev_1 = t.annee - 1
      and t.prev_2 = t.annee - 2
      and b_n.cantine_line_ministry is not null
),

-- TDs des cantines ISO pour toutes les années concernées
-- perimetre_key vient de iso_sample (classification de l'année n)
iso_td as (
    select
        s.annee_ref,
        s.iso_type,
        s.perimetre_key,
        b.annee                                 as annee_td,
        b.valeur_totale,
        b.valeur_bio_agg,
        b.valeur_egalim_agg,
        b.valeur_viandes_volailles              as vv,
        b.valeur_viandes_volailles_egalim       as vv_egalim,
        b.valeur_produits_de_la_mer             as pdm,
        b.valeur_produits_de_la_mer_egalim      as pdm_egalim,
        b.total_origine_france,
        b.valeur_viandes_volailles_france       as vv_france,
        b.atteint_bio,
        b.atteint_egalim,
        b.atteint_bio_et_egalim,
        b.atteint_viandes_et_poissons_egalim,
        b.atteint_3_objectifs,
        b.choix_multiple,
        b.atteint_vege_quotidien,
        b.td_volet_diversification_complet
    from iso_sample s
    join base b on b.canteen_id = s.canteen_id
    where (s.iso_type = '2ans' and b.annee in (s.annee_ref, s.annee_ref - 1))
       or (s.iso_type = '3ans' and b.annee in (s.annee_ref, s.annee_ref - 1, s.annee_ref - 2))
),

-- Agrégation par (annee_ref, iso_type, annee_td, perimetre_key)
stats_lm as (
    select
        annee_ref,
        iso_type,
        annee_td,
        perimetre_key,
        count(*)                                                            as nb_td,
        sum(valeur_totale)                                                  as valeur_totale,
        sum(valeur_bio_agg)                                                 as valeur_bio_agg,
        sum(valeur_egalim_agg)                                              as valeur_egalim_agg,
        sum(vv)                                                             as vv,
        sum(vv_egalim)                                                      as vv_egalim,
        sum(pdm)                                                            as pdm,
        sum(pdm_egalim)                                                     as pdm_egalim,
        sum(total_origine_france)                                           as total_france,
        sum(vv_france)                                                      as vv_france,
        sum(atteint_bio::int)                                               as nb_bio,
        sum(atteint_egalim::int)                                            as nb_egalim,
        sum(atteint_bio_et_egalim::int)                                     as nb_bio_et_egalim,
        sum(atteint_viandes_et_poissons_egalim::int)                        as nb_vp_egalim,
        sum(atteint_3_objectifs::int)                                       as nb_3_obj,
        sum(case when vv_egalim > 0 and pdm_egalim > 0 then 1 else 0 end)  as nb_td_vp_renseignes,
        sum(choix_multiple::int)                                            as nb_choix_multiple,
        sum(atteint_vege_quotidien::int)                                    as nb_vege_quotidien,
        sum(td_volet_diversification_complet::int)                          as nb_td_diversification_complet
    from iso_td
    group by annee_ref, iso_type, annee_td, perimetre_key
),

-- Sous-totaux groupe
stats_groupe as (
    select
        annee_ref,
        iso_type,
        annee_td,
        case
            when perimetre_key in ('ecologie', 'mer')                             then 'MTE'
            when perimetre_key in ('jeunesse', 'enseignement_superieur', 'sport') then 'MEJSESR'
            when perimetre_key in ('justice_hors_pjj', 'justice_pjj')             then 'Justice'
            when perimetre_key in ('travail', 'sante')                            then 'Ministères sociaux'
        end                                                                         as perimetre_key,
        sum(nb_td)                  as nb_td,
        sum(valeur_totale)          as valeur_totale,
        sum(valeur_bio_agg)         as valeur_bio_agg,
        sum(valeur_egalim_agg)      as valeur_egalim_agg,
        sum(vv)                     as vv,
        sum(vv_egalim)              as vv_egalim,
        sum(pdm)                    as pdm,
        sum(pdm_egalim)             as pdm_egalim,
        sum(total_france)           as total_france,
        sum(vv_france)              as vv_france,
        sum(nb_bio)                 as nb_bio,
        sum(nb_egalim)              as nb_egalim,
        sum(nb_bio_et_egalim)       as nb_bio_et_egalim,
        sum(nb_vp_egalim)           as nb_vp_egalim,
        sum(nb_3_obj)               as nb_3_obj,
        sum(nb_td_vp_renseignes)    as nb_td_vp_renseignes,
        sum(nb_choix_multiple)                  as nb_choix_multiple,
        sum(nb_vege_quotidien)                  as nb_vege_quotidien,
        sum(nb_td_diversification_complet)      as nb_td_diversification_complet
    from stats_lm
    where perimetre_key in (
        'ecologie', 'mer',
        'jeunesse', 'enseignement_superieur', 'sport',
        'justice_hors_pjj', 'justice_pjj',
        'travail', 'sante'
    )
    group by
        annee_ref,
        iso_type,
        annee_td,
        case
            when perimetre_key in ('ecologie', 'mer')                             then 'MTE'
            when perimetre_key in ('jeunesse', 'enseignement_superieur', 'sport') then 'MEJSESR'
            when perimetre_key in ('justice_hors_pjj', 'justice_pjj')             then 'Justice'
            when perimetre_key in ('travail', 'sante')                            then 'Ministères sociaux'
        end
),

all_stats as (
    select * from stats_lm
    union all
    select * from stats_groupe
),

-- Pivot : une colonne par année (n, n-1, n-2)
pivoted as (
    select
        annee_ref,
        iso_type,
        perimetre_key,

        max(case when annee_td = annee_ref     then nb_td           end) as nb_td_n,
        max(case when annee_td = annee_ref - 1 then nb_td           end) as nb_td_n1,
        max(case when annee_td = annee_ref - 2 then nb_td           end) as nb_td_n2,

        max(case when annee_td = annee_ref     then valeur_totale   end) as vt_n,
        max(case when annee_td = annee_ref - 1 then valeur_totale   end) as vt_n1,
        max(case when annee_td = annee_ref - 2 then valeur_totale   end) as vt_n2,

        max(case when annee_td = annee_ref     then valeur_bio_agg  end) as bio_n,
        max(case when annee_td = annee_ref - 1 then valeur_bio_agg  end) as bio_n1,
        max(case when annee_td = annee_ref - 2 then valeur_bio_agg  end) as bio_n2,

        max(case when annee_td = annee_ref     then valeur_egalim_agg end) as egalim_n,
        max(case when annee_td = annee_ref - 1 then valeur_egalim_agg end) as egalim_n1,
        max(case when annee_td = annee_ref - 2 then valeur_egalim_agg end) as egalim_n2,

        max(case when annee_td = annee_ref     then vv              end) as vv_n,
        max(case when annee_td = annee_ref - 1 then vv              end) as vv_n1,
        max(case when annee_td = annee_ref - 2 then vv              end) as vv_n2,
        max(case when annee_td = annee_ref     then vv_egalim       end) as vv_egalim_n,
        max(case when annee_td = annee_ref - 1 then vv_egalim       end) as vv_egalim_n1,
        max(case when annee_td = annee_ref - 2 then vv_egalim       end) as vv_egalim_n2,
        max(case when annee_td = annee_ref     then pdm             end) as pdm_n,
        max(case when annee_td = annee_ref - 1 then pdm             end) as pdm_n1,
        max(case when annee_td = annee_ref - 2 then pdm             end) as pdm_n2,
        max(case when annee_td = annee_ref     then pdm_egalim      end) as pdm_egalim_n,
        max(case when annee_td = annee_ref - 1 then pdm_egalim      end) as pdm_egalim_n1,
        max(case when annee_td = annee_ref - 2 then pdm_egalim      end) as pdm_egalim_n2,

        max(case when annee_td = annee_ref     then total_france    end) as france_n,
        max(case when annee_td = annee_ref - 1 then total_france    end) as france_n1,
        max(case when annee_td = annee_ref - 2 then total_france    end) as france_n2,
        max(case when annee_td = annee_ref     then vv_france       end) as vv_france_n,
        max(case when annee_td = annee_ref - 1 then vv_france       end) as vv_france_n1,
        max(case when annee_td = annee_ref - 2 then vv_france       end) as vv_france_n2,

        max(case when annee_td = annee_ref     then nb_bio          end) as nb_bio_n,
        max(case when annee_td = annee_ref - 1 then nb_bio          end) as nb_bio_n1,
        max(case when annee_td = annee_ref - 2 then nb_bio          end) as nb_bio_n2,
        max(case when annee_td = annee_ref     then nb_egalim       end) as nb_egalim_n,
        max(case when annee_td = annee_ref - 1 then nb_egalim       end) as nb_egalim_n1,
        max(case when annee_td = annee_ref - 2 then nb_egalim       end) as nb_egalim_n2,
        max(case when annee_td = annee_ref     then nb_bio_et_egalim end) as nb_bio_et_egalim_n,
        max(case when annee_td = annee_ref - 1 then nb_bio_et_egalim end) as nb_bio_et_egalim_n1,
        max(case when annee_td = annee_ref - 2 then nb_bio_et_egalim end) as nb_bio_et_egalim_n2,
        max(case when annee_td = annee_ref     then nb_vp_egalim    end) as nb_vp_egalim_n,
        max(case when annee_td = annee_ref - 1 then nb_vp_egalim    end) as nb_vp_egalim_n1,
        max(case when annee_td = annee_ref - 2 then nb_vp_egalim    end) as nb_vp_egalim_n2,
        max(case when annee_td = annee_ref     then nb_3_obj        end) as nb_3_obj_n,
        max(case when annee_td = annee_ref - 1 then nb_3_obj        end) as nb_3_obj_n1,
        max(case when annee_td = annee_ref - 2 then nb_3_obj        end) as nb_3_obj_n2,
        max(case when annee_td = annee_ref     then nb_td_vp_renseignes end) as nb_td_vp_n,
        max(case when annee_td = annee_ref - 1 then nb_td_vp_renseignes end) as nb_td_vp_n1,

        max(case when annee_td = annee_ref     then nb_choix_multiple   end) as nb_choix_multiple_n,
        max(case when annee_td = annee_ref - 1 then nb_choix_multiple   end) as nb_choix_multiple_n1,
        max(case when annee_td = annee_ref - 2 then nb_choix_multiple   end) as nb_choix_multiple_n2,
        max(case when annee_td = annee_ref     then nb_vege_quotidien   end) as nb_vege_n,
        max(case when annee_td = annee_ref - 1 then nb_vege_quotidien   end) as nb_vege_n1,
        max(case when annee_td = annee_ref - 2 then nb_vege_quotidien   end) as nb_vege_n2,
        max(case when annee_td = annee_ref     then nb_td_diversification_complet end) as nb_diversification_n,
        max(case when annee_td = annee_ref - 1 then nb_td_diversification_complet end) as nb_diversification_n1,
        max(case when annee_td = annee_ref - 2 then nb_td_diversification_complet end) as nb_diversification_n2

    from all_stats
    group by annee_ref, iso_type, perimetre_key
),

ref_perimetre as (
    select * from (values
        (1,  'mer',                         'Mer',                                         'MTE',                false),
        (2,  'ecologie',                    'Environnement',                               'MTE',                false),
        (3,  'MTE',                         'TOTAL MTE',                                   'MTE',                true),
        (4,  'affaires_etrangeres',         'Affaires étrangères',                         null,                 false),
        (5,  'armee',                       'Armées',                                      null,                 false),
        (6,  'autorites_independantes',     'AAI',                                         null,                 false),
        (7,  'culture',                     'Culture',                                     null,                 false),
        (8,  'economie',                    'Économie et finances',                        null,                 false),
        (9,  'jeunesse',                    'Éducation nationale',                         'MEJSESR',            false),
        (10, 'enseignement_superieur',      'Enseignement supérieur et recherche',         'MEJSESR',            false),
        (11, 'sport',                       'Sports',                                      'MEJSESR',            false),
        (12, 'MEJSESR',                     'TOTAL MEJSESR',                               'MEJSESR',            true),
        (13, 'justice_hors_pjj',            'Justice hors PJJ',                            'Justice',            false),
        (14, 'justice_pjj',                 'Justice PJJ',                                 'Justice',            false),
        (15, 'Justice',                     'TOTAL Justice',                               'Justice',            true),
        (16, 'interieur',                   'Intérieur',                                   null,                 false),
        (17, 'premier_ministre',            'Premier ministre',                            null,                 false),
        (18, 'agriculture',                 'Agriculture',                                 null,                 false),
        (19, 'travail',                     'Travail',                                     'Ministères sociaux', false),
        (20, 'sante',                       'Santé',                                       'Ministères sociaux', false),
        (21, 'Ministères sociaux',          'TOTAL Ministères sociaux',                    'Ministères sociaux', true),
        (22, 'transformation',              'Fonction Publique',                            null,                false),
        (23, 'administration_territoriale', 'Administration territoriale de l''État (ATE)', null,                false)
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
)

select
    r.sort_order,
    r.perimetre_key,
    r.perimetre_lib,
    r.groupe_spe,
    r.groupe_lib,
    r.est_total_groupe,
    p.annee_ref,
    p.iso_type,

    -- Taille échantillon ISO (identique sur toutes les années par construction)
    p.nb_td_n                                                                       as nb_td_iso_n,
    p.nb_td_n1                                                                      as nb_td_iso_n1,
    p.nb_td_n2                                                                      as nb_td_iso_n2,

    -- Part EGalim
    round((100.0 * p.egalim_n  / nullif(p.vt_n,  0))::numeric, 1)                  as part_egalim_n,
    round((100.0 * p.egalim_n1 / nullif(p.vt_n1, 0))::numeric, 1)                  as part_egalim_n1,
    round((100.0 * p.egalim_n2 / nullif(p.vt_n2, 0))::numeric, 1)                  as part_egalim_n2,
    round((100.0 * p.egalim_n  / nullif(p.vt_n,  0)
         - 100.0 * p.egalim_n1 / nullif(p.vt_n1, 0))::numeric, 1)                  as delta_egalim_n1,
    round((100.0 * p.egalim_n  / nullif(p.vt_n,  0)
         - 100.0 * p.egalim_n2 / nullif(p.vt_n2, 0))::numeric, 1)                  as delta_egalim_n2,

    -- Part bio
    round((100.0 * p.bio_n  / nullif(p.vt_n,  0))::numeric, 1)                     as part_bio_n,
    round((100.0 * p.bio_n1 / nullif(p.vt_n1, 0))::numeric, 1)                     as part_bio_n1,
    round((100.0 * p.bio_n2 / nullif(p.vt_n2, 0))::numeric, 1)                     as part_bio_n2,
    round((100.0 * p.bio_n  / nullif(p.vt_n,  0)
         - 100.0 * p.bio_n1 / nullif(p.vt_n1, 0))::numeric, 1)                     as delta_bio_n1,
    round((100.0 * p.bio_n  / nullif(p.vt_n,  0)
         - 100.0 * p.bio_n2 / nullif(p.vt_n2, 0))::numeric, 1)                     as delta_bio_n2,

    -- Part origine France
    round((100.0 * p.france_n  / nullif(p.vt_n,  0))::numeric, 1)                  as part_france_n,
    round((100.0 * p.france_n1 / nullif(p.vt_n1, 0))::numeric, 1)                  as part_france_n1,
    round((100.0 * p.france_n2 / nullif(p.vt_n2, 0))::numeric, 1)                  as part_france_n2,
    round((100.0 * p.france_n  / nullif(p.vt_n,  0)
         - 100.0 * p.france_n1 / nullif(p.vt_n1, 0))::numeric, 1)                  as delta_france_n1,
    round((100.0 * p.france_n  / nullif(p.vt_n,  0)
         - 100.0 * p.france_n2 / nullif(p.vt_n2, 0))::numeric, 1)                  as delta_france_n2,

    -- Part V&P EGalim
    round((100.0 * (p.vv_egalim_n  + p.pdm_egalim_n)  / nullif(p.vv_n  + p.pdm_n,  0))::numeric, 1) as part_vp_egalim_n,
    round((100.0 * (p.vv_egalim_n1 + p.pdm_egalim_n1) / nullif(p.vv_n1 + p.pdm_n1, 0))::numeric, 1) as part_vp_egalim_n1,
    round((100.0 * (p.vv_egalim_n2 + p.pdm_egalim_n2) / nullif(p.vv_n2 + p.pdm_n2, 0))::numeric, 1) as part_vp_egalim_n2,
    round((100.0 * (p.vv_egalim_n  + p.pdm_egalim_n)  / nullif(p.vv_n  + p.pdm_n,  0)
         - 100.0 * (p.vv_egalim_n1 + p.pdm_egalim_n1) / nullif(p.vv_n1 + p.pdm_n1, 0))::numeric, 1) as delta_vp_egalim_n1,
    round((100.0 * (p.vv_egalim_n  + p.pdm_egalim_n)  / nullif(p.vv_n  + p.pdm_n,  0)
         - 100.0 * (p.vv_egalim_n2 + p.pdm_egalim_n2) / nullif(p.vv_n2 + p.pdm_n2, 0))::numeric, 1) as delta_vp_egalim_n2,

    -- Part VV EGalim
    round((100.0 * p.vv_egalim_n  / nullif(p.vv_n,  0))::numeric, 1)               as part_vv_egalim_n,
    round((100.0 * p.vv_egalim_n1 / nullif(p.vv_n1, 0))::numeric, 1)               as part_vv_egalim_n1,
    round((100.0 * p.vv_egalim_n2 / nullif(p.vv_n2, 0))::numeric, 1)               as part_vv_egalim_n2,
    round((100.0 * p.vv_egalim_n  / nullif(p.vv_n,  0)
         - 100.0 * p.vv_egalim_n1 / nullif(p.vv_n1, 0))::numeric, 1)               as delta_vv_egalim_n1,
    round((100.0 * p.vv_egalim_n  / nullif(p.vv_n,  0)
         - 100.0 * p.vv_egalim_n2 / nullif(p.vv_n2, 0))::numeric, 1)               as delta_vv_egalim_n2,

    -- Part VV France
    round((100.0 * p.vv_france_n  / nullif(p.vv_n,  0))::numeric, 1)               as part_vv_france_n,
    round((100.0 * p.vv_france_n1 / nullif(p.vv_n1, 0))::numeric, 1)               as part_vv_france_n1,
    round((100.0 * p.vv_france_n2 / nullif(p.vv_n2, 0))::numeric, 1)               as part_vv_france_n2,
    round((100.0 * p.vv_france_n  / nullif(p.vv_n,  0)
         - 100.0 * p.vv_france_n1 / nullif(p.vv_n1, 0))::numeric, 1)               as delta_vv_france_n1,
    round((100.0 * p.vv_france_n  / nullif(p.vv_n,  0)
         - 100.0 * p.vv_france_n2 / nullif(p.vv_n2, 0))::numeric, 1)               as delta_vv_france_n2,

    -- % cantines atteint bio
    round((100.0 * p.nb_bio_n  / nullif(p.nb_td_n,  0))::numeric, 1)               as taux_atteint_bio_n,
    round((100.0 * p.nb_bio_n1 / nullif(p.nb_td_n1, 0))::numeric, 1)               as taux_atteint_bio_n1,
    round((100.0 * p.nb_bio_n2 / nullif(p.nb_td_n2, 0))::numeric, 1)               as taux_atteint_bio_n2,
    round((100.0 * p.nb_bio_n  / nullif(p.nb_td_n,  0)
         - 100.0 * p.nb_bio_n1 / nullif(p.nb_td_n1, 0))::numeric, 1)               as delta_atteint_bio_n1,
    round((100.0 * p.nb_bio_n  / nullif(p.nb_td_n,  0)
         - 100.0 * p.nb_bio_n2 / nullif(p.nb_td_n2, 0))::numeric, 1)               as delta_atteint_bio_n2,

    -- % cantines atteint EGalim
    round((100.0 * p.nb_egalim_n  / nullif(p.nb_td_n,  0))::numeric, 1)            as taux_atteint_egalim_n,
    round((100.0 * p.nb_egalim_n1 / nullif(p.nb_td_n1, 0))::numeric, 1)            as taux_atteint_egalim_n1,
    round((100.0 * p.nb_egalim_n2 / nullif(p.nb_td_n2, 0))::numeric, 1)            as taux_atteint_egalim_n2,
    round((100.0 * p.nb_egalim_n  / nullif(p.nb_td_n,  0)
         - 100.0 * p.nb_egalim_n1 / nullif(p.nb_td_n1, 0))::numeric, 1)            as delta_atteint_egalim_n1,
    round((100.0 * p.nb_egalim_n  / nullif(p.nb_td_n,  0)
         - 100.0 * p.nb_egalim_n2 / nullif(p.nb_td_n2, 0))::numeric, 1)            as delta_atteint_egalim_n2,

    -- % cantines atteint bio ET EGalim
    round((100.0 * p.nb_bio_et_egalim_n  / nullif(p.nb_td_n,  0))::numeric, 1)     as taux_atteint_bio_et_egalim_n,
    round((100.0 * p.nb_bio_et_egalim_n1 / nullif(p.nb_td_n1, 0))::numeric, 1)     as taux_atteint_bio_et_egalim_n1,
    round((100.0 * p.nb_bio_et_egalim_n2 / nullif(p.nb_td_n2, 0))::numeric, 1)     as taux_atteint_bio_et_egalim_n2,
    round((100.0 * p.nb_bio_et_egalim_n  / nullif(p.nb_td_n,  0)
         - 100.0 * p.nb_bio_et_egalim_n1 / nullif(p.nb_td_n1, 0))::numeric, 1)     as delta_atteint_bio_et_egalim_n1,
    round((100.0 * p.nb_bio_et_egalim_n  / nullif(p.nb_td_n,  0)
         - 100.0 * p.nb_bio_et_egalim_n2 / nullif(p.nb_td_n2, 0))::numeric, 1)     as delta_atteint_bio_et_egalim_n2,

    -- % cantines atteint V&P EGalim
    round((100.0 * p.nb_vp_egalim_n  / nullif(p.nb_td_n,  0))::numeric, 1)         as taux_atteint_vp_egalim_n,
    round((100.0 * p.nb_vp_egalim_n1 / nullif(p.nb_td_n1, 0))::numeric, 1)         as taux_atteint_vp_egalim_n1,
    round((100.0 * p.nb_vp_egalim_n2 / nullif(p.nb_td_n2, 0))::numeric, 1)         as taux_atteint_vp_egalim_n2,
    round((100.0 * p.nb_vp_egalim_n  / nullif(p.nb_td_n,  0)
         - 100.0 * p.nb_vp_egalim_n1 / nullif(p.nb_td_n1, 0))::numeric, 1)         as delta_atteint_vp_egalim_n1,
    round((100.0 * p.nb_vp_egalim_n  / nullif(p.nb_td_n,  0)
         - 100.0 * p.nb_vp_egalim_n2 / nullif(p.nb_td_n2, 0))::numeric, 1)         as delta_atteint_vp_egalim_n2,

    -- % cantines atteint 3 objectifs
    round((100.0 * p.nb_3_obj_n  / nullif(p.nb_td_n,  0))::numeric, 1)             as taux_atteint_3_objectifs_n,
    round((100.0 * p.nb_3_obj_n1 / nullif(p.nb_td_n1, 0))::numeric, 1)             as taux_atteint_3_objectifs_n1,
    round((100.0 * p.nb_3_obj_n2 / nullif(p.nb_td_n2, 0))::numeric, 1)             as taux_atteint_3_objectifs_n2,
    round((100.0 * p.nb_3_obj_n  / nullif(p.nb_td_n,  0)
         - 100.0 * p.nb_3_obj_n1 / nullif(p.nb_td_n1, 0))::numeric, 1)             as delta_atteint_3_objectifs_n1,
    round((100.0 * p.nb_3_obj_n  / nullif(p.nb_td_n,  0)
         - 100.0 * p.nb_3_obj_n2 / nullif(p.nb_td_n2, 0))::numeric, 1)             as delta_atteint_3_objectifs_n2,

    -- Représentativité V&P renseignés
    p.nb_td_vp_n                                                                    as nb_td_vp_renseignes_n,
    p.nb_td_vp_n1                                                                   as nb_td_vp_renseignes_n1,
    round((100.0 * p.nb_td_vp_n  / nullif(p.nb_td_n,  0))::numeric, 1)             as taux_td_vp_renseignes_n,
    round((100.0 * p.nb_td_vp_n1 / nullif(p.nb_td_n1, 0))::numeric, 1)             as taux_td_vp_renseignes_n1,

    -- Végétarien : offre quotidienne parmi cantines à choix multiple
    p.nb_choix_multiple_n,
    p.nb_choix_multiple_n1,
    p.nb_choix_multiple_n2,
    p.nb_vege_n                                                                     as nb_cantines_vege_quotidien_n,
    p.nb_vege_n1                                                                    as nb_cantines_vege_quotidien_n1,
    p.nb_vege_n2                                                                    as nb_cantines_vege_quotidien_n2,
    round((100.0 * p.nb_vege_n  / nullif(p.nb_choix_multiple_n,  0))::numeric, 1)  as taux_vege_quotidien_n,
    round((100.0 * p.nb_vege_n1 / nullif(p.nb_choix_multiple_n1, 0))::numeric, 1)  as taux_vege_quotidien_n1,
    round((100.0 * p.nb_vege_n2 / nullif(p.nb_choix_multiple_n2, 0))::numeric, 1)  as taux_vege_quotidien_n2,
    round((100.0 * p.nb_vege_n  / nullif(p.nb_choix_multiple_n,  0)
         - 100.0 * p.nb_vege_n1 / nullif(p.nb_choix_multiple_n1, 0))::numeric, 1)  as delta_vege_quotidien_n1,
    round((100.0 * p.nb_vege_n  / nullif(p.nb_choix_multiple_n,  0)
         - 100.0 * p.nb_vege_n2 / nullif(p.nb_choix_multiple_n2, 0))::numeric, 1)  as delta_vege_quotidien_n2,

    -- Diversification : volet complet / taille échantillon ISO
    p.nb_diversification_n,
    p.nb_diversification_n1,
    p.nb_diversification_n2,
    round((100.0 * p.nb_diversification_n  / nullif(p.nb_td_n,  0))::numeric, 1)   as taux_diversification_n,
    round((100.0 * p.nb_diversification_n1 / nullif(p.nb_td_n1, 0))::numeric, 1)   as taux_diversification_n1,
    round((100.0 * p.nb_diversification_n2 / nullif(p.nb_td_n2, 0))::numeric, 1)   as taux_diversification_n2,
    round((100.0 * p.nb_diversification_n  / nullif(p.nb_td_n,  0)
         - 100.0 * p.nb_diversification_n1 / nullif(p.nb_td_n1, 0))::numeric, 1)   as delta_diversification_n1,
    round((100.0 * p.nb_diversification_n  / nullif(p.nb_td_n,  0)
         - 100.0 * p.nb_diversification_n2 / nullif(p.nb_td_n2, 0))::numeric, 1)   as delta_diversification_n2

from pivoted p
join ref_perimetre_with_groupe r on r.perimetre_key = p.perimetre_key
order by p.annee_ref, p.iso_type, r.sort_order
