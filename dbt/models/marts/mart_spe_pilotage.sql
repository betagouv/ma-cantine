-- Pilotage de la campagne de télédéclaration pour les RSPE (tableau de bord Metabase).
-- Une ligne par restaurant du périmètre État et par année de données, Armées incluses
-- (est_armees sépare le tableau commun du tableau Armées). n-1 = la ligne de l'année précédente.
-- Restaurant, tutelle et gestionnaires : état du jour (mart_cantines), pas celui figé dans la TD.
-- Les chiffres diffèrent donc du bilan SPE (mart_spe_bilan, figé au 29/04 n+1).
-- Indicateurs de la mesure 10 : repris de mart_teledeclarations, vides sans TD retenue.
-- Cibles et calendrier absents : les questions Metabase les lisent dans les tables téléversées
-- par la DGAL (le taux dépend des filtres du tableau).

with perimetre as (
    select * from {{ ref('int_spe_perimetre') }}
),

cantines as (
    select * from {{ ref('mart_cantines') }}
),

statuts as (
    select * from {{ ref('int_campagne_statut') }}
),

teledeclarations as (
    select * from {{ ref('mart_teledeclarations') }}
)

select
    -- restaurant
    c.id                                                        as canteen_id,
    c.siret,
    c.nom,
    c.groupe_id,
    g.nom                                                       as groupe_nom,
    c.type_production,
    c.type_gestion,
    c.nbre_repas_jour,
    c.nbre_repas_an,
    c.date_creation::date                                       as date_inscription,  -- UTC

    -- périmètre
    p.perimetre_key,
    p.perimetre_lib,
    p.pole_ministeriel,
    p.ordre_affichage,
    p.est_armees,

    -- secteur : les libellés ne contiennent pas de virgule (macro libelles_secteurs)
    c.secteurs,
    case when c.secteurs like '%,%' then 'Secteurs multiples' else c.secteurs end
                                                                as secteur,

    -- géographie
    c.code_insee_commune,
    c.libelle_commune,
    c.departement,
    c.departement_lib,
    c.region,
    c.region_lib,

    -- gestionnaires ; relance d'un satellite : les gestionnaires de son groupe
    c.adresses_gestionnaires,
    coalesce(g.adresses_gestionnaires, c.adresses_gestionnaires)
                                                                as adresses_relance,

    -- statut de l'année
    s.annee,
    s.statut_td,
    s.teledeclaration_id,
    s.date_teledeclaration,
    s.date_debut_saisie,
    s.date_modification_saisie,
    s.td_complete,
    s.td_generee_par_groupe,
    s.en_cours_via_groupe,
    s.td_deposee_non_retenue,

    -- mesure 10 : valeurs à réagréger (somme / somme dans Metabase)
    t.valeur_totale,
    t.valeur_bio_agg,
    t.valeur_egalim_agg,
    t.valeur_viandes_et_poissons,
    t.valeur_viandes_et_poissons_egalim,

    -- objectifs, seuils selon la zone (même règle que les atteint_* de mart_teledeclarations)
    t.atteint_bio,
    t.atteint_egalim,
    t.atteint_viandes_et_poissons_egalim,
    case
        when t.teledeclaration_id is null           then null
        when t.cantine_departement = '976'          then 'Mayotte : 5 % dont 2 % de bio'
        when t.cantine_objectif_zone_geo = 'droms'  then 'DROM : 20 % dont 5 % de bio'
        else                                             'Métropole : 50 % dont 20 % de bio'
    end                                                         as seuil_applicable,

    -- végétarien, diversification
    t.choix_multiple,
    t.atteint_vege_quotidien,
    t.td_volet_diversification_complet,

    -- gaspillage (filtre 10 à 500 g par couvert déjà appliqué dans mart_teledeclarations)
    t.gaspi_total_mass_kg,
    t.gaspi_meal_count,
    t.gaspi_g_par_couvert,
    -- niveau ADEME sur le ratio non arrondi, comme int_spe_waste_by_canteen
    case
        when coalesce(t.gaspi_meal_count, 0) = 0                            then null
        when t.gaspi_total_mass_kg * 1000 / t.gaspi_meal_count <= 47        then 'Niveau 3'
        when t.gaspi_total_mass_kg * 1000 / t.gaspi_meal_count <= 74        then 'Niveau 2'
        when t.gaspi_total_mass_kg * 1000 / t.gaspi_meal_count <= 95        then 'Niveau 1'
        else                                                                     'Non atteint'
    end                                                         as niveau_ademe

from perimetre as p
inner join cantines as c on p.canteen_id = c.id
left join cantines as g on c.groupe_id = g.id
inner join statuts as s on p.canteen_id = s.canteen_id
-- teledeclaration_id n'est pas unique (satellites déclarés par un groupe) : jointure sur la cantine aussi
left join teledeclarations as t
    on s.canteen_id = t.canteen_id and s.teledeclaration_id = t.teledeclaration_id
