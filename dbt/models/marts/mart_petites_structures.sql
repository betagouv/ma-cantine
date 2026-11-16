-- Expérimentation « Petites structures » : pilotage par les DRAAF (onglet du tableau Metabase 70).
-- Une ligne par cantine éligible, état du jour. Éligibilité : is_petite_structure, champ calculé
-- par l'application (data/models/canteen_petite_structure.py), jamais recalculé ici.
-- Données brutes : les 32 colonnes du modèle Metabase 964 (liste des cantines du tableau 70), mêmes
-- noms, types, valeurs et ordre, pour une liste identique et des filtres communs aux onglets.
-- Année de l'expérimentation : variable petites_structures_annee (2026 = achats 2026, campagne de
-- télédéclaration 2027).
-- TD de l'année : TD retenue dans mart_teledeclarations pour cette année (mêmes règles que
-- l'observatoire).
-- Activité OSA : au moins un achat actif daté de cette année ; saisie = date de création de l'achat,
-- à l'heure de Paris. Une cantine peut avoir saisi un achat de l'année avant le 1er janvier.
-- Inscription dans l'expérimentation et palier : à venir (fonctionnalité de l'application).

{% set annee = var('petites_structures_annee', 2026) %}

with cantines as (
    select * from {{ ref('mart_cantines') }}
    where is_petite_structure
),

-- une TD retenue par cantine et par année dans mart_teledeclarations
teledeclarations as (
    select
        canteen_id,
        date_teledeclaration,
        diagnostic_type
    from {{ ref('mart_teledeclarations') }}
    where annee = {{ annee }}
),

achats as (
    select
        canteen_id,
        min(creation_date)                  as date_premiere_saisie,
        max(creation_date)                  as date_derniere_saisie
    from {{ ref('stg_purchases') }}
    where purchase_date >= make_date({{ annee }}, 1, 1)
      and purchase_date < make_date({{ annee }} + 1, 1, 1)
    group by canteen_id
)

select
    -- données brutes : les 32 colonnes du modèle Metabase 964, dans le même ordre
    c.id,
    c.nom,
    c.siret,
    c.siren_unite_legale,
    c.code_insee_commune,
    c.libelle_commune,
    c.departement,
    c.departement_lib,
    c.region,
    c.region_lib,
    c.epci,
    c.epci_lib,
    c.pat_liste,
    c.pat_lib_liste,
    -- mart_cantines stocke l'heure UTC ; le modèle 964 donne la date à l'heure de Paris
    (c.date_creation at time zone 'UTC' at time zone 'Europe/Paris')::date
                                                                as date_creation,
    c.date_modification,
    c.nbre_repas_jour::float8                                   as nbre_repas_jour,
    c.nbre_repas_an::float8                                     as nbre_repas_an,
    case c.modele_economique
        when 'public'  then 'Public'
        when 'private' then 'Privé'
    end                                                         as modele_economique,
    {{ libelle_type_gestion('c.type_gestion') }}                as type_gestion,
    {{ libelle_type_production('c.type_production') }}          as type_production,
    c.siret_cuisine_centrale,
    c.ministere_tutelle_lib                                     as ministere_tutelle,
    c.secteurs                                                  as secteur,
    c.categories                                                as categorie,
    case when c.is_spe then 'Oui' else 'Non' end                as spe,
    c.adresses_gestionnaires,
    c.declaration_donnees_2021,
    c.declaration_donnees_2022,
    c.declaration_donnees_2023,
    c.declaration_donnees_2024,
    c.declaration_donnees_2025,

    -- code : valeur ciblée par le filtre « Modèle économique » du tableau 70
    c.modele_economique                                         as modele_economique_code,

    -- expérimentation
    {{ annee }}                                                 as annee_experimentation,

    -- télédéclaration de l'année de l'expérimentation
    case when t.canteen_id is not null then 'Oui' else 'Non' end
                                                                as td_annee,
    (t.date_teledeclaration at time zone 'Europe/Paris')::date  as date_teledeclaration,
    case t.diagnostic_type
        when 'SIMPLE'   then 'Simplifiée'
        when 'COMPLETE' then 'Détaillée'
    end                                                         as type_td,

    -- outil de suivi des achats (OSA), achats datés de l'année de l'expérimentation
    case when a.canteen_id is not null then 'Oui' else 'Non' end
                                                                as activite_osa,
    (a.date_premiere_saisie at time zone 'Europe/Paris')::date  as date_premiere_saisie_osa,
    (a.date_derniere_saisie at time zone 'Europe/Paris')::date  as date_derniere_saisie_osa

from cantines as c
left join teledeclarations as t on c.id = t.canteen_id
left join achats as a on c.id = a.canteen_id
