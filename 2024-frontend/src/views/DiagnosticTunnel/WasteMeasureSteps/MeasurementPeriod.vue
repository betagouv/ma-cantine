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
    <div class="fr-grid-row">
      <div class="fr-col-12 fr-col-sm-6">
        <DsfrInputGroup
          v-model="payload.startDate"
          type="date"
          label="Debut de la période"
          label-visible
          class="fr-mb-2w"
          :error-message="formatError(v$.startDate)"
        />
        <DsfrInputGroup
          v-model="payload.endDate"
          type="date"
          label="Fin de la période (inclusif)"
          label-visible
          class="fr-mb-2w"
          :error-message="formatError(v$.endDate)"
        />
      </div>
      <div class="fr-col-sm-6">
        <HelpText question="Pendant combien de temps mesurer ?">
          <p>
            Pour garantir une bonne estimation, nous vous conseillons de réaliser vos mesures sur une période d’au moins
            5 jours.
          </p>
        </HelpText>
      </div>
    </div>
    <div class="fr-grid-row fr-mt-0w">
      <div class="fr-col-sm-6">
        <div class="fr-grid-row">
          <DsfrInputGroup
            v-model.number="payload.mealCount"
            type="number"
            label="Nombre de couverts sur la période"
            label-visible
            class="fr-mb-2w"
            :error-message="formatError(v$.mealCount)"
            :disabled="!state.editMealCount"
          />
          <div>
            <DsfrButton @click="togglePeriodEdit">Modifier</DsfrButton>
          </div>
        </div>
      </div>
      <div class="fr-col-sm-6">
        <HelpText>
          <p>
            Calculé à partir du nombre de couverts par jour indiqué pour votre établissement :
          </p>
          <div v-if="!state.editCanteenMealCount" class="fr-grid-row">
            <p>{{ payload.canteen.dailyMealCount }}</p>
            <DsfrButton @click="toggleCanteenEdit">Modifier</DsfrButton>
          </div>
          <div v-else class="fr-grid-row">
            <!-- TODO: how to keep in alignement against year meal count? Show both? -->
            <DsfrInputGroup
              v-model.number="payload.canteen.dailyMealCount"
              type="number"
              label="Nombre de couverts par jour"
              label-visible
              class="fr-mb-2w"
              :error-message="formatError(v$.canteen.dailyMealCount)"
            />
            <div>
              <DsfrButton @click="state.editCanteenMealCount = !state.editCanteenMealCount">Sauvegarder</DsfrButton>
            </div>
          </div>
        </HelpText>
      </div>
    </div>
  </div>
</template>
