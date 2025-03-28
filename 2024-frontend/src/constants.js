export default Object.freeze({
  DiagnosticImportLevels: [
    {
      key: "SIMPLE",
      urlSlug: "cantines-et-diagnostics-simples",
      title: "Importer des bilans simples",
      help:
        "Vous voulez créer ou mettre à jour des bilans. Vous connaissez que les valeurs totales de vos achats bio et de qualité",
    },
    {
      key: "COMPLETE",
      urlSlug: "cantines-et-diagnostics-complets",
      title: "Importer des bilans détaillés",
      help:
        "Vous voulez créer ou mettre à jour des bilans. Vous connaissez les labels et les familles de produits de vos achats",
    },
  ],
  CentralKitchenImportLevels: [
    {
      key: "CC_SIMPLE",
      urlSlug: "cuisine-centrale-diagnostics-simples",
      title: "Importer des bilans simples pour des livreurs de repas",
      help:
        "Vous ne connaissez pas les données par cantine satellite, que par livreur de repas. Vous connaissez que les valeurs totales de vos achats bio et de qualité",
    },
    {
      key: "CC_COMPLETE",
      urlSlug: "cuisine-centrale-diagnostics-complets",
      title: "Importer des bilans détaillés pour des livreurs de repas",
      help:
        "Vous ne connaissez pas les données par cantine satellite, que par livreur de repas. Vous connaissez les labels et les familles de produits de vos achats",
    },
  ],
  WasteMeasurement: {
    daysInPeriod: {
      title: "Période de mesure de mes déchets alimentaires",
    },
    mealCount: {
      title: "Nombre de couverts sur la période",
    },
    totalMass: {
      title: "Masse totale des déchets alimentaires relevée sur la période de mesure",
    },
    preparation: {
      title: "Déchets alimentaires issus de la préparation",
    },
    unserved: {
      title: "Denrées présentées aux convives mais non servies",
    },
    leftovers: {
      title: "Restes assiettes",
    },
  },
})
