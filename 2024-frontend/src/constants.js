export default Object.freeze({
  DiagnosticImportLevels: [
    {
      key: "NONE",
      urlSlug: "cantines-seules",
      title: "Importer des cantines sans bilan",
      label: "Sans bilan",
      help: "Vous voulez importer des cantines sans données d'approvisionnement",
      icon: "$community-fill",
    },
    {
      key: "SIMPLE",
      urlSlug: "cantines-et-diagnostics-simples",
      title: "Importer des cantines et bilans simples",
      label: "Diagnostic simple",
      help: "Vous connaissez les valeurs totales de vos achats bio et de qualité",
      icon: "$bar-chart-box-fill",
    },
    {
      key: "COMPLETE",
      urlSlug: "cantines-et-diagnostics-complets",
      title: "Importer des cantines et bilans complets",
      label: "Diagnostic complet",
      help: "Vous connaissez les labels et les familles de produits de vos achats",
      icon: "$checkbox-circle-fill",
    },
  ],
  CentralKitchenImportLevels: [
    {
      key: "CC_SIMPLE",
      urlSlug: "cuisine-centrale-diagnostics-simples",
      title: "Mettre à jour vos satellites et renseigner des bilans simples",
      description:
        "Ce type de fichier vous permet de renseigner vos données d'approvisionnement simplifiées au niveau de la cuisine centrale et de lister vos cantines satellites seulement avec leurs données d'établissement. Les données d'approvisionnement restent donc seulement nécessaires pour les cuisines centrales.",
      label: "Cuisine centrale avec bilan simple",
      help:
        "Vous voulez renseigner vos satellites et vous connaissez les valeurs totaux, bio, et de qualité et durable",
      icon: "$bar-chart-box-fill",
    },
    {
      key: "CC_COMPLETE",
      urlSlug: "cuisine-centrale-diagnostics-complets",
      title: "Mettre à jour vos satellites et renseigner des bilans complets",
      description:
        "Ce type de fichier vous permet de renseigner vos données d'approvisionnement complètes au niveau de la cuisine centrale et de lister vos cantines satellites seulement avec leurs données d'établissement. Les données d'approvisionnement restent donc seulement nécessaires pour les cuisines centrales.",
      label: "Cuisine centrale avec bilan complet",
      help:
        "Vous voulez renseigner vos satellites et vous connaissez les labels et les familles de produits de vos achats",
      icon: "$checkbox-circle-fill",
    },
  ],
})
