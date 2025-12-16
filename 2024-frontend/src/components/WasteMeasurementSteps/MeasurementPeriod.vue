<script setup>
import { onMounted, reactive, watch, inject, computed } from "vue"
import { useVuelidate } from "@vuelidate/core"
import { formatError } from "@/utils.js"
import HelpText from "./HelpText.vue"
import Constants from "@/constants.js"

import { helpers } from "@vuelidate/validators"
import { useValidators } from "@/validators.js"
const { required, integer, minValue } = useValidators()

const emit = defineEmits(["provide-vuelidate", "update-payload"])

const originalPayload = inject("originalPayload")
const canteen = inject("canteen")

const state = reactive({
  editMealCount: false,
})

const togglePeriodEdit = () => {
  state.editMealCount = !state.editMealCount
}

const datesEntered = computed(() => {
  return !!payload.periodStartDate && !!payload.periodEndDate
})

const startDateAsDate = computed(() => {
  return new Date(payload.periodStartDate)
})
const endDateAsDate = computed(() => {
  return new Date(payload.periodEndDate)
})

const daysInPeriod = computed(() => {
  if (!datesEntered.value) return undefined
  const milliseconds = endDateAsDate.value - startDateAsDate.value
  const daysInclusive = milliseconds / 1000 / 60 / 60 / 24 + 1
  if (daysInclusive < 0) return undefined
  return daysInclusive
})


const payload = reactive({})

const afterStartDateValidator = (date) => {
  date = new Date(date)
  return date >= startDateAsDate.value
}

const afterStartDate = helpers.withMessage(
  "La date de fin ne peut pas être avant la date de début",
  afterStartDateValidator
)

const rules = {
  periodStartDate: { required },
  periodEndDate: { required, afterStartDate },
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
            />
          </div>
        </fieldset>
      </div>
      <div class="fr-col-md-6">
        <HelpText v-if="!datesEntered" question="Pendant combien de temps mesurer&nbsp;?">
          <p class="fr-mb-0">
            Pour garantir une bonne estimation, nous vous conseillons de réaliser vos mesures sur une période
            <b>d'au moins 5 jours.</b>
          </p>
        </HelpText>
      </div>
    </div>
    <div class="fr-grid-row fr-grid-row--middle fr-mt-2w" v-if="canteen.dailyMealCount">
      <div class="fr-col-md-6">
        <div class="fr-grid-row fr-grid-row--bottom">
          <div class="fr-mr-2w">
            <DsfrInputGroup
              v-model.number="payload.mealCount"
              type="number"
              :label="Constants.WasteMeasurement.mealCount.title"
              :hint="`${daysInPeriod || '?'} jours`"
              label-visible
              :error-message="formatError(v$.mealCount)"
              :disabled="!state.editMealCount"
            />
          </div>
          <div>
            <DsfrButton
              v-if="!state.editMealCount"
              @click="togglePeriodEdit"
              :disabled="!datesEntered"
              tertiary
              icon="fr-icon-pencil-fill"
            >
              Modifier
            </DsfrButton>
          </div>
        </div>
      </div>
      <div class="fr-col-md-6">
        <HelpText v-if="datesEntered">
          <p class="fr-mb-1w">
            Calculé à partir du nombre de couverts par jour indiqué pour votre établissement :
          </p>
          <p class="fr-mb-0">
            <b>{{ canteen.dailyMealCount }}</b>
          </p>
        </HelpText>
      </div>
    </div>
    <div class="fr-grid-row fr-grid-row--middle fr-mt-2w" v-else>
      <div class="fr-col-md-6">
        <div class="fr-grid-row fr-grid-row--bottom">
          <div class="fr-mr-2w">
            <DsfrInputGroup
              v-model.number="payload.mealCount"
              type="number"
              :label="Constants.WasteMeasurement.mealCount.title"
              :hint="`${daysInPeriod || '?'} jours`"
              label-visible
              :error-message="formatError(v$.mealCount)"
            />
          </div>
        </div>
      </div>
      <div class="fr-col-md-6">
        <HelpText v-if="datesEntered && canteen.yearlyMealCount">
          <p class="fr-mb-1w">
            Pour rappel, votre établissement sert
            <b>{{ canteen.yearlyMealCount }}</b>
            repas par an.
          </p>
        </HelpText>
      </div>
    </div>
  </div>
</template>
