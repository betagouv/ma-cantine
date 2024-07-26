<script setup>
import { onMounted, reactive, watch, inject } from "vue"
import { useVuelidate } from "@vuelidate/core"
import { required, integer, minValue } from "@vuelidate/validators"
import { formatError } from "@/utils.js"
import HelpText from "./HelpText.vue"

const emit = defineEmits(["provide-vuelidate", "update-payload"])

const originalPayload = inject("originalPayload")

const state = reactive({
  editMealCount: originalPayload.editMealCount,
  editCanteenMealCount: originalPayload.editCanteenMealCount,
})

const toggleCanteenEdit = () => {
  state.editCanteenMealCount = !state.editCanteenMealCount
  // disable period meal count edit to avoid confusion
  if (state.editCanteenMealCount) state.editMealCount = false
}

const togglePeriodEdit = () => {
  state.editMealCount = !state.editMealCount
  if (state.editMealCount) state.editCanteenMealCount = false
  // TODO: do we want to track when the number was changed from the auto calculation?
}

const saveCanteenMealCount = () => {
  state.editCanteenMealCount = !state.editCanteenMealCount
}

const payload = reactive({
  startDate: originalPayload.startDate,
  endDate: originalPayload.endDate,
  mealCount: 100, // TODO: update according to days in period * canteen daily meal count
  canteen: {
    dailyMealCount: 200, // TODO: initialise with data
  },
})

const rules = {
  startDate: { required }, // TODO: ensure greater than endDate of last measurement taken
  endDate: { required }, // TODO: ensure greater than startDate
  mealCount: { required, integer, minValue: minValue(1) },
  canteen: {
    dailyMealCount: { required, integer, minValue: minValue(1) },
  },
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
})
</script>

<template>
  <div>
    <div class="fr-grid-row fr-grid-row--middle">
      <div class="fr-col-12 fr-col-md-6">
        <fieldset class="fr-px-0 fr-pt-0 fr-mx-0">
          <legend class="fr-text--lg fr-mb-1w fr-px-0">Période de mesure de mon gaspillage alimentaire</legend>
          <div class="fr-col-md-7">
            <DsfrInputGroup
              v-model="payload.startDate"
              type="date"
              label="Début"
              label-visible
              :error-message="formatError(v$.startDate)"
            />
            <DsfrInputGroup
              v-model="payload.endDate"
              type="date"
              label="Fin"
              label-visible
              class="fr-mb-2w"
              :error-message="formatError(v$.endDate)"
            />
          </div>
        </fieldset>
      </div>
      <div class="fr-col-md-6">
        <!-- TODO: show this whilst !startDate || !endDate -->
        <HelpText question="Pendant combien de temps mesurer&nbsp;?">
          <p class="fr-mb-0">
            Pour garantir une bonne estimation, nous vous conseillons de réaliser vos mesures sur une période
            <b>d'au moins 5 jours.</b>
          </p>
        </HelpText>
      </div>
    </div>
    <div class="fr-grid-row fr-grid-row--middle fr-mt-0w">
      <div class="fr-col-md-6">
        <div class="fr-grid-row fr-grid-row--bottom">
          <div class="fr-mr-2w">
            <DsfrInputGroup
              v-model.number="payload.mealCount"
              type="number"
              label="Nombre de couverts sur la période"
              label-visible
              :error-message="formatError(v$.mealCount)"
              :disabled="!state.editMealCount"
            />
          </div>
          <div>
            <DsfrButton v-if="!state.editMealCount" @click="togglePeriodEdit" tertiary icon="fr-icon-pencil-fill">
              Modifier
            </DsfrButton>
            <DsfrButton v-else @click="togglePeriodEdit">Sauvegarder</DsfrButton>
          </div>
        </div>
      </div>
      <div class="fr-col-md-6">
        <!-- TODO: show this when !!startDate && !!endDate -->
        <HelpText>
          <p>
            Calculé à partir du nombre de couverts par jour indiqué pour votre établissement :
          </p>
          <div v-if="!state.editCanteenMealCount" class="fr-grid-row fr-grid-row--bottom">
            <p class="fr-mb-0 fr-mr-2w">{{ payload.canteen.dailyMealCount }}</p>
            <div>
              <DsfrButton @click="toggleCanteenEdit" tertiary icon="fr-icon-pencil-fill" size="sm">Modifier</DsfrButton>
            </div>
          </div>
          <div v-else class="fr-grid-row fr-grid-row--bottom">
            <!-- TODO: how to keep in alignement against year meal count? Show both? -->
            <div class="fr-mr-2w">
              <DsfrInputGroup
                v-model.number="payload.canteen.dailyMealCount"
                type="number"
                label="Nombre de couverts par jour"
                label-visible
                :error-message="formatError(v$.canteen.dailyMealCount)"
              />
            </div>
            <div>
              <DsfrButton @click="saveCanteenMealCount">Sauvegarder</DsfrButton>
            </div>
          </div>
        </HelpText>
      </div>
    </div>
  </div>
</template>
