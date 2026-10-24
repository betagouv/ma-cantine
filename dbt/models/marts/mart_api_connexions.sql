-- Une ligne par (application, utilisateur, jour de connexion).
-- Connexion = jeton obtenu ou renouvelé par un logiciel (int_api_connexions).
-- jour = date de la connexion à l'heure de Paris.

with connexions_par_jour as (
    select
        (date_connexion at time zone 'Europe/Paris')::date  as jour,
        application_id,
        user_id,
        count(*)                                            as nb_jetons,
        min(date_connexion)                                 as premiere_connexion_du_jour
    from {{ ref('int_api_connexions') }}
    group by 1, application_id, user_id
)

select
    c.jour,
    c.application_id,
    a.application_nom,
    a.editeur,
    a.est_test,
    c.user_id,
    coalesce(u.is_staff or u.is_dev, false)                 as utilisateur_est_equipe,
    c.nb_jetons,
    c.premiere_connexion_du_jour
from connexions_par_jour as c
left join {{ ref('int_api_applications') }} as a on c.application_id = a.application_id
left join {{ ref('stg_users') }} as u on c.user_id = u.user_id
