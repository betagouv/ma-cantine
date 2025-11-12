import cantines from "@/data/cantines.json"

const getBadge = (name) => {
  const index = cantines.actions.findIndex((action) => action.names.includes(name))
  return cantines.actions[index]
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
