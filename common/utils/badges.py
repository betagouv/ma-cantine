def badges_for_queryset(teledeclaration_year_queryset):
    badge_querysets = {}
    if teledeclaration_year_queryset:
        # Avoid division by zero
        teledeclaration_year_queryset = teledeclaration_year_queryset.filter(valeur_totale__gt=0)
        # Calculate the percent of bio & egalim
        teledeclaration_year_queryset = teledeclaration_year_queryset.with_appro_percent_stats()
        badge_querysets["appro"] = teledeclaration_year_queryset.egalim_objectives_reached().distinct()
    return badge_querysets
