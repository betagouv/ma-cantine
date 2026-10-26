-- Une ligne par bilan créé via l'API par un logiciel connu (application OAuth2 renseignée).
-- Lu dans les bilans et non dans EventLog : la requête de création ne donne pas l'identifiant
-- du bilan créé, donc pas sa télédéclaration.
-- jour_creation = date de création à l'heure de Paris.

select
    d.diagnostic_id,
    d.canteen_id,
    d.year                                                  as annee_bilan,
    d.creation_date                                         as date_creation,
    (d.creation_date at time zone 'Europe/Paris')::date     as jour_creation,
    d.creation_source_api_oauth2_application_id             as application_id,
    a.application_nom,
    a.editeur,
    a.est_test,
    d.creation_user_id                                      as user_id,
    d.status                                                as statut,
    d.status = 'SUBMITTED'                                  as est_teledeclare,
    d.teledeclaration_date                                  as date_teledeclaration
from {{ ref('stg_diagnostics') }} as d
left join {{ ref('int_api_applications') }} as a
    on d.creation_source_api_oauth2_application_id = a.application_id
where d.creation_source = 'API'
  and d.creation_source_api_oauth2_application_id is not null
  -- un bilan de satellite généré depuis celui du groupe copie ses champs de création
  and not coalesce(d.generated_from_groupe_diagnostic, false)
