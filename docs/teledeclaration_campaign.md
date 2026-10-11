# Campagne de télédéclaration

## Avant la campagne

* ajouter les dates dans [models/diagnostic_teledeclaration_dates.py](../data/models/diagnostic_teledeclaration_dates.py)
* ajouter les champs dans [models/diagnostic_teledeclaration_fields.py](../data/models/diagnostic_teledeclaration_fields.py)
* ajouter les groupes de champs dans [models/diagnostic_teledeclaration_field_groups.py](../data/models/diagnostic_teledeclaration_field_groups.py)
* ajouter le nouveau champ `Canteen.declaration_donnees_YEAR`
* modifier les endroits avec `# TODO teledeclaration_campaign`

## Pendant la campagne

### Exports

Modifier la fréquence des exports Metabase & Open Data, voir [macantine/schedules.py](../macantine/schedules.py)

### 1TD1Site

1. remplir les champs `invalid_warning_reason_list` &  `warning_reason_list`
    ```
    python manage.py diagnostic_fill_invalid_warning_reason_list --year YYYY --apply
    ```
2. créer les TD "fantômes" pour les cantines RSAT
    ```
    python manage.py teledeclaration_generate_1td1site --year YYYY --apply
    ```

TODO: temps réel au moment du save/cancel des TD

## Après la campagne

TODO (dbt)
