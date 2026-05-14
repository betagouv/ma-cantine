with source as (
    select * from {{ source('datawarehouse', 'users_raw') }}
),

renamed as (
    select
        id                          as user_id,
        username,
        email,
        first_name,
        last_name,
        is_active,
        is_staff,
        is_superuser,
        is_dev,
        is_elected_official,
        created_with_mcp,
        mcp_id,
        mcp_organizations,
        avatar,
        job,
        other_job_description,
        phone_number,
        source,
        other_source_description,
        law_awareness,
        departments,
        email_confirmed,
        opt_out_reminder_emails,
        date_joined,
        last_login,
        data
        --creation_mtm_source,
        --creation_mtm_campaign,
        --creation_mtm_medium,
        -- brevo_last_update_date,
        -- brevo_is_deleted

    from source
)

select * from renamed