<script setup>
import { onMounted, reactive, watch, inject } from "vue"
import { useVuelidate } from "@vuelidate/core"
import { formatError } from "@/utils.js"
import { helpers } from "@vuelidate/validators"
import { useValidators } from "@/validators.js"
import documentation from "@/data/documentation.json"
import HelpText from "./HelpText.vue"
import Constants from "@/constants.js"

const emit = defineEmits(["provide-vuelidate", "update-payload"])
const originalPayload = inject("originalPayload")
const canteen = inject("canteen")
const payload = reactive({})
const { required, integer, minValue } = useValidators()

const rules = {
  periodStartDate: { required },
  periodEndDate: { required,
    afterStartDate: helpers.withMessage(
      "La date de fin ne peut pas être avant la date de début",
      (periodEndDate) => new Date(payload.periodStartDate) <= new Date(periodEndDate)
    )
  },
  mealCount: { required, integer, minValue: minValue(1) },
}

const v$ = useVuelidate(rules, payload)

const updatePayload = () => {
  emit("update-payload", payload)
}

watch(payload, () => {
  updatePayload()
})

onMounted(() => {
  emit("provide-vuelidate", v$)
  payload.periodStartDate = originalPayload?.periodStartDate
  payload.periodEndDate = originalPayload?.periodEndDate
  payload.mealCount = originalPayload?.mealCount
})
</script>

<template>
  <div>
    <div class="fr-grid-row fr-grid-row--middle">
      <div class="fr-col-12 fr-col-md-6">
        <fieldset class="fr-px-0 fr-pt-0 fr-mx-0">
          <legend class="fr-text--lg fr-mb-1w fr-px-0">{{ Constants.WasteMeasurement.daysInPeriod.title }}</legend>
          <div class="fr-col-md-7">
            <DsfrInputGroup
              v-model="payload.periodStartDate"
              type="date"
              label="Début"
              label-visible
              :max="payload.periodEndDate"
              :error-message="formatError(v$.periodStartDate)"
            />
            <DsfrInputGroup
              v-model="payload.periodEndDate"
              type="date"
              label="Fin"
              label-visible
              class="fr-mb-2w"
              :min="payload.periodStartDate"
              :error-message="formatError(v$.periodEndDate)"
            />
            <DsfrInputGroup
              v-model.number="payload.mealCount"
              type="number"
              :label="Constants.WasteMeasurement.mealCount.title"
              :hint="`Pour rappel, votre nombre de couvert par jour est de ${canteen.dailyMealCount} jours`"
              label-visible
              :error-message="formatError(v$.mealCount)"
            />
          </div>
        </fieldset>
      </div>
      <div class="fr-col-md-6">
        <HelpText question="Pendant combien de temps mesurer&nbsp;?">
          <p class="fr-mb-0">
            Pour garantir une bonne estimation, nous vous conseillons de réaliser vos mesures sur une période
            <b>d'au moins 5 jours.</b>
          </p>
        </HelpText>
      </div>
    </div>
  </div>
</template>
