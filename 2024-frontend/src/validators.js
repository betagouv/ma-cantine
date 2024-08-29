import * as validators from "@vuelidate/validators"

const VUELIDATE_VALIDATORS = ["required", "integer", "decimal", "minValue", "maxValue"]

export const useValidators = () => {
  const ourValidators = {}
  VUELIDATE_VALIDATORS.forEach((vName) => (ourValidators[vName] = validators[vName]))

  return ourValidators
}
