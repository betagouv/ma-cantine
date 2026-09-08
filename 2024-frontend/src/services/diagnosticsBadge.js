const toCompleteActions = [
  "10_add_satellites",
  "35_fill_canteen_data",
  "18_prefill_diagnostic",
  "20_create_diagnostic",
  "30_fill_diagnostic",
  "36_fill_satellite_canteen_data",
]
const toTeledeclareActions = ["40_teledeclare"]
const isTeledeclaredActions = [
  "91_nothing_satellite_teledeclared",
  "95_nothing"
]
const isWaitingActions = ["90_nothing_satellite"]
const notTeledeclaredActions = ["45_did_not_teledeclare"]

const getBadge = (name, campaignDates) => {
  let label = null
  let type = null
  const isInCampaign = campaignDates.inCorrection || campaignDates.inTeledeclaration
  const toTeledeclare = toTeledeclareActions.includes(name)
  const hasTeledeclared = isTeledeclaredActions.includes(name)
  const waitingCentral = isWaitingActions.includes(name)
  const needsFill = toCompleteActions.includes(name)
  const notTeledeclared = notTeledeclaredActions.includes(name)

  switch (true) {
    case hasTeledeclared: // Always display if a diagnostic is teledeclared
      label = "Télédéclaré"
      type = "success"
      break
    case notTeledeclared: // If diagnostic is not teledeclared
      label = "Non télédéclaré"
      type = "neutral"
      break
    case isInCampaign && toTeledeclare: // If diagnostic needs to be teledeclared
      label = "À télédéclarer"
      type = "error"
      break
    case isInCampaign && needsFill: // If diagnostic or canteen is missing data to teledeclare
      label = "À compléter"
      type = "error"
      break
    case isInCampaign && waitingCentral: // If central did not teledeclare its diagnostic
      label = "En attente"
      type = "warning"
      break
  }
  return {
    label,
    type,
  }
}

const getTeledeclareButton = (action) => {
  if (!toTeledeclareActions.includes(action)) return false

  return {
    label: "Télédéclarer",
    name: "MyProgress",
    type: "primary",
    icon: "fr-icon-send-plane-line",
    measure: "etablissement",
  }
}

const getCompleteButton = (action) => {
  if (!toCompleteActions.includes(action)) return false

  return {
    label: "À compléter",
    name: "MyProgress",
    type: "tertiary",
    noIcon: true,
    measure: "etablissement",
  }
}

export default { getBadge, getTeledeclareButton, getCompleteButton }
