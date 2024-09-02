export default Object.freeze({
  DiagnosticImportLevels: [
    {
      key: "NONE",
      urlSlug: "cantines-seules",
      title: "Créer des cantines",
      help: "Vous voulez créer ou mettre à jour des cantines",
    },
    {
      key: "SIMPLE",
      urlSlug: "cantines-et-diagnostics-simples",
      title: "Importer des bilan simples",
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
      title: "Importer des bilans détaillés pour des livreurs de repas",
      help:
        "Vous ne connaissez pas les données par cantine satellite, que par livreur de repas. Vous connaissez les valeurs totaux, bio, et de qualité et durable",
    },
    {
      key: "CC_COMPLETE",
      urlSlug: "cuisine-centrale-diagnostics-complets",
      title: "Importer des bilans détaillés pour des livreurs de repas",
      help:
        "Vous ne connaissez pas les données par cantine satellite, que par livreur de repas. Vous connaissez les labels et les familles de produits de vos achats",
    },
  ],
})
