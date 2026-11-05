import {
    APPROVISIONNEMENT as configFields,
    DIVERSIFICATION as configDiversificationFields
} from "../../../teledeclaration/2026/champs.json"
import tunnelTeledeclaration from "@/data/tunnelTeledeclaration.json"
import { toCamelCase } from "@/utils.js"

/* Fields */
const tunnelApproCustomisation = tunnelTeledeclaration.approvisionnement.fields

const getRequiredApproProps = ({ SIMPLE, COMPLETE }) => {
  const isSameRequired = SIMPLE.is_required === COMPLETE.is_required
  if (isSameRequired) return { required: SIMPLE.is_required }
  return { requiredByType: { SIMPLE: SIMPLE.is_required, COMPLETE: COMPLETE.is_required } }
}

const getHintApproProps = (customisation, config) => {
  if (customisation.hint) return customisation.hint
  return config.index ? `${config.index} : ${config.verbose_name}` : undefined
}

const generateApproFields = () => {
  const fields = { diagnosticType: { apiKey: "diagnosticType", ...tunnelApproCustomisation.diagnosticType } }
  for (const [name, config] of Object.entries(configFields)) {
    const apiKey = toCamelCase(name)
    const requiredProps = getRequiredApproProps(config.diagnostic_type)
    const customisation = tunnelApproCustomisation[apiKey] ?? {}
    fields[apiKey] = {
      apiKey,
      shortName: customisation.shortName,
      labelRecap: config.verbose_name,
      hint: getHintApproProps(customisation, config),
      tooltip: customisation.tooltip,
      isRelatedField: customisation.isRelatedField,
      type: customisation.type ?? "number",
      options: customisation.options,
      autofill: name.startsWith("valeur_"),
      ...requiredProps,
    }
  }
  return fields
}

const generateVoletFields = (voletConfig, voletCustomisation) => {
  const fields = {}
  for (const [name, config] of Object.entries(voletConfig)) {
    const apiKey = toCamelCase(name)
    fields[apiKey] = { apiKey, labelRecap: config.verbose_name, ...voletCustomisation[apiKey] }
  }
  return fields
}

/* Data */
const groups = { ...tunnelTeledeclaration.approvisionnement.groups, ...tunnelTeledeclaration.diversification.groups }
const fields = {
  ...generateApproFields(),
  ...generateVoletFields(configDiversificationFields, tunnelTeledeclaration.diversification.fields),
}

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
