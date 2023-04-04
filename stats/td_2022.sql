with
starting_data as (
    select (value_bio_ht)/value_total_ht * 100 as p_bio, id
    from data_diagnostic
    where value_total_ht > 0
),
    td_2022
    as (
        SELECT * from data_teledeclaration
        where year = 2022 and status = 'SUBMITTED'
    ),
    td_values
    as (
        SELECT
            id,
            canteen_id,
            CAST(declared_data -> 'teledeclaration' ->> 'value_total_ht' as float) as total,
            CAST(declared_data -> 'teledeclaration' ->> 'value_bio_ht' as float) as bio,
            CAST(declared_data -> 'teledeclaration' ->> 'value_sustainable_ht' as float) as sustainable,
            CAST(declared_data -> 'teledeclaration' ->> 'value_externality_performance_ht' as float) as externality,
            CAST(declared_data -> 'teledeclaration' ->> 'value_egalim_others_ht' as float) as other_egalim,
declared_data -> 'teledeclaration' ->> 'diagnostic_type' as diagnostic_type
        from td_2022
    ),
    no_null_bio
    as (
        SELECT * from td_values
        where bio is not null
    ),
    some_non_null_egalim_hors_bio
    as (
        SELECT * from td_values
        where sustainable is not null or externality is not null or other_egalim is not null
    ),
    sector_td_2022
    as (
        SELECT *
        from
            data_canteen_sectors
            left join data_sector on data_canteen_sectors.sector_id = data_sector.id
            left join td_values on data_canteen_sectors.canteen_id = td_values.canteen_id
        where
            td_values.id is not null and
            bio is not null and
            (sustainable is not null or externality is not null or other_egalim is not null)
    )
