import * as validators from "@vuelidate/validators"
import { useI18n } from "vue-i18n"

// To use more vuelidate validators, add the name of the validator to the appropriate array
// and add the translation for the error message in @/locales/...
const VUELIDATE_VALIDATORS = ["required", "integer", "decimal"]
const VUELIDATE_VALIDATORS_WITH_ARGS = ["minValue", "maxValue"]

// https://github.com/vuelidate/vuelidate/issues/1164#issuecomment-2104538357
export const useValidators = () => {
  const { t } = useI18n()
  const withI18nMessage = validators.createI18nMessage({ t })

  const ourValidators = {}
  VUELIDATE_VALIDATORS.forEach((vName) => (ourValidators[vName] = withI18nMessage(validators[vName])))
  VUELIDATE_VALIDATORS_WITH_ARGS.forEach(
    (vName) => (ourValidators[vName] = withI18nMessage(validators[vName], { withArguments: true }))
  )

  return ourValidators
}
