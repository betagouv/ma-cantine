{#
    Regroupement SPE d'un code ministère (déjà éclaté en `justice_pjj` /
    `justice_hors_pjj`) : MTE, MEJSESR, Justice, Ministères sociaux, AAI, ATE.
    Les autres codes passent tels quels, y compris `''` et `null`.

    Copie exacte du `case` de `cantine_groupe_spe` dans `mart_teledeclarations`.
    Ce mart ne l'utilise pas encore : le jour où il le fait, les deux doivent
    rester identiques, faute de quoi `groupe_spe` (côté cantines) et
    `cantine_groupe_spe` (côté TD) divergeront.
#}

{% macro groupe_spe(col) %}
    (
        case
            when {{ col }} in ('ecologie', 'mer')                             then 'MTE'
            when {{ col }} in ('jeunesse', 'enseignement_superieur', 'sport') then 'MEJSESR'
            when {{ col }} in ('justice_hors_pjj', 'justice_pjj')             then 'Justice'
            when {{ col }} in ('travail', 'sante')                            then 'Ministères sociaux'
            when {{ col }} = 'autorites_independantes'                        then 'AAI'
            when {{ col }} = 'administration_territoriale'                    then 'ATE'
            else {{ col }}
        end
    )
{% endmacro %}
