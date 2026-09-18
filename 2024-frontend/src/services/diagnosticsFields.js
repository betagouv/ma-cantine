import teledeclaration from "@/data/teledeclaration.json"

const getField = (fieldName) => {
  return teledeclaration.fields[fieldName]
}

const getFieldError = (fieldName, errors) => {
  const hasError = errors.find(error => error.field === fieldName)
  return hasError ? hasError.message : null
}

const getFieldsListFromPage = (pageName, canteenIsGroupe, diagnosticIsSimple) => {
  switch (true) {
    case pageName === "GestionnaireTunnelApproInformations" && !canteenIsGroupe:
      return teledeclaration.groups.informationsCantine
    case pageName === "GestionnaireTunnelApproInformations" && canteenIsGroupe:
      return teledeclaration.groups.informationsGroupe
    case pageName === "GestionnaireTunnelApproCouverts":
      return teledeclaration.groups.couverts
    case pageName === "GestionnaireTunnelApproSaisie":
      return teledeclaration.groups.saisie
    case pageName === "GestionnaireTunnelApproEgalim" && diagnosticIsSimple:
      return teledeclaration.groups.egalimSimple
    case pageName === "GestionnaireTunnelApproEgalim" && !diagnosticIsSimple:
      return teledeclaration.groups.egalimComplete
    case pageName === "GestionnaireTunnelApproOrigine":
      return teledeclaration.groups.origine
    case pageName === "GestionnaireTunnelApproLocalCircuitCourt":
      return teledeclaration.groups.localCircuitCourt
    default:
      return []
  }
}

const getFieldsListFromGroup = (groupName) => {
  return teledeclaration.groups[groupName]
}

export default { getField, getFieldError, getFieldsListFromPage, getFieldsListFromGroup }
