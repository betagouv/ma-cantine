{#
    Copie écrite à la main de `data/models/sector.py`.
    Ne jamais retirer un code : les anciennes TD l'utilisent encore.
    À remplacer par une source le jour où l'application exporte ces référentiels.

    Tableau JSON de codes secteur → libellés au format du RNC (`sector_list`) :
    libellés séparés par `,` sans espace, dans l'ordre où ils sont stockés.
    Même résultat que `get_sector_lib_list_from_sector_list` (`sector.py`) :
    les codes inconnus sont ignorés. `null` si la liste est vide ou absente.

    Les libellés et non les codes : `administration_administratif` est contenu dans
    `administration_administratif_des_collectivites`, donc un filtre Metabase
    « contient » sur les codes se tromperait. Aucun des 26 libellés n'est contenu
    dans un autre, et aucun ne contient de virgule.

    Les codes sont lus dans `referentiel_secteurs()`.
#}

{% macro libelles_secteurs(json_col) %}
    (
        select string_agg(referentiel_secteurs.libelle, ',' order by elements.position)
        from jsonb_array_elements_text(({{ json_col }})::jsonb) with ordinality as elements (code, position)
        inner join {{ referentiel_secteurs() }}
            on elements.code = referentiel_secteurs.code
    )
{% endmacro %}
