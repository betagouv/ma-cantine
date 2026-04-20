-- Source actuelle : diagnostics_raw (filtré sur les télédéclarations soumises)
-- Source précédente : table teledeclarations (export ETL manuel)
-- Seul ce fichier a été modifié lors du changement de source.
-- Les noms de colonnes exposés restent identiques → mart_teledeclarations inchangé.
-- Les infos cantine viennent du canteen_snapshot (JSON), pas d'une jointure.

with diagnostics as (
    select * from {{ ref('stg_diagnostics') }}
    where teledeclaration_id is not null
      and status = 'SUBMITTED'
),

renamed as (
    select
        -- identifiers
        teledeclaration_id,
        canteen_id,
        year,
        teledeclaration_version,
        creation_source,
        diagnostic_type,
        teledeclaration_mode,

        -- canteen info (extraite du canteen_snapshot JSON)
        canteen_snapshot::jsonb ->> 'name'                              as cantine_name,
        canteen_snapshot::jsonb ->> 'siret'                             as siret,
        canteen_snapshot::jsonb ->> 'siren_unite_legale'                as siren_unite_legale,
        (canteen_snapshot::jsonb ->> 'daily_meal_count')::float         as daily_meal_count,
        (canteen_snapshot::jsonb ->> 'yearly_meal_count')::float        as yearly_meal_count,
        canteen_snapshot::jsonb ->> 'management_type'                   as management_type,
        canteen_snapshot::jsonb ->> 'production_type'                   as production_type,
        canteen_snapshot::jsonb ->> 'economic_model'                    as economic_model,
        canteen_snapshot::jsonb ->> 'line_ministry'                     as line_ministry,
        (canteen_snapshot::jsonb ->> 'line_ministry') is not null       as spe,
        (canteen_snapshot::jsonb ->> 'is_filled')::boolean              as is_filled,
        (canteen_snapshot::jsonb ->> 'production_type') = 'central'     as genere_par_cuisine_centrale,

        -- secteur / catégorie (depuis sector_list dans le snapshot)
        array_to_string(
            array(select jsonb_array_elements_text(canteen_snapshot::jsonb -> 'sector_list')),
            ', '
        )                                                               as secteur,
        case
            when (array(select jsonb_array_elements_text(canteen_snapshot::jsonb -> 'sector_list')))[1] like 'administration%' then 'Administration'
            when (array(select jsonb_array_elements_text(canteen_snapshot::jsonb -> 'sector_list')))[1] like 'entreprise%'     then 'Entreprise'
            when (array(select jsonb_array_elements_text(canteen_snapshot::jsonb -> 'sector_list')))[1] like 'education%'      then 'Enseignement'
            when (array(select jsonb_array_elements_text(canteen_snapshot::jsonb -> 'sector_list')))[1] like 'sante%'          then 'Santé'
            when (array(select jsonb_array_elements_text(canteen_snapshot::jsonb -> 'sector_list')))[1] like 'social%'         then 'Social / Médico-social'
            when (array(select jsonb_array_elements_text(canteen_snapshot::jsonb -> 'sector_list')))[1] like 'loisir%'         then 'Loisirs'
            when (array(select jsonb_array_elements_text(canteen_snapshot::jsonb -> 'sector_list')))[1] is not null            then 'Autres'
        end                                                             as categorie,

        -- satellites (depuis satellites_snapshot si disponible)
        case
            when satellites_snapshot is not null
            then jsonb_array_length(satellites_snapshot::jsonb)
        end                                                             as satellite_canteens_count,

        -- geo (department et region disponibles dans le snapshot, lib non disponibles sans jointure)
        canteen_snapshot::jsonb ->> 'department'                        as department,
        null::text                                                      as department_lib,
        canteen_snapshot::jsonb ->> 'region'                            as region,
        null::text                                                      as region_lib,
        canteen_snapshot::jsonb ->> 'city_insee_code'                   as city_insee_code,
        null::integer                                                   as nbre_cantines_region,
        null::text                                                      as objectif_zone_geo,

        -- teledeclaration metadata
        teledeclaration_date,
        applicant_snapshot::jsonb ->> 'email'                           as applicant_email,

        -- declarations history (non disponible dans le snapshot)
        null::boolean                                                   as declaration_donnees_2021,
        null::boolean                                                   as declaration_donnees_2022,
        null::boolean                                                   as declaration_donnees_2023,
        null::boolean                                                   as declaration_donnees_2024,
        null::boolean                                                   as declaration_donnees_2025,

        -- appro — valeurs (bien typées dans diagnostics_raw)
        valeur_totale,
        valeur_bio,
        coalesce(valeur_egalim_agg::float,
            coalesce(valeur_bio::float, 0::float)
            + coalesce(valeur_siqo::float, 0::float)
            + coalesce(valeur_externalites_performance::float, 0::float)
            + coalesce(valeur_egalim_autres::float, 0::float)
        )                                                               as valeur_egalim_agg,
        coalesce(valeur_egalim_hors_bio_agg::float,
            coalesce(valeur_siqo::float, 0::float)
            + coalesce(valeur_externalites_performance::float, 0::float)
            + coalesce(valeur_egalim_autres::float, 0::float)
        )                                                               as valeur_egalim_hors_bio_agg,
        valeur_siqo,
        valeur_externalites_performance,
        valeur_egalim_autres,
        valeur_viandes_volailles,
        valeur_produits_de_la_mer,
        valeur_viandes_volailles_egalim,
        valeur_produits_de_la_mer_egalim,
        coalesce(valeur_viandes_volailles::float, 0::float)
            + coalesce(valeur_produits_de_la_mer::float, 0::float)                   as valeur_viandes_et_poissons,
        coalesce(valeur_viandes_volailles_egalim::float, 0::float)
            + coalesce(valeur_produits_de_la_mer_egalim::float, 0::float)            as valeur_viandes_et_poissons_egalim,

        -- origine France (toutes disponibles dans diagnostics_raw)
        valeur_viandes_volailles_france,
        valeur_charcuterie_france,
        valeur_produits_de_la_mer_france,
        valeur_fruits_et_legumes_france,
        valeur_produits_laitiers_france,
        valeur_boulangerie_france,
        valeur_boissons_france,
        valeur_autres_france,

        -- ratios (déjà calculés dans diagnostics_raw)
        pourcentage_bio,
        pourcentage_egalim,
        pourcentage_egalim_hors_bio,
        case
            when valeur_viandes_volailles::float > 0
            then valeur_viandes_volailles_egalim::float / valeur_viandes_volailles::float
        end                                                             as ratio_viandes_volailles_egalim,
        case
            when valeur_produits_de_la_mer::float > 0
            then valeur_produits_de_la_mer_egalim::float / valeur_produits_de_la_mer::float
        end                                                             as ratio_produits_de_la_mer_egalim,
        objectifs_egalim_atteints,

        -- diversification
        service_type,
        vegetarian_weekly_recurrence,
        vegetarian_menu_type,

        -- gaspillage
        has_waste_diagnostic,
        has_waste_plan,
        -- waste_actions est un array → extraction des actions individuelles par matching
        waste_actions::text ilike '%inscription%'                       as action_gaspi_inscription,
        waste_actions::text ilike '%sensibilisation%'                   as action_gaspi_sensibilisation,
        waste_actions::text ilike '%formation%'                         as action_gaspi_formation,
        waste_actions::text ilike '%distribution%'                      as action_gaspi_distribution,
        waste_actions::text ilike '%portions%'                          as action_gaspi_portions,
        waste_actions::text ilike '%reutilisation%'                     as action_gaspi_reutilisation

    from diagnostics
)

select * from renamed
