# Tracking avec matomo

| catégorie | action | nom | valeur | description | depuis où |
| --- | --- | --- | --- | --- | --- |
| inquiry | send | functionalityQuestion / demo / bug / egalim / other | | Les demandes envoyées | Page contact / Page dév / Page partenaires |
| inquiry | send | import-purchases-success | | L'import d'achats a reussi | Page d'import d'achats |
| inquiry | send | import-diagnostics-success | | L'import de diagnostics a reussi | Page d'import de diagnostics |
| data-warning | teledeclare / go-back | td-satellite-count-is-1 | | Message affiché quand une CC déclare un seul satellite | Preview de télédéclaration (page diagnostic / page actions) |
| data-warning | teledeclare / go-back | td-satellite-count-over-200 | # satellites | Message affiché quand une CC déclare plus de 200 satellites | Preview de télédéclaration (page diagnostic / page actions) |
| data-warning | teledeclare / go-back | td-meal-cost-over-10 | Coût calculé | Message affiché quand le coût denrées dépasse 10 euro | Preview de télédéclaration (page diagnostic / page actions) |
| data-warning | teledeclare / go-back | td-meal-cost-under-0.1 | Coût calculé | Message affiché quand le coût denrées est moins de 0.1 euro | Preview de télédéclaration (page diagnostic / page actions) |
| data-warning | teledeclare / go-back | td-days-open-over-365 | # de jours | Message affiché quand le nombre de jours de service est supérieur à 365 | Preview de télédéclaration (page diagnostic / page actions) |
| data-warning | teledeclare / go-back | td-days-open-under-50 | # de jours | Message affiché quand le nombre de jours de service est inférieur à 50 | Preview de télédéclaration (page diagnostic / page actions) |
| canteen | modification | technical-control-cancel/technical-control-save | | Garde-fous de modification d'une cantine (CC avec un satellite ou plus de 250) | Page modification cantine |
| message | send | canteen-not-found-email | | Quelqu'un a envoyé un demande pour trouver une cantine | Page nos cantines / Page d'une cantine publiée |
| form | submit | poster-generator | | Quelqu'un a téléchargé une affiche | Page generateur affichage |
