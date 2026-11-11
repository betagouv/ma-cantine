import {
    APPROVISIONNEMENT as configFields,
    DIVERSIFICATION as configDiversificationFields,
    GASPILLAGE as configGaspillageFields,
    INFORMATION as configInformationFields,
    PLASTIQUE as configPlastiqueFields
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
  return config.index_metier ? `${config.index_metier} : ${config.verbose_name}` : undefined
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
    fields[apiKey] = {
        apiKey,
        shortName: `${config.verbose_name} :`,
        labelRecap: config.verbose_name,
        required: config.is_required,
        ...voletCustomisation[apiKey]
    }
  }
  return fields
}

/* Data */
const groups = {
  ...tunnelTeledeclaration.approvisionnement.groups,
  ...tunnelTeledeclaration.diversification.groups,
  ...tunnelTeledeclaration.gaspillage.groups,
  ...tunnelTeledeclaration.information.groups,
  ...tunnelTeledeclaration.plastique.groups,
}
const fields = {
  ...generateApproFields(),
  ...generateVoletFields(configDiversificationFields, tunnelTeledeclaration.diversification.fields),
  ...generateVoletFields(configGaspillageFields, tunnelTeledeclaration.gaspillage.fields),
  ...generateVoletFields(configInformationFields, tunnelTeledeclaration.information.fields),
  ...generateVoletFields(configPlastiqueFields, tunnelTeledeclaration.plastique.fields),
}

/* Pages */
const pagesFieldsGroups = {
  GestionnaireTunnelApproInformations: ["informationsCantine", "informationsGroupe"],
  GestionnaireTunnelApproCouverts: ["couverts"],
  GestionnaireTunnelApproSaisie: ["saisie"],
  GestionnaireTunnelApproEgalim: ["egalimSimple", "egalimComplete"],
  GestionnaireTunnelApproOrigine: ["origine"],
  GestionnaireTunnelApproLocalCircuitCourt: ["localCircuitCourt"],
  GestionnaireTunnelGaspillage: ["gaspillage"],
  GestionnaireTunnelConvives: ["information"],
  GestionnaireTunnelVegetarien: ["diversification"],
  GestionnaireTunnelPlastique: ["plastique"],
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
  let fieldsGroups = pagesFieldsGroups[pageName] || []
  if (canteenIsGroupe) fieldsGroups = fieldsGroups.filter((group) => group !== "informationsCantine")
  if (!canteenIsGroupe) fieldsGroups = fieldsGroups.filter((group) => group !== "informationsGroupe")
  if (diagnosticIsSimple) fieldsGroups = fieldsGroups.filter((group) => group !== "egalimComplete")
  if (!diagnosticIsSimple) fieldsGroups = fieldsGroups.filter((group) => group !== "egalimSimple")
  return groups[fieldsGroups[0]] || []
}

const getFieldsListFromGroup = (groupName) => {
  if (groupName !== "approvisionnement") return groups[groupName]

  return [
    ...groups.informationsCantine,
    ...groups.informationsGroupe,
    ...groups.couverts,
    ...groups.saisie,
    ...groups.egalimSimple,
    ...groups.egalimComplete,
    ...groups.origine,
    ...groups.localCircuitCourt
  ]
}

const getFieldsWithAutofill = () => {
  return Object.keys(fields).filter((field) => fields[field].autofill)
}

export default { getField, getFieldError, getFieldsListFromPage, getFieldsListFromGroup, getFieldsWithAutofill }
