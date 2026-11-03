import { APPROVISIONNEMENT as configFields } from "../../../teledeclaration/2026/champs.json"
import tunnelTeledeclaration from "@/data/tunnelTeledeclaration.json"
import { toCamelCase } from "@/utils.js"

/* Fields */
const tunnelApproCustomisation = tunnelTeledeclaration.approvisionnement.fields

const formatFieldData = (name, config) => {
  const apiKey = toCamelCase(name)
  const { SIMPLE, COMPLETE } = config.diagnostic_type
  const isSameRequired = SIMPLE.is_required === COMPLETE.is_required
  const isAlwaysRequired = SIMPLE.is_required && COMPLETE.is_required
  return {
    apiKey,
    labelRecap: config.verbose_name,
    hint: config.index ? `${config.index} : ${config.verbose_name}` : undefined,
    type: "number",
    autofill: name.startsWith("valeur_"),
    placeholder: isAlwaysRequired ? undefined : "Je ne sais pas",
    ...(isSameRequired
      ? { required: SIMPLE.is_required }
      : { requiredByType: { SIMPLE: SIMPLE.is_required, COMPLETE: COMPLETE.is_required } }),
    ...tunnelApproCustomisation[apiKey],
  }
}

const generateTeledeclarationFields = () => {
  const fields = { diagnosticType: { apiKey: "diagnosticType", ...tunnelApproCustomisation.diagnosticType } }
  for (const [name, config] of Object.entries(configFields)) {
    fields[toCamelCase(name)] = formatFieldData(name, config)
  }
    console.log("fields", fields)
  return fields
}

/* Data */
const groups = { ...tunnelTeledeclaration.approvisionnement.groups }
const fields = generateTeledeclarationFields()

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
