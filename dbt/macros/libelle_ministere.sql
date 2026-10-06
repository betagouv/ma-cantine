{#
    Copie écrite à la main de `Canteen.Ministries` dans `data/models/canteen.py`.
    Ne jamais retirer un code : les anciennes TD l'utilisent encore.
    À remplacer par une source le jour où l'application exporte ces référentiels.

    Code ministère → libellé, comme `line_ministry` dans le RNC.
    Un code inconnu, vide ou nul donne `null`. Le test
    `tests/assert_codes_secteurs_et_ministeres_ont_un_libelle.sql` signale tout
    code présent dans les données mais absent d'ici.

    Deux libellés contiennent une virgule (Agriculture, Autorités indépendantes) :
    sans conséquence, la colonne ne porte qu'un seul ministère.
#}

{% macro libelle_ministere(col) %}
    (
        case {{ col }}
            when 'affaires_etrangeres'               then 'Affaires étrangères'
            when 'agriculture'                       then 'Agriculture, Alimentation et Forêts'
            when 'armee'                             then 'Armées'
            when 'territoires'                       then 'Cohésion des territoires - Relations avec les collectivités territoriales'
            when 'culture'                           then 'Culture'
            when 'economie'                          then 'Économie et finances'
            when 'jeunesse'                          then 'Éducation et Jeunesse'
            when 'enseignement_superieur'            then 'Enseignement supérieur et Recherche'
            when 'ecologie'                          then 'Environnement'
            when 'transformation'                    then 'Fonction Publiques'
            when 'interieur'                         then 'Intérieur et Outre-mer'
            -- `justice` : code de l'application. dbt l'éclate en `justice_pjj` / `justice_hors_pjj`
            -- (selon le secteur `social_pjj`) ; les trois donnent « Justice », comme le RNC.
            when 'justice'                           then 'Justice'
            when 'justice_pjj'                       then 'Justice'
            when 'justice_hors_pjj'                  then 'Justice'
            when 'mer'                               then 'Mer'
            when 'administration_territoriale'       then 'Préfecture - Administration Territoriale de l''État (ATE)'
            when 'autorites_independantes'           then 'Présidence de la république - Autorités indépendantes (AAI, API)'
            when 'premier_ministre'                  then 'Services du Premier Ministre'
            when 'sante'                             then 'Santé et Solidarités'
            when 'sport'                             then 'Sport'
            when 'travail'                           then 'Travail'
            -- codes retirés de l'application, encore présents dans d'anciennes TD
            when 'autre'                             then 'Autre'  -- retiré par #5291
        end
    )
{% endmacro %}
