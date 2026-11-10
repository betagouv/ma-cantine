const getStatus = (key, isTeledeclared, check, recap) => {
  if (key !== "approvisionnement") return "empty"
  if (recap?.canteenDiagnosticApproStats?.objectifsEgalimAtteints) return "objectivesReached"
  if (isTeledeclared) return "teledeclared"
  if (check?.isClean) return "clean"
  return "empty"
}

const getMacaronsStatus = (isTeledeclared, check, recap) => {
  return {
    approvisionnement: getStatus("approvisionnement", isTeledeclared, check, recap),
    information: getStatus("information", isTeledeclared, check),
    gaspillage: getStatus("gaspillage", isTeledeclared, check),
    diversification: getStatus("diversification", isTeledeclared, check),
    plastique: getStatus("plastique", isTeledeclared, check),
  }
}

export default { getMacaronsStatus }
