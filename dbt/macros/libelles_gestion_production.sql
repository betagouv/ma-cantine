{#
    Copies écrites à la main de `Canteen.ManagementType` et `Canteen.ProductionType` dans
    `data/models/canteen.py`. Un code inconnu, vide ou nul donne `null`.
#}

{% macro libelle_type_gestion(col) %}
    (
        case {{ col }}
            when 'direct'                   then 'Directe'
            when 'conceded'                 then 'Concédée'
        end
    )
{% endmacro %}

{% macro libelle_type_production(col) %}
    (
        case {{ col }}
            when 'groupe'                   then 'Groupe'
            when 'central'                  then 'Cuisine centrale'
            when 'central_serving'          then 'Cuisine centrale et site'
            when 'site'                     then 'Restaurant avec cuisine sur place'
            when 'site_cooked_elsewhere'    then 'Restaurant satellite'
        end
    )
{% endmacro %}
