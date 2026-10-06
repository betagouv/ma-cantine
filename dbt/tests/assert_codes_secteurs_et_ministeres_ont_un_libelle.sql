-- Aucun code secteur ni ministère présent dans les données ne doit être sans libellé.
--
-- Une ligne renvoyée = un code connu de l'application mais absent des macros dbt
-- (`referentiel_secteurs`, `libelle_ministere`) : c'est le signe qu'un code a été ajouté
-- dans `data/models/sector.py` ou dans `Canteen.Ministries` sans être reporté dans dbt.
-- Correction : ajouter le code et son libellé dans la macro concernée. Ne jamais retirer
-- un code des macros, même s'il disparaît de l'application : les anciennes TD l'utilisent.
--
-- Lit les sources brutes pour tout couvrir : les cantines supprimées comprises
-- (`canteens_raw`) et toutes les TD, avec leurs codes figés (`canteen_snapshot`).
-- Le ministère est lu en code applicatif (`justice` non éclaté), que la macro connaît aussi.

with codes_secteurs as (
    select
        'cantines'                                          as cote,
        jsonb_array_elements_text(sector_list)              as code
    from {{ source('datawarehouse', 'canteens_raw') }}
    where jsonb_typeof(sector_list) = 'array'

    union all

    select
        'teledeclarations'                                              as cote,
        jsonb_array_elements_text(canteen_snapshot -> 'sector_list')    as code
    from {{ source('datawarehouse', 'diagnostics_raw') }}
    where jsonb_typeof(canteen_snapshot -> 'sector_list') = 'array'
),

codes_ministeres as (
    select
        'cantines'                                          as cote,
        line_ministry                                       as code
    from {{ source('datawarehouse', 'canteens_raw') }}

    union all

    select
        'teledeclarations'                                  as cote,
        canteen_snapshot ->> 'line_ministry'                as code
    from {{ source('datawarehouse', 'diagnostics_raw') }}
    where canteen_snapshot is not null
)

select
    'secteur'                                               as type_code,
    codes_secteurs.cote,
    codes_secteurs.code,
    count(*)                                                as nb_lignes
from codes_secteurs
left join {{ referentiel_secteurs() }}
    on codes_secteurs.code = referentiel_secteurs.code
where codes_secteurs.code != ''
  and referentiel_secteurs.code is null
group by codes_secteurs.cote, codes_secteurs.code

union all

select
    'ministere'                                             as type_code,
    codes_ministeres.cote,
    codes_ministeres.code,
    count(*)                                                as nb_lignes
from codes_ministeres
where codes_ministeres.code != ''
  and {{ libelle_ministere('codes_ministeres.code') }} is null
group by codes_ministeres.cote, codes_ministeres.code
