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
    from managers m
    inner join users u on u.user_id = m.user_id
    group by m.canteen_id
),

final as (
    select
        c.*,
        cma.manager_emails,
        c.line_ministry is not null                   as is_spe
    from canteens c
    left join canteen_managers_agg cma on cma.canteen_id = c.canteen_id
)

select * from final
