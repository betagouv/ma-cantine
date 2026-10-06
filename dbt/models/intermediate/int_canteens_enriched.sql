with canteens as (
    select * from {{ ref('stg_canteens') }}
),

managers as (
    select * from {{ ref('stg_canteen_managers') }}
),

users as (
    select * from {{ ref('stg_users') }}
),

-- aggregate manager emails per canteen
canteen_managers_agg as (
    select
        m.canteen_id,
        string_agg(u.email, ', ' order by u.email) as manager_emails
    from managers as m
    inner join users as u on m.user_id = u.user_id
    group by m.canteen_id
),

-- cantines ayant au moins un gestionnaire, sans passer par la table des utilisateurs :
-- équivalent de `obj.managers.exists()` (RNC, `active_on_ma_cantine`)
canteens_with_manager as (
    select distinct canteen_id
    from managers
),

final as (
    select
        c.*,
        cma.manager_emails,
        -- `bool(line_ministry)` dans l'application (`Canteen.is_spe`) : la chaîne vide
        -- n'est pas un ministère. Un simple `is not null` en comptait 17 332 de trop.
        nullif(c.line_ministry, '') is not null      as is_spe,
        cwm.canteen_id is not null                   as has_manager
    from canteens as c
    left join canteen_managers_agg as cma on c.canteen_id = cma.canteen_id
    left join canteens_with_manager as cwm on c.canteen_id = cwm.canteen_id
)

select * from final
