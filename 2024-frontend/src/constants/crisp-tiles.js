import documentation from "@/data/documentation.json"
import IconMacaronApprovisionnement from "@/components/IconMacaronApprovisionnement.vue"
import IconMacaronGaspillage from "@/components/IconMacaronGaspillage.vue"
import IconMacaronDiversification from "@/components/IconMacaronDiversification.vue"
import IconMacaronPlastique from "@/components/IconMacaronPlastique.vue"
import IconMacaronInformation from "@/components/IconMacaronInformation.vue"

const tiles = [
  {
    title: "Produits EGalim",
    macaron: IconMacaronApprovisionnement,
    details:
      "Retrouvez la liste des labels éligibles aux 50% de produits EGalim, aux 20% de produits bio et aux 60% de produits EGalim pour les familles cumulées viandes-volailles-poissons.",
    to: documentation.qualiteDurabiliteProduits,
  },
  {
    title: "Lutte contre le gaspillage alimentaire",
    macaron: IconMacaronGaspillage,
    details:
      "La lutte contre le gaspillage alimentaire est un pilier de la transition écologique en restauration collective. Les lois EGalim (2018) et AGEC (2020) imposent des obligations concrètes aux établissements pour limiter les pertes, valoriser les excédents et améliorer la gestion des repas.",
    to: documentation.lutteGaspillageAlimentaire,
  },
  {
    title: "Diversification des sources de protéines et menu végétarien",
    macaron: IconMacaronDiversification,
    details:
      "La loi EGalim a introduit des évolutions majeures en matière de restauration collective, dont l’obligation de proposer régulièrement des menus végétariens.",
    to: documentation.diversificationSourcesProteines,
  },
  {
    title: "Substitution du plastique",
    macaron: IconMacaronPlastique,
    details:
      "Dans le cadre de la loi EGalim, la réduction du plastique en restauration collective nécessite une adaptation dans les comportements existants.",
    to: documentation.interdictionPlastique,
  },
  {
    title: "Informations des convives",
    macaron: IconMacaronInformation,
    details:
      "Vous souhaitez valoriser vos actions auprès des convives ? Zoom sur les obligations en matière de communication.",
    to: documentation.informationsConvives,
  },
]

export { tiles }
