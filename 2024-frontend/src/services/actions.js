import badges from "@/data/badges.json"

const getBadge = (name) => {
  const index = badges.canteen.findIndex((badge) => badge.actions.includes(name))
  return badges.canteen[index]
}

const getTeledeclareButton = (action) => {
  if (action !== "40_teledeclare") return false

  return {
    label: "Télédéclarer",
    name: "MyProgress",
    icon: "fr-icon-send-plane-line",
    measure: "etablissement",
  }
}

export default { getBadge, getTeledeclareButton }
