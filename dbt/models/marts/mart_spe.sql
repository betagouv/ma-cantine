with teledeclarations as (
    select * from {{ ref('stg_teledeclarations') }}
    where production_type != 'groupe'
      and teledeclaration_mode != 'SATELLITE_WITHOUT_APPRO'
      and (invalid_reason_list is null or invalid_reason_list::text = '[]')
      and line_ministry is not null
      and line_ministry != ''
)

select
    line_ministry,
    year,

    -- volumes
    count(*)                                                                as nb_teledeclarations,
    count(distinct canteen_id)                                              as nb_cantines,

    -- appro — totaux
    sum(valeur_totale)                                                      as sum_valeur_totale,
    sum(valeur_bio)                                                         as sum_valeur_bio,
    sum(valeur_egalim_agg)                                                  as sum_valeur_egalim,
    sum(valeur_viandes_et_poissons)                                         as sum_valeur_viandes_et_poissons,
    sum(valeur_viandes_et_poissons_egalim)                                  as sum_valeur_viandes_et_poissons_egalim,

    sum(total_origine_france)                                               as sum_total_origine_france,

    -- taux agrégés (sum numérateur / sum dénominateur)
    sum(total_origine_france)        / nullif(sum(valeur_totale), 0)        as taux_origine_france,
    sum(valeur_bio)                  / nullif(sum(valeur_totale), 0)        as taux_bio,
    sum(valeur_egalim_agg)           / nullif(sum(valeur_totale), 0)        as taux_egalim,
    sum(valeur_viandes_et_poissons_egalim)
        / nullif(sum(valeur_viandes_et_poissons), 0)                        as taux_egalim_viandes_et_poissons,

    -- objectifs EGalim (nb cantines atteignant le seuil)
    count(*) filter (
        where valeur_bio / nullif(valeur_totale, 0) >= 0.20
    )                                                                       as nb_cantines_objectif_bio,
    count(*) filter (
        where valeur_egalim_agg / nullif(valeur_totale, 0) >= 0.50
    )                                                                       as nb_cantines_objectif_egalim,
    count(*) filter (
        where valeur_bio / nullif(valeur_totale, 0) >= 0.20
          and valeur_egalim_agg / nullif(valeur_totale, 0) >= 0.50
    )                                                                       as nb_cantines_objectif_bio_et_egalim,
    count(*) filter (
        where valeur_viandes_et_poissons > 0
          and valeur_viandes_et_poissons_egalim / nullif(valeur_viandes_et_poissons, 0) >= 1.0
    )                                                                       as nb_cantines_objectif_viandes_et_poissons_egalim

from teledeclarations
group by line_ministry, year
order by year, line_ministry
