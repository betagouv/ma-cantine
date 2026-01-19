const getBadge = (name, campaignDates) => {
  let label = null
  let type = null
  const isInCampaign = campaignDates.inCorrection || campaignDates.inTeledeclaration
  const toTeledeclare = name === "40_teledeclare"
  const hasTeledeclared = ["91_nothing_satellite_teledeclared", "95_nothing"].includes(name)
  const waitingCentral = name === "90_nothing_satellite"
  const needsFill = [
    "10_add_satellites",
    "35_fill_canteen_data",
    "18_prefill_diagnostic",
    "20_create_diagnostic",
    "30_fill_diagnostic",
    "36_fill_satellite_canteen_data",
  ].includes(name)

  switch (true) {
    case hasTeledeclared: // Always display if a diagnostic is teledeclared
      label = "Télédéclaré"
      type = "success"
      break
    case !hasTeledeclared && !campaignDates.inTeledeclaration: // If not in teledeclaration campaign this is defaut badge for a diagnostic
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
  if (action !== "40_teledeclare") return false

  return {
    label: "Télédéclarer",
    name: "MyProgress",
    icon: "fr-icon-send-plane-line",
    measure: "etablissement",
  }
}

export default { getBadge, getTeledeclareButton }
