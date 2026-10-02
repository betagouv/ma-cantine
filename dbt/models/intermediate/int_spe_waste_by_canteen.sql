-- Gaspillage alimentaire SPE au niveau cantine : 1 ligne par (canteen_id, annee)
--
-- Socle commun à tous les marts SPE (Vue 1 via int_spe_waste, Vue 2 via mart_spe_bilan_ate) :
-- un seul calcul par cantine, donc un seul jeu de filtres.
--   - restriction aux cantines ayant une TD valide l'année concernée ;
--   - mêmes exclusions que les marts SPE (EPA en ATE, SIRETs exclus, transformation) ;
--   - filtre qualité : ratio entre 10 et 500 g par couvert (écarte notamment les cantines
--     qui déclarent des couverts sans masse, qui gonflaient le dénominateur) ;
--   - niveau ADEME calculé par cantine, avant toute agrégation.
--
-- line_ministry, region et secteur viennent du snapshot de TD (stg_teledeclarations),
-- pour rester cohérents avec les statistiques TD de la même ligne de mart.

with waste as (
    select * from {{ ref('stg_waste_measurements') }}
),

canteens as (
    select distinct
        canteen_id,
        year,
        siret,
        line_ministry,
        region,
        secteur
    from {{ ref('stg_teledeclarations') }}
    where line_ministry is not null
      and line_ministry != ''
      and production_type not in ('groupe', 'central', 'central_serving')
      and teledeclaration_mode != 'SATELLITE_WITHOUT_APPRO'
      and (invalid_reason_list is null or invalid_reason_list::text = '[]')
      and (secteur != 'administration_etablissement_public' or line_ministry != 'administration_territoriale')
      -- coalesce indispensable : `null not in (...)` vaut null, donc un `not in` nu
      -- écarterait silencieusement toutes les cantines sans SIRET (38 dans le
      -- périmètre SPE en 2025, dont 8 avec une mesure de gaspillage)
      and coalesce(siret, '') not in ('21400312100172', '26760171400087')
      and line_ministry != 'transformation'
)

select
    w.annee,
    w.canteen_id,
    c.siret,
    c.line_ministry,
    c.region,
    c.secteur,
    sum(w.total_mass)                                               as total_mass_kg,
    sum(w.meal_count)                                               as total_meal_count,
    round(
        (sum(w.total_mass) * 1000 / nullif(sum(w.meal_count), 0))::numeric, 1
    )                                                               as gaspi_g_par_couvert,
    case
        when sum(w.meal_count) is null or sum(w.meal_count) = 0    then null
        when sum(w.total_mass) * 1000 / sum(w.meal_count) <= 47    then 'Niveau 3'
        when sum(w.total_mass) * 1000 / sum(w.meal_count) <= 74    then 'Niveau 2'
        when sum(w.total_mass) * 1000 / sum(w.meal_count) <= 95    then 'Niveau 1'
        else                                                             'Non atteint'
    end                                                             as niveau_ademe
from waste as w
inner join canteens as c
    on w.canteen_id = c.canteen_id
    and w.annee = c.year
group by w.annee, w.canteen_id, c.siret, c.line_ministry, c.region, c.secteur
having
    sum(w.meal_count) > 0
    and (sum(w.total_mass) * 1000 / sum(w.meal_count)) >= 10
    and (sum(w.total_mass) * 1000 / sum(w.meal_count)) <= 500
