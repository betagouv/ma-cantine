{{ config(materialized='table') }}

-- Vue 2 : ATE éclaté par région (total) et par secteur (détail)
-- Structure miroir de mart_spe_bilan : région = groupe, secteur = périmètre
-- Dénominateur nb_inscrites : disponible au niveau région uniquement

with waste_base as (
    select
        w.annee,
        c.region,
        w.canteen_id,
        w.total_mass,
        w.meal_count,
        case
            when jsonb_array_length(c.sector_list::jsonb) > 1
                then 'Secteurs multiples'
            else (array(select jsonb_array_elements_text(c.sector_list::jsonb)))[1]
        end                                 as secteur
    from {{ ref('stg_waste_measurements') }} w
    join {{ ref('stg_canteens') }} c
        on c.canteen_id = w.canteen_id
        and c.line_ministry = 'administration_territoriale'
        and c.region is not null
),

waste_by_region as (
    select
        annee,
        region,
        count(distinct canteen_id)          as nb_canteens_avec_mesure,
        sum(total_mass)                     as total_mass_kg,
        sum(meal_count)                     as total_meal_count
    from waste_base
    group by annee, region
),

waste_by_region_sector as (
    select
        annee,
        region,
        secteur,
        count(distinct canteen_id)          as nb_canteens_avec_mesure,
        sum(total_mass)                     as total_mass_kg,
        sum(meal_count)                     as total_meal_count
    from waste_base
    group by annee, region, secteur
),

