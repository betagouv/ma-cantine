-- Restaurants du périmètre État : une ligne par cantine active.
-- Périmètre = cantines avec une administration de tutelle (tutelle actuelle, Justice éclatée en
-- justice_pjj / justice_hors_pjj), corrigé par les corrections téléversées par la DGAL dans
-- Metabase (SIRET exclus, ou forcés sur une tutelle ; une correction s'applique à toutes les
-- cantines qui partagent le SIRET).
-- Règle de la vue 3 du rapport SPE 2026 : les établissements publics (EPA, EPIC) de tutelle ATE
-- sont exclus.
-- Libellé, pôle ministériel et ordre d'affichage : référentiel des tutelles téléversé par la DGAL.

with cantines as (
    select * from {{ ref('mart_cantines') }}
),

corrections as (
    select * from {{ ref('stg_spe_corrections_perimetre') }}
),

tutelles as (
    select * from {{ ref('stg_spe_tutelles') }}
),

perimetre as (
    select
        c.id                                                    as canteen_id,
        coalesce(corr.ministere_force, c.ministere_tutelle)     as perimetre_key,
        corr.siret is not null                                  as est_corrige
    from cantines as c
    left join corrections as corr on c.siret = corr.siret
    where
        (c.ministere_tutelle is not null or corr.ministere_force is not null)
        and not coalesce(corr.exclure, false)
        -- libellé produit par la macro libelles_secteurs ; seul secteur de la cantine
        and not (
            coalesce(corr.ministere_force, c.ministere_tutelle) = 'administration_territoriale'
            and c.secteurs = 'Etablissements publics d''Etat (EPA ou EPIC)'
        )
)

select
    p.canteen_id,
    p.perimetre_key,
    t.perimetre_lib,
    t.pole_ministeriel,
    t.ordre_affichage,
    p.perimetre_key = 'armee'                                   as est_armees,
    p.est_corrige
from perimetre as p
left join tutelles as t on p.perimetre_key = t.perimetre_key
