{{ config(materialized='table') }}

-- Vue 2 : ATE éclaté par région
-- Dénominateur : cantines ATE par région inscrites avant le 29 avril de l'année n+1

with canteens_ate as (
    select
        region,
        region_lib,
        creation_date
    from {{ ref('stg_canteens') }}
    where line_ministry = 'administration_territoriale'
      and region is not null
      and region != ''
),

years as (
    select distinct year as annee
    from {{ ref('stg_teledeclarations') }}
    where line_ministry = 'administration_territoriale'
),

nb_inscrites_region as (
    select
        c.region,
        c.region_lib,
        y.annee,
        count(*)                    as nb_inscrites
    from canteens_ate c
    cross join years y
    where c.creation_date <= make_date(y.annee::int + 1, 4, 29)
    group by c.region, c.region_lib, y.annee
),

stats as (
    select
        annee,
        cantine_region                                                              as region,
        cantine_lib_region                                                          as lib_region,
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
        sum(case when valeur_viandes_volailles_egalim > 0
                  and valeur_produits_de_la_mer_egalim > 0
                 then 1 else 0 end)                                                 as nb_td_vp_renseignes,
        sum(case when valeur_egalim_agg is not null then 1 else 0 end)                     as nb_td_egalim_renseignes
    from {{ ref('mart_teledeclarations') }}
    where cantine_line_ministry = 'administration_territoriale'
      and cantine_region is not null
    group by annee, cantine_region, cantine_lib_region
)

select
    s.annee,
    s.region,
    coalesce(s.lib_region, i.region_lib, s.region)                                 as lib_region,

    coalesce(i.nb_inscrites, 0)                                                     as nb_inscrites,
    s.nb_td                                                                         as nb_teledeclarations,
    round((100.0 * s.nb_td / nullif(i.nb_inscrites, 0))::numeric, 1)               as taux_td_pct,

    round((100.0 * s.valeur_egalim_agg / nullif(s.valeur_totale, 0))::numeric, 1)  as part_egalim_pct,
    round((100.0 * s.valeur_bio_agg    / nullif(s.valeur_totale, 0))::numeric, 1)  as part_bio_pct,
    round((100.0 * s.total_france      / nullif(s.valeur_totale, 0))::numeric, 1)  as part_france_pct,
    round((100.0 * (s.vv_egalim + s.pdm_egalim) / nullif(s.vv + s.pdm, 0))::numeric, 1) as part_vp_egalim_pct,
    round((100.0 * s.vv_egalim         / nullif(s.vv, 0))::numeric, 1)             as part_vv_egalim_pct,
    round((100.0 * s.vv_france         / nullif(s.vv, 0))::numeric, 1)             as part_vv_france_pct,

    s.nb_bio                                                                        as nb_cantines_atteint_bio,
    round((100.0 * s.nb_bio            / nullif(s.nb_td, 0))::numeric, 1)          as taux_atteint_bio_pct,
    s.nb_egalim                                                                     as nb_cantines_atteint_egalim,
    round((100.0 * s.nb_egalim         / nullif(s.nb_td, 0))::numeric, 1)          as taux_atteint_egalim_pct,
    s.nb_bio_et_egalim                                                              as nb_cantines_atteint_bio_et_egalim,
    round((100.0 * s.nb_bio_et_egalim  / nullif(s.nb_td, 0))::numeric, 1)          as taux_atteint_bio_et_egalim_pct,
    s.nb_vp_egalim                                                                  as nb_cantines_atteint_vp_egalim,
    round((100.0 * s.nb_vp_egalim      / nullif(s.nb_td, 0))::numeric, 1)          as taux_atteint_vp_egalim_pct,
    s.nb_3_obj                                                                      as nb_cantines_atteint_3_objectifs,
    round((100.0 * s.nb_3_obj          / nullif(s.nb_td, 0))::numeric, 1)          as taux_atteint_3_objectifs_pct,

    s.nb_td_vp_renseignes                                                           as nb_td_vp_renseignes,
    round((100.0 * s.nb_td_vp_renseignes    / nullif(s.nb_td, 0))::numeric, 1)     as taux_td_vp_renseignes_pct,
    s.nb_td_egalim_renseignes                                                       as nb_td_egalim_renseignes,
    round((100.0 * s.nb_td_egalim_renseignes / nullif(s.nb_td, 0))::numeric, 1)    as taux_td_egalim_renseignes_pct

from stats s
left join nb_inscrites_region i
    on i.region = s.region
    and i.annee = s.annee
order by s.annee, lib_region
