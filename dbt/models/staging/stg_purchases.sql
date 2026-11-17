-- Achats saisis dans l'outil de suivi des achats (OSA) : une ligne par achat actif.
-- Les achats supprimés (suppression logique, deletion_date renseignée) sont exclus.

with source as (
    select * from {{ source('datawarehouse', 'purchases_raw') }}
),

renamed as (
    select
        id                                  as purchase_id,
        canteen_id,
        date                                as purchase_date,
        creation_date,
        modification_date,
        creation_source
    from source
    where deletion_date is null
)

select * from renamed
