const economicModel = [
  {
    label: "Public",
    value: "public",
    hint:
      "Tout restaurant sous la responsabilité d’une personne morale de droit public, qu’il soit opéré en gestion directe ou en gestion concédée (notamment avec une société de restauration collective privée). Restaurant sous la responsabilité directe ou indirecte (via association de gestion) d’une structure publique d’État (administration centrale, services déconcentrés et opérateurs dont établissements publics), d’une collectivité (commune, EPCI, département, région), ou de la fonction publique hospitalière.  ",
  },
  {
    label: "Privé",
    value: "private",
    hint:
      "Restaurant sous la responsabilité d’une structure privée : entreprise, association (hors associations de gestion d’un restaurant de structure publique), établissement scolaire privé, etc.",
  },
]

const managementType = [
  { label: "Directe", value: "direct" },
  { label: "Concédée", value: "conceded" },
]

const productionType = [
  { label: "Produit sur place les repas qu'il sert à ses convives", value: "site" },
  { label: "Sert des repas preparés par un autre établissement", value: "site_cooked_elsewhere" },
  { label: "Livre des repas mais n'a pas de lieu de service en propre", value: "central" },
  { label: "Livre des repas et accueille aussi des convives sur place", value: "central_serving" },
]

export default {
  economicModel,
  managementType,
  productionType,
}
