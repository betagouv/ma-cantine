-- Population SPE inscrite : 1 ligne par (cantine, année)
--
-- Règle : une cantine est inscrite pour l'année N si elle existe le 29 avril de
-- l'année N+1 au soir, heure de Paris. La journée du 29/04 compte en entier, donc
-- une cantine créée le 29/04 est comptée et une cantine supprimée le 29/04 ne l'est pas.
-- creation_date et deletion_date sont des timestamptz stockés en UTC, d'où la
-- conversion explicite en heure de Paris.
--
-- Le line_ministry exposé est celui ACTUEL de la cantine (pas celui du snapshot de TD).
-- Les overrides propres à chaque mart (reclassements, exclusions de SIRET, exclusion
-- des EPA en ATE) ne sont PAS appliqués ici : ce modèle ne fournit que la population.

with canteens as (
    select
        canteen_id,
        siret,
        line_ministry,
        region,
        region_lib,
        sector_list,
        creation_date,
        deletion_date
    from {{ ref('stg_canteens_all') }}
    where line_ministry is not null
      and line_ministry != ''
),

spe_years as (
    select distinct year as annee
    from {{ ref('stg_teledeclarations') }}
    where line_ministry is not null
      and line_ministry != ''
)

select
    c.canteen_id,
    c.siret,
    y.annee,
    c.line_ministry,
    c.region,
    c.region_lib,
    c.sector_list
from canteens as c
cross join spe_years as y
where (c.creation_date at time zone 'Europe/Paris')::date <= make_date(y.annee::int + 1, 4, 29)
  and (
      c.deletion_date is null
      or (c.deletion_date at time zone 'Europe/Paris')::date > make_date(y.annee::int + 1, 4, 29)
  )
