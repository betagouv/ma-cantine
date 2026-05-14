with source as (
    select * from {{ source('datawarehouse', 'canteens_raw') }}
),

renamed as (
    select
        id                          as canteen_id,
        siret,
        siren_unite_legale,
        groupe_id,
        creation_date,
        deletion_date,
        modification_date,
        creation_source,
        import_source,
        central_producer_siret,
        claimed_by_id,
        name                        as cantine_name,
        daily_meal_count,
        yearly_meal_count,
        production_type,
        management_type,
        economic_model,
        case
            when line_ministry = 'justice'
                 and sector_list::jsonb @> '["social_pjj"]'
            then 'justice_pjj'
            when line_ministry = 'justice'
            then 'justice_hors_pjj'
            else line_ministry
        end                 as line_ministry,
        sector_list,
        -- geo
        city_insee_code,
        city,
        postal_code,
        department,
        department_lib,
        region,
        region_lib,
        epci,
        epci_lib,
        pat_list,
        pat_lib_list,

        -- status
        is_filled,
        has_been_claimed,

        -- teledeclarations
        declaration_donnees_2021,
        declaration_donnees_2022,
        declaration_donnees_2023,
        declaration_donnees_2024,
        declaration_donnees_2025,

        redacted_appro_years,
        publication_comments,
        quality_comments,
        waste_comments,
        diversification_comments,
        plastics_comments,
        information_comments,
        reservation_expe_participant,
        vegetarian_expe_participant,

        -- automated tasks
        siret_inconnu,
        siret_etat_administratif,
        geolocation_bot_attempts
        --creation_mtm_source,
        --creation_mtm_campaign,
        --creation_mtm_medium,
        --logo

    from source
)

select *
from renamed
where deletion_date is null