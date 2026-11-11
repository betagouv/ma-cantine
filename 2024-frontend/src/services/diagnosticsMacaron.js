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

  const objectives = {
    information: recap?.canteenDiagnosticThematiquesStats?.objectifsInformationAtteints,
    gaspillage: recap?.canteenDiagnosticThematiquesStats?.objectifsGaspillageAtteints,
    diversification: recap?.canteenDiagnosticThematiquesStats?.objectifsDiversificationAtteints,
    plastique: recap?.canteenDiagnosticThematiquesStats?.objectifsPlastiqueAtteints,
    approvisionnement: recap?.canteenDiagnosticApproStats?.objectifsEgalimAtteints,
  }

  const isAppro = key === "approvisionnement"
  if (isTeledeclared && objectives[key]) return "objectivesReached"
  if (isAppro && isTeledeclared) return "teledeclared"
  if (!isAppro && isTeledeclared && isCleanVolets[key] && isFilledVolets[key]) return "teledeclared"
  if (isAppro && isCleanVolets[key]) return "clean"
  if (!isAppro && isCleanVolets[key] && isFilledVolets[key]) return "clean"
  return "empty"
}

const getMacaronsStatus = (isTeledeclared, check, recap) => {
  return {
    approvisionnement: getStatus("approvisionnement", isTeledeclared, check, recap),
    information: getStatus("information", isTeledeclared, check, recap),
    gaspillage: getStatus("gaspillage", isTeledeclared, check, recap),
    diversification: getStatus("diversification", isTeledeclared, check, recap),
    plastique: getStatus("plastique", isTeledeclared, check, recap),
  }
}

export default { getMacaronsStatus }
