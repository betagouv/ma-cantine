const getStatus = (key, isTeledeclared, check, recap) => {
  if (key !== "appro") return "empty"
  if (recap?.canteenDiagnosticApproStats?.objectifsEgalimAtteints) return "objectivesReached"
  if (isTeledeclared) return "teledeclared"
  if (check?.isClean) return "clean"
  return "empty"
}

const getMacaronsStatus = (isTeledeclared, check, recap) => {
  return {
    appro: getStatus("appro", isTeledeclared, check, recap),
    info: getStatus("info", isTeledeclared, check),
    waste: getStatus("waste", isTeledeclared, check),
    diversification: getStatus("diversification", isTeledeclared, check),
    plastic: getStatus("plastic", isTeledeclared, check),
  }
}

export default { getMacaronsStatus }
