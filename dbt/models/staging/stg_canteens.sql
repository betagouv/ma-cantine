-- Cantines actives : les cantines supprimées (soft delete) sont exclues.
-- Le renommage des colonnes est fait dans stg_canteens_all.

select *
from {{ ref('stg_canteens_all') }}
where deletion_date is null
