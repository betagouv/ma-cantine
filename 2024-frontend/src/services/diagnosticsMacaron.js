const getStatus = (key, isTeledeclared, check, recap) => {

  const isCleanVolets = {
    information: check?.isCleanInformation,
    gaspillage: check?.isCleanGaspillage,
    diversification: check?.isCleanDiversification,
    plastique: check?.isCleanPlastique,
    approvisionnement: check?.isCleanApprovisionnement,
  }

  const isFilledVolets = {
    information: check?.isFilledInformation,
    gaspillage: check?.isFilledGaspillage,
    diversification: check?.isFilledDiversification,
    plastique: check?.isFilledPlastique,
    approvisionnement: check?.isFilledApprovisionnement,
  }

  const isAppro = key === "approvisionnement"
  if (recap?.canteenDiagnosticApproStats?.objectifsEgalimAtteints) return "objectivesReached"
  if (isAppro && isTeledeclared) return "teledeclared"
  if (!isAppro && isTeledeclared && isCleanVolets[key] && isFilledVolets[key]) return "teledeclared"
  if (isAppro && isCleanVolets[key]) return "clean"
  if (!isAppro && isCleanVolets[key] && isFilledVolets[key]) return "clean"
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