canteens_ate as (
    select
        region,
        region_lib,
        creation_date,
        case
            when jsonb_array_length(sector_list::jsonb) > 1 then 'Secteurs multiples'
            else (array(select jsonb_array_elements_text(sector_list::jsonb)))[1]
        end                         as secteur
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

nb_inscrites_region_sector as (
    select
        c.region,
        c.region_lib,
        c.secteur,
        y.annee,
        count(*)                    as nb_inscrites
    from canteens_ate c
    cross join years y
    where c.creation_date <= make_date(y.annee::int + 1, 4, 29)
    group by c.region, c.region_lib, c.secteur, y.annee
),

-- Cibles ventilées par secteur (RIA / RA) pour toutes les régions ATE
ref_cibles_region_sector as (
    select * from (values
        -- AURA
        ('84', 'administration_inter_administratif',  12, 'Cible ferme'),
        ('84', 'administration_administratif',          1, 'Cible à préciser'),
        -- BFC
        ('27', 'administration_inter_administratif',   4, 'Cible ferme'),
        ('27', 'administration_administratif',          1, 'Cible ferme'),
        -- BZH
        ('53', 'administration_inter_administratif',   5, 'Cible ferme'),
        ('53', 'administration_administratif',          0, 'Cible ferme'),
        -- CVL
        ('24', 'administration_inter_administratif',   6, 'Cible ferme'),
        ('24', 'administration_administratif',          0, 'Cible ferme'),
        -- Corse
        ('94', 'administration_inter_administratif',   1, 'Cible ferme'),
        ('94', 'administration_administratif',          0, 'Cible ferme'),
        -- Grand Est
        ('44', 'administration_inter_administratif',  12, 'Cible ferme'),
        ('44', 'administration_administratif',          0, 'Cible ferme'),
        -- Hauts-de-France
        ('32', 'administration_inter_administratif',   4, 'Cible ferme'),
        ('32', 'administration_administratif',          1, 'Cible ferme'),
        -- Île-de-France
        ('11', 'administration_inter_administratif',   7, 'Cible ferme'),
        ('11', 'administration_administratif',          3, 'Cible ferme'),
        -- Normandie
        ('28', 'administration_inter_administratif',   7, 'Cible ferme'),
        ('28', 'administration_administratif',          1, 'Précision en cours'),
        -- Nouvelle-Aquitaine
        ('75', 'administration_inter_administratif',  12, 'Cible ferme'),
        ('75', 'administration_administratif',          6, 'Précision en cours'),
        -- Occitanie
        ('76', 'administration_inter_administratif',   9, 'Cible ferme'),
        ('76', 'administration_administratif',          1, 'Précision en cours'),
        -- PACA
        ('93', 'administration_inter_administratif',   4, 'Cible ferme'),
        ('93', 'administration_administratif',          0, 'Cible ferme'),
        -- Pays de la Loire
        ('52', 'administration_inter_administratif',  10, 'Cible ferme'),
        ('52', 'administration_administratif',          0, 'Cible ferme')
    ) as t(region, secteur, cible_etablissements, fiabilite_cible)
),

-- Cibles région : somme des cibles secteur (toutes les régions ont désormais un détail)
ref_cibles_region as (
    select
        region,
        null::text                                                                      as region_lib,
        sum(cible_etablissements)                                                       as cible_etablissements,
        case when bool_and(fiabilite_cible = 'Cible ferme')
             then 'Cible ferme' else 'Précision en cours'
        end                                                                             as fiabilite_cible
    from ref_cibles_region_sector
    group by region
),

-- Cantines à inclure dans le périmètre ATE avec secteur forcé (hors line_ministry standard)
overrides_secteur_ate as (
    select * from (values
        ('94807198000015', 'administration_inter_administratif')
    ) as t(siret, secteur_force)
),

-- Totaux par région
stats_region as (
    select
        annee,
        cantine_region                                                              as region,
        cantine_lib_region                                                          as lib_region,
        null::text                                                                  as secteur,
        true                                                                        as est_total_region,
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
        sum(case when valeur_egalim_agg is not null then 1 else 0 end)              as nb_td_egalim_renseignes,
        sum(choix_multiple::int)                                                    as nb_choix_multiple,
        sum(atteint_vege_quotidien::int)                                            as nb_vege_quotidien,
        sum(td_volet_diversification_complet::int)                                  as nb_td_diversification_complet
    from {{ ref('mart_teledeclarations') }}
    left join overrides_secteur_ate o on o.siret = cantine_siret
    where (cantine_line_ministry = 'administration_territoriale' and cantine_region is not null)
       or o.siret is not null
    group by annee, cantine_region, cantine_lib_region
),

-- Détail par secteur au sein de chaque région
stats_secteur as (
    select
        annee,
        cantine_region                                                              as region,
        cantine_lib_region                                                          as lib_region,
        coalesce(o.secteur_force, cantine_secteur)                                 as secteur,
        false                                                                       as est_total_region,
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
        sum(case when valeur_egalim_agg is not null then 1 else 0 end)              as nb_td_egalim_renseignes,
        sum(choix_multiple::int)                                                    as nb_choix_multiple,
        sum(atteint_vege_quotidien::int)                                            as nb_vege_quotidien,
        sum(td_volet_diversification_complet::int)                                  as nb_td_diversification_complet
    from {{ ref('mart_teledeclarations') }}
    left join overrides_secteur_ate o on o.siret = cantine_siret
    where (cantine_line_ministry = 'administration_territoriale' and cantine_region is not null)
       or o.siret is not null
    group by annee, cantine_region, cantine_lib_region, coalesce(o.secteur_force, cantine_secteur)
),

all_stats as (
    select * from stats_region
    union all
    select * from stats_secteur
)

select
    s.annee,
    s.region,
    coalesce(s.lib_region, i.region_lib, s.region)                                 as lib_region,
    s.secteur,
    s.est_total_region,

    coalesce(case when s.est_total_region then i.nb_inscrites else is_.nb_inscrites end, 0) as nb_inscrites,
    s.nb_td                                                                         as nb_teledeclarations,
    round((100.0 * s.nb_td / nullif(
        case when s.est_total_region then i.nb_inscrites else is_.nb_inscrites end, 0
    ))::numeric, 1)                                                                 as taux_td_pct,

    round((100.0 * s.valeur_egalim_agg / nullif(s.valeur_totale, 0))::numeric, 1)  as part_egalim_pct,
    round((100.0 * s.valeur_bio_agg    / nullif(s.valeur_totale, 0))::numeric, 1)  as part_bio_pct,
    round((100.0 * s.total_france      / nullif(s.valeur_totale, 0))::numeric, 1)  as part_france_pct,
    round((100.0 * (s.vv_egalim + s.pdm_egalim) / nullif(s.vv + s.pdm, 0))::numeric, 1) as part_vp_egalim_pct,
    round((100.0 * s.vv_egalim         / nullif(s.vv, 0))::numeric, 1)             as part_vv_egalim_pct,
    round((100.0 * s.vv_france         / nullif(s.vv, 0))::numeric, 1)             as part_vv_france_pct,

    s.nb_bio                                                                        as nb_cantines_atteint_bio,
    round((100.0 * s.nb_bio            / nullif(case when s.est_total_region then coalesce(cr.cible_etablissements, i.nb_inscrites) else coalesce(crs.cible_etablissements, is_.nb_inscrites) end, 0))::numeric, 1) as taux_atteint_bio_pct,
    s.nb_egalim                                                                     as nb_cantines_atteint_egalim,
    round((100.0 * s.nb_egalim         / nullif(case when s.est_total_region then coalesce(cr.cible_etablissements, i.nb_inscrites) else coalesce(crs.cible_etablissements, is_.nb_inscrites) end, 0))::numeric, 1) as taux_atteint_egalim_pct,
    s.nb_bio_et_egalim                                                              as nb_cantines_atteint_bio_et_egalim,
    round((100.0 * s.nb_bio_et_egalim  / nullif(case when s.est_total_region then coalesce(cr.cible_etablissements, i.nb_inscrites) else coalesce(crs.cible_etablissements, is_.nb_inscrites) end, 0))::numeric, 1) as taux_atteint_bio_et_egalim_pct,
    s.nb_vp_egalim                                                                  as nb_cantines_atteint_vp_egalim,
    round((100.0 * s.nb_vp_egalim      / nullif(case when s.est_total_region then coalesce(cr.cible_etablissements, i.nb_inscrites) else coalesce(crs.cible_etablissements, is_.nb_inscrites) end, 0))::numeric, 1) as taux_atteint_vp_egalim_pct,
    s.nb_3_obj                                                                      as nb_cantines_atteint_3_objectifs,
    round((100.0 * s.nb_3_obj          / nullif(case when s.est_total_region then coalesce(cr.cible_etablissements, i.nb_inscrites) else coalesce(crs.cible_etablissements, is_.nb_inscrites) end, 0))::numeric, 1) as taux_atteint_3_objectifs_pct,

    s.nb_td_vp_renseignes                                                           as nb_td_vp_renseignes,
    round((100.0 * s.nb_td_vp_renseignes    / nullif(case when s.est_total_region then coalesce(cr.cible_etablissements, i.nb_inscrites) else coalesce(crs.cible_etablissements, is_.nb_inscrites) end, 0))::numeric, 1) as taux_td_vp_renseignes_pct,
    s.nb_td_egalim_renseignes                                                       as nb_td_egalim_renseignes,
    round((100.0 * s.nb_td_egalim_renseignes / nullif(case when s.est_total_region then coalesce(cr.cible_etablissements, i.nb_inscrites) else coalesce(crs.cible_etablissements, is_.nb_inscrites) end, 0))::numeric, 1) as taux_td_egalim_renseignes_pct,

    s.nb_choix_multiple                                                             as nb_cantines_choix_multiple,
    s.nb_vege_quotidien                                                             as nb_cantines_vege_quotidien,
    round((100.0 * s.nb_vege_quotidien / nullif(s.nb_choix_multiple, 0))::numeric, 1) as taux_vege_quotidien_pct,

    s.nb_td_diversification_complet                                                 as nb_td_diversification_complet,
    round((100.0 * s.nb_td_diversification_complet / nullif(
        case when s.est_total_region then i.nb_inscrites else is_.nb_inscrites end, 0
    ))::numeric, 1)                                                                 as taux_td_diversification_complet_pct,

    -- gaspillage : région pour les totaux, secteur pour le détail
    coalesce(wrs.nb_canteens_avec_mesure, wr.nb_canteens_avec_mesure)               as nb_canteens_mesure_gaspi,
    round((100.0 * coalesce(wrs.nb_canteens_avec_mesure, wr.nb_canteens_avec_mesure) / nullif(
        case when s.est_total_region then i.nb_inscrites else is_.nb_inscrites end, 0
    ))::numeric, 1)                                                                 as taux_representativite_gaspi_pct,
    round((coalesce(wrs.total_mass_kg, wr.total_mass_kg) * 1000
           / nullif(coalesce(wrs.total_meal_count, wr.total_meal_count), 0))::numeric, 1) as gaspi_g_par_couvert,
    case
        when coalesce(wrs.total_meal_count, wr.total_meal_count) is null
          or coalesce(wrs.total_meal_count, wr.total_meal_count) = 0               then null
        when coalesce(wrs.total_mass_kg, wr.total_mass_kg) * 1000
             / coalesce(wrs.total_meal_count, wr.total_meal_count) <= 47            then 'Niveau 3'
        when coalesce(wrs.total_mass_kg, wr.total_mass_kg) * 1000
             / coalesce(wrs.total_meal_count, wr.total_meal_count) <= 74            then 'Niveau 2'
        when coalesce(wrs.total_mass_kg, wr.total_mass_kg) * 1000
             / coalesce(wrs.total_meal_count, wr.total_meal_count) <= 95            then 'Niveau 1'
        else                                                                             'Non atteint'
    end                                                                             as niveau_ademe,

    -- cible établissements : région (fallback nb_inscrites) ou secteur si cible connue
    case when s.est_total_region
         then coalesce(cr.cible_etablissements, i.nb_inscrites)
         when crs.cible_etablissements is not null
         then crs.cible_etablissements
         else null
    end                                                                             as cible_etablissements,
    case when s.est_total_region
         then coalesce(cr.fiabilite_cible, 'Non renseignée')
         when crs.fiabilite_cible is not null
         then crs.fiabilite_cible
         else null
    end                                                                             as fiabilite_cible,

    -- taux d'inscription : région si cible officielle, secteur si cible secteur connue
    case when s.est_total_region
         then round((100.0 * i.nb_inscrites / nullif(cr.cible_etablissements, 0))::numeric, 1)
         when crs.cible_etablissements is not null
         then round((100.0 * is_.nb_inscrites / nullif(crs.cible_etablissements, 0))::numeric, 1)
         else null
    end                                                                             as taux_inscription_pct

from all_stats s
left join nb_inscrites_region i
    on i.region = s.region
    and i.annee = s.annee
    and s.est_total_region = true
left join nb_inscrites_region_sector is_
    on is_.region = s.region
    and is_.annee = s.annee
    and is_.secteur is not distinct from s.secteur
    and s.est_total_region = false
left join ref_cibles_region cr
    on cr.region = s.region
    and s.est_total_region = true
left join ref_cibles_region_sector crs
    on crs.region = s.region
    and crs.secteur is not distinct from s.secteur
    and s.est_total_region = false
left join waste_by_region wr
    on wr.region = s.region
    and wr.annee = s.annee
    and s.est_total_region = true
left join waste_by_region_sector wrs
    on wrs.region = s.region
    and wrs.annee = s.annee
    and wrs.secteur is not distinct from s.secteur
    and s.est_total_region = false
order by s.annee, coalesce(s.lib_region, i.region_lib, s.region), s.est_total_region desc, s.secteur
