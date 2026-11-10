const getStatus = (key, isTeledeclared, check, recap) => {
  const isCleanVolets = {
    information: check?.isCleanInformation,
    gaspillage: check?.isCleanGaspillage,
    diversification: check?.isCleanDiversification,
    plastique: check?.isCleanPlastique,
    approvisionnement: check?.isCleanApprovisionnement,
  }
  if (recap?.canteenDiagnosticApproStats?.objectifsEgalimAtteints) return "objectivesReached"
  if (isTeledeclared) return "teledeclared"  // TODO : fix it for thematique volet
  if (isCleanVolets[key]) return "clean"
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
