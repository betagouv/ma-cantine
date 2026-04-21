-- Télédéclarations soumises mais flagguées comme invalides (invalid_reason_list non vide).
-- Ces lignes sont exclues de mart_teledeclarations.
-- Cette vue permet de consulter et analyser les cas invalides séparément.

with source as (
    select * from {{ ref('stg_teledeclarations') }}
)

select
    teledeclaration_id,
    canteen_id,
    year,
    teledeclaration_date,
    diagnostic_type,
    cantine_name,
    siret,
    department,
    region,
    invalid_reason_list
from source
where invalid_reason_list is not null
  and invalid_reason_list::text != '[]'
