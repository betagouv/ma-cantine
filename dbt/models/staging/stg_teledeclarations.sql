-- Source actuelle : table teledeclarations (export ETL manuel, mise à jour chaque nuit)
-- Source future   : diagnostics_raw (filtré sur teledeclaration_id IS NOT NULL)
-- Seul ce fichier sera modifié lors du changement de source.
-- Les noms de colonnes ici sont alignés sur diagnostics_raw pour minimiser les changements.

with source as (
    select * from {{ source('datawarehouse', 'teledeclarations') }}
),

renamed as (
    select
        -- identifiers
        id                                                          as teledeclaration_id,
        canteen_id,
        year,
        version                                                     as teledeclaration_version,
        creation_source,
        diagnostic_type,

        -- canteen info (dénormalisé ici, viendra d'un join stg_canteens dans diagnostics_raw)
        name                                                        as cantine_name,
        siret,
        siren_unite_legale,
        daily_meal_count,
        yearly_meal_count,
        management_type,
        production_type,
        modele_economique                                           as economic_model,
        secteur,
        categorie,
        satellite_canteens_count,
        line_ministry,
        spe,
        is_filled,
        genere_par_cuisine_centrale,

        -- geo
        departement                                                 as department,
        lib_departement                                             as department_lib,
        region,
        lib_region                                                  as region_lib,
        code_insee_commune                                          as city_insee_code,
        nbre_cantines_region,
        objectif_zone_geo,

        -- teledeclaration metadata
        creation_date::date                                         as teledeclaration_date,
        email                                                       as applicant_email,

        -- declarations history
        declaration_donnees_2021,
        declaration_donnees_2022,
        declaration_donnees_2023,
        declaration_donnees_2024,
        declaration_donnees_2025,

        -- appro — valeurs (cast text → float pour les colonnes mal typées)
        nullif(valeur_totale, '')::float                            as valeur_totale,
        valeur_bio,
        valeur_somme_egalim_avec_bio                                as valeur_egalim_agg,
        valeur_somme_egalim_hors_bio                                as valeur_egalim_hors_bio_agg,
        valeur_siqo,
        valeur_externalites_performance,
        valeur_egalim_autres,
        nullif(valeur_viandes_volailles, '')::float                 as valeur_viandes_volailles,
        nullif(valeur_produits_de_la_mer, '')::float                as valeur_produits_de_la_mer,
        nullif(valeur_viandes_volailles_egalim, '')::float          as valeur_viandes_volailles_egalim,
        nullif(valeur_produits_de_la_mer_egalim, '')::float         as valeur_produits_de_la_mer_egalim,
        valeur_viandes_volailles_produits_de_la_mer                 as valeur_viandes_et_poissons,
        valeur_viandes_volailles_produits_de_la_mer_egalim          as valeur_viandes_et_poissons_egalim,

        -- origine France
        -- valeur_viandes_volailles_france présente mais mal typée
        nullif(valeur_viandes_volailles_france, '')::float          as valeur_viandes_volailles_france,
        -- colonnes absentes de la table actuelle, disponibles dans diagnostics_raw
        null::float                                                 as valeur_charcuterie_france,
        null::float                                                 as valeur_produits_de_la_mer_france,
        null::float                                                 as valeur_fruits_et_legumes_france,
        null::float                                                 as valeur_produits_laitiers_france,
        null::float                                                 as valeur_boulangerie_france,
        null::float                                                 as valeur_boissons_france,
        null::float                                                 as valeur_autres_france,

        -- ratios (cast text → float)
        nullif(ratio_bio, '')::float                                as pourcentage_bio,
        nullif(ratio_egalim_avec_bio, '')::float                    as pourcentage_egalim,
        nullif(ratio_egalim_sans_bio, '')::float                    as pourcentage_egalim_hors_bio,
        ratio_viandes_volailles_egalim,
        ratio_produits_de_la_mer_egalim,
        null::boolean                                               as objectifs_egalim_atteints,

        -- diversification
        service_type,
        vegetarian_weekly_recurrence,
        vegetarian_menu_type,

        -- gaspillage (noms différents dans diagnostics_raw : has_waste_diagnostic, has_waste_plan, waste_actions)
        diag_gaspi                                                  as has_waste_diagnostic,
        plan_action_gaspi                                           as has_waste_plan,
        action_gaspi_inscription,
        action_gaspi_sensibilisation,
        action_gaspi_formation,
        action_gaspi_distribution,
        action_gaspi_portions,
        action_gaspi_reutilisation

    from source
)

select * from renamed
