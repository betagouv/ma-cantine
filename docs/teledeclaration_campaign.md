# Campagne de télédéclaration

## Avant la campagne

### Définir les dates

voir [macantine/utils.py](../macantine/utils.py) et la constante `CAMPAIGN_DATES`

## Pendant la campagne

### Exports

Modifier la fréquence des exports Metabase & Open Data, voir [macantine/celery.py](../macantine/celery.py)

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
