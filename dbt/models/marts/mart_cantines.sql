-- Une ligne par cantine active (non supprimée).
-- Aligné sur trois références : le Registre national des cantines (RNC, open data,
-- `CanteenOpenDataSerializer`), l'observatoire et le rapport au parlement
-- (`mart_teledeclarations`). Les noms de colonnes reprennent ceux du modèle Metabase 964.

with source as (
    select * from {{ ref('int_canteens_enriched') }}
),

-- Chaîne vide → null sur les colonnes texte où les données en contiennent (relevé du
-- 05/10/2026). Une valeur vide n'est pas une valeur : sans ce nettoyage, un filtre
-- Metabase « est vide » ne la trouverait pas, et `''` se glisserait dans les listes de valeurs.
cantines as (
    select
        canteen_id,
        nullif(siret, '')                                   as siret,
        nullif(siren_unite_legale, '')                      as siren_unite_legale,
        groupe_id,
        nullif(central_producer_siret, '')                  as central_producer_siret,
        claimed_by_id,
        cantine_name,
        daily_meal_count,
        yearly_meal_count,
        nullif(production_type, '')                         as production_type,
        nullif(management_type, '')                         as management_type,
        nullif(economic_model, '')                          as economic_model,
        nullif(line_ministry, '')                           as line_ministry,
        is_spe,
        sector_list,
        nullif(city_insee_code, '')                         as city_insee_code,
        nullif(city, '')                                    as city,
        postal_code,
        department,
        department_lib,
        region,
        region_lib,
        epci,
        epci_lib,
        pat_list,
        pat_lib_list,
        declaration_donnees_2021,
        declaration_donnees_2022,
        declaration_donnees_2023,
        declaration_donnees_2024,
        declaration_donnees_2025,
        has_manager,
        manager_emails,
        creation_date,
        modification_date,
        creation_source
    from source
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

    -- ministère : code dbt (justice éclaté en justice_pjj / justice_hors_pjj),
    -- libellé (= `line_ministry` dans le RNC) et regroupement SPE
    line_ministry                                       as ministere_tutelle,
    {{ libelle_ministere('line_ministry') }}            as ministere_tutelle_lib,
    {{ groupe_spe('line_ministry') }}                   as groupe_spe,
    is_spe,

    -- secteurs et catégories : libellés séparés par `,`, liste complète
    -- (= `sector_list` dans le RNC ; `categories` = catégories de tous les secteurs)
    {{ libelles_secteurs('sector_list') }}              as secteurs,
    {{ libelles_categories('sector_list') }}            as categories,

    city_insee_code                                     as code_insee_commune,
    city                                                as libelle_commune,
    postal_code                                         as code_postal,
    department                                          as departement,
    department_lib                                      as departement_lib,
    region,
    region_lib,
    epci,
    epci_lib,
    nullif(
        array_to_string(array(select jsonb_array_elements_text(pat_list::jsonb)), ','),
        ''
    )                                                   as pat_liste,
    nullif(
        array_to_string(array(select jsonb_array_elements_text(pat_lib_list::jsonb)), ','),
        ''
    )                                                   as pat_lib_liste,
    declaration_donnees_2021,
    declaration_donnees_2022,
    declaration_donnees_2023,
    declaration_donnees_2024,
    declaration_donnees_2025,

    -- Périmètre du RNC : `Canteen.objects.publicly_visible()` (data/models/canteen.py:90)
    -- exclut les groupes et les cantines des armées. Le `exclude` de Django garde les
    -- cantines sans valeur, d'où le `coalesce` (sinon null != 'groupe' vaudrait null).
    coalesce(production_type, '') != 'groupe'
    and coalesce(line_ministry, '') != 'armee'          as est_perimetre_rnc,

    -- = `active_on_ma_cantine` dans le RNC (api/serializers/canteen.py:802). Le code ne
    -- vérifie que la présence d'un gestionnaire, malgré la description du schéma data.gouv.
    has_manager                                         as active_sur_ma_cantine,

    manager_emails                                      as adresses_gestionnaires,
    creation_date::timestamp                            as date_creation,
    modification_date::date                             as date_modification,
    creation_source

from cantines
