{#
    Copie écrite à la main de `data/models/sector.py`.
    Ne jamais retirer un code : les anciennes TD l'utilisent encore.
    À remplacer par une source le jour où l'application exporte ces référentiels.

    Tableau JSON de codes secteur → libellés des catégories, séparés par `,`
    sans espace, sans doublon, dans l'ordre de première apparition.
    Même résultat que `get_category_lib_list_from_sector_list` (`sector.py:197`),
    y compris sur ses deux particularités :
      - les codes vides sont ignorés ;
      - un code inconnu donne « Autres » (branche `else` de
        `get_sector_category_from_sector`), alors que `libelles_secteurs`
        l'ignore. L'asymétrie est celle de l'application.
    `null` si la liste est vide ou absente.

    À ne pas confondre avec `cantine_categorie` de `mart_teledeclarations`, qui ne
    garde que la catégorie du premier secteur (règle propre à dbt).

    Les codes sont lus dans `referentiel_secteurs()`.
#}

{% macro libelles_categories(json_col) %}
    (
        select string_agg(categories.libelle_categorie, ',' order by categories.premiere_position)
        from (
            select
                coalesce(referentiel_secteurs.libelle_categorie, 'Autres') as libelle_categorie,
                min(elements.position)                                       as premiere_position
            from jsonb_array_elements_text(({{ json_col }})::jsonb) with ordinality as elements (code, position)
            left join {{ referentiel_secteurs() }}
                on elements.code = referentiel_secteurs.code
            where elements.code != ''
            group by coalesce(referentiel_secteurs.libelle_categorie, 'Autres')
        ) as categories
    )
{% endmacro %}
