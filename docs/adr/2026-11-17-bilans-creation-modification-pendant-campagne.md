# ADR : Bilans : création & modification uniquement pendant la campagne (imports & API v2)

- Statut : acceptée
- Date : 17/11/2026 (merge sur `staging`, en prod le même jour avec la release 2026.62.0). Imports : en prod avec les releases 2026.58.0 (04/11/2026) et 2026.59.0 (10/11/2026).
- PRs : #7471, #7472, #7490, #7557, #7558 (imports), #7554, #7555 (année de la campagne en cours), #7664, #7665 (API v2)

## Contexte

- Un bilan de l'année N est télédéclaré pendant la campagne du début de l'année N+1 (`CAMPAIGN_DATES`), par exemple les bilans 2026 début 2027.
- Jusque-là, les imports et l'API permettaient de créer ou de modifier des bilans toute l'année, et pour n'importe quelle année autorisée par le modèle.
- L'API v2 des bilans s'ouvre aux éditeurs (#7577) : les règles doivent être fixées avant, pour ne pas la casser ensuite.

## Décision

1. **Imports de bilans (simple & détaillé)** : uniquement pendant la campagne (télédéclaration ou correction) (#7472). Hors campagne, le fichier entier est refusé avec une seule erreur (#7557), et les pages d'import de bilans redirigent vers la page des imports, qui indique que l'import n'est possible que pendant la campagne (#7490).
2. **Imports, format 2026** : plus de colonne `année_bilan` (#7558). Les bilans importés sont ceux de l'année de la campagne en cours (`get_current_campaign_year()`).
3. **API v2, création (POST)** : uniquement pendant la campagne (#7664). Le champ `year` n'est plus demandé : c'est l'année de la campagne en cours. Un `year` envoyé est ignoré.
4. **API v2, modification (PATCH) du bilan & de ses 5 volets** : uniquement pendant la campagne, et uniquement pour le bilan de l'année de la campagne en cours (#7665). La lecture (GET) reste possible toute l'année.
5. Briques communes :
   - `get_current_campaign_year()` : l'année précédente, ou `TELEDECLARATION_YEAR_OVERRIDE` (#7555) ;
   - `validate_is_in_teledeclaration_or_correction_period(action)` : un message d'erreur par action (`import`, `create`, `update`…) ;
   - les settings `TELEDECLARATION_*_OVERRIDE` & `CORRECTION_*_OVERRIDE` pour ouvrir la campagne dans les environnements non-prod.

## Ce qui ne change pas

- L'interface de la plateforme.
- La règle du modèle (`validate_year_and_can_edit`) : années autorisées = année de la campagne en cours et la suivante (#7554). Une fois la campagne terminée, un bilan en brouillon n'est plus modifiable ; après la période de correction, plus aucun bilan ne l'est.
- Un bilan télédéclaré : seuls les volets additionnels (hors approvisionnement) restent modifiables, et uniquement pendant la campagne (#7506, #7576).

## Conséquences

- En prod, pas d'import de bilans ni d'écriture via l'API v2 entre la fin de la période de correction (vers mai) et l'ouverture de la campagne suivante (janvier).
- API v2 : hors campagne, ou pour un bilan d'une autre année, erreur 400 avec un message explicite.
- Le tunnel de télédéclaration (front 2024) utilise les endpoints v2 des volets, mais n'est déjà accessible que pendant la campagne.
- Démo & staging : pour tester, ouvrir la campagne avec les settings `*_OVERRIDE`.

## Écarts restants

À traiter dans une PR séparée, ou plus tard (l'année prochaine) :

1. **Imports, format 2025** : l'année de chaque ligne (`année_bilan`) n'est vérifiée que par la validation du modèle, qui accepte l'année de la campagne en cours et la suivante. Pendant la campagne 2026 (début 2027), un fichier au format 2025 peut donc encore créer ou modifier des bilans 2027. À corriger dans une PR séparée, ou à la suppression du format 2025.
2. **API v1** : création & modification toujours possibles toute l'année (dans les limites de la règle du modèle). Elle est déjà utilisée par des éditeurs : impossible de la changer sans les casser. À revoir plus tard (l'année prochaine, ou à la dépréciation de la v1 au profit de la v2).
