const getStatus = (key, isTeledeclared, check) => {
  if (key !== "appro") return "empty"
  if (isTeledeclared) return "teledeclared"
  if (check?.isClean) return "fill"
  return "empty"
}

const getMacaronsStatus = (isTeledeclared, check) => {
  return {
    appro: getStatus("appro", isTeledeclared, check),
    info: getStatus("info", isTeledeclared, check),
    waste: getStatus("waste", isTeledeclared, check),
    diversification: getStatus("diversification", isTeledeclared, check),
    plastic: getStatus("plastic", isTeledeclared, check),
  }
}

export default { getMacaronsStatus }
