import badges from "@/data/badges.json"

const getBadge = (name) => {
  const index = badges.canteen.findIndex((badge) => badge.actions.includes(name))
  return badges.canteen[index]
}

const getButton = (action) => {
  let noButton = false
  let label = null
  let name = null
  let icon = null
  let measure = null

  switch (true) {
    case action === "10_add_satellites":
      label = "Ajouter"
      name = "GestionnaireCantineSatellitesGerer"
      icon = "fr-icon-add-line"
      break
    case action === "20_create_diagnostic" || action === "18_prefill_diagnostic":
      label = "Créer"
      name = "MyProgress"
      icon = "fr-icon-add-line"
      measure = "qualite-des-produits"
      break
    case action === "30_fill_diagnostic":
      label = "Modifier"
      name = "MyProgress"
      icon = "fr-icon-edit-line"
      measure = "qualite-des-produits"
      break
    case action === "35_fill_canteen_data":
      label = "Modifier"
      name = "GestionnaireCantineGerer"
      icon = "fr-icon-edit-line"
      break
    case action === "40_teledeclare":
      label = "Télédéclarer"
      name = "MyProgress"
      icon = "fr-icon-send-plane-line"
      measure = "etablissement"
      break
    default:
      noButton = true
  }

  if (noButton) return null
  return {
    label,
    name,
    icon,
    measure,
  }
}

export default { getBadge, getButton }
