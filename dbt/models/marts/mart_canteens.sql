with source as (
    select * from {{ ref('int_canteens_enriched') }}
)

select
    canteen_id                                          as id,
    siret,
    siren_unite_legale,
    groupe_id,
    central_producer_siret                              as siret_cuisine_centrale,
    claimed_by_id,
    cantine_name                                        as nom,
    daily_meal_count                                    as nbre_repas_jour,
    yearly_meal_count                                   as nbre_repas_an,
    production_type                                     as type_production,
    management_type                                     as type_gestion,
    economic_model                                      as modele_economique,
    line_ministry                                       as ministere_tutelle,
    is_spe,
    array_to_string(
        array(select jsonb_array_elements_text(sector_list::jsonb)),
        ', '
    )                                                   as secteur,

    -- categorie dérivée du premier secteur
    case
        when (array(select jsonb_array_elements_text(sector_list::jsonb)))[1] like 'administration%' then 'Administration'
        when (array(select jsonb_array_elements_text(sector_list::jsonb)))[1] like 'entreprise%'     then 'Entreprise'
        when (array(select jsonb_array_elements_text(sector_list::jsonb)))[1] like 'education%'      then 'Enseignement'
        when (array(select jsonb_array_elements_text(sector_list::jsonb)))[1] like 'sante%'          then 'Santé'
        when (array(select jsonb_array_elements_text(sector_list::jsonb)))[1] like 'social%'         then 'Social / Médico-social'
        when (array(select jsonb_array_elements_text(sector_list::jsonb)))[1] like 'loisir%'         then 'Loisirs'
        when (array(select jsonb_array_elements_text(sector_list::jsonb)))[1] is not null            then 'Autres'
    end                                                 as categorie,
    city_insee_code                                     as code_insee_commune,
    city                                                as libelle_commune,
    postal_code                                         as code_postal,
    department                                          as departement,
    department_lib                                      as departement_lib,
    region,
    region_lib,
    epci,
    epci_lib,
    array_to_string(
        array(select jsonb_array_elements_text(pat_list::jsonb)),
        ', '
    )                                                   as pat_liste,
    array_to_string(
        array(select jsonb_array_elements_text(pat_lib_list::jsonb)),
        ', '
    )                                                   as pat_lib_liste,
    declaration_donnees_2021,
    declaration_donnees_2022,
    declaration_donnees_2023,
    declaration_donnees_2024,
    declaration_donnees_2025,
    manager_emails                                      as adresses_gestionnaires,
    creation_date::timestamp                            as date_creation,
    modification_date::date                             as date_modification,
    creation_source

from source
