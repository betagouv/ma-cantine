import teledeclarationFields from "@/data/teledeclarationFields.json"
import teledeclarationGroups from "@/data/teledeclarationGroups.json"

/* Data */
const groups = { ...teledeclarationGroups.approvisionnement, ...teledeclarationGroups.diversification }
const fields = { ...teledeclarationFields.approvisionnement, ...teledeclarationFields.diversification }

/* Actions */
const getField = (fieldName) => {
  return fields[fieldName]
}

const getFieldError = (fieldName, errors) => {
  const hasError = errors.find(error => error.field === fieldName)
  return hasError ? hasError.message : null
}

const getFieldsListFromPage = (pageName, canteenIsGroupe, diagnosticIsSimple) => {
  switch (true) {
    case pageName === "GestionnaireTunnelApproInformations" && !canteenIsGroupe:
      return groups.informationsCantine
    case pageName === "GestionnaireTunnelApproInformations" && canteenIsGroupe:
      return groups.informationsGroupe
    case pageName === "GestionnaireTunnelApproCouverts":
      return groups.couverts
    case pageName === "GestionnaireTunnelApproSaisie":
      return groups.saisie
    case pageName === "GestionnaireTunnelApproEgalim" && diagnosticIsSimple:
      return groups.egalimSimple
    case pageName === "GestionnaireTunnelApproEgalim" && !diagnosticIsSimple:
      return groups.egalimComplete
    case pageName === "GestionnaireTunnelApproOrigine":
      return groups.origine
    case pageName === "GestionnaireTunnelApproLocalCircuitCourt":
      return groups.localCircuitCourt
    default:
      return []
  }
}

const getFieldsListFromGroup = (groupName) => {
  return groups[groupName]
}

const getFieldsWithAutofill = () => {
  return Object.keys(fields).filter((field) => fields[field].autofill)
}

export default { getField, getFieldError, getFieldsListFromPage, getFieldsListFromGroup, getFieldsWithAutofill }
