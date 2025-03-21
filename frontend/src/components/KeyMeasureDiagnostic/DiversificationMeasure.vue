<template>
  <div>
    <v-checkbox
      hide-details="auto"
      class="mb-4"
      v-model="diagnostic.hasDiversificationPlan"
      :label="constantsDiversificationMeasureStep.hasDiversificationPlan.title"
      :readonly="readonly"
      :disabled="readonly"
      v-if="applicableRules.hasDiversificationPlan"
    />

    <fieldset class="my-3" v-if="applicableRules.hasDiversificationPlan">
      <legend class="text-left mb-2 mt-3" :class="{ 'grey--text': !diagnostic.hasDiversificationPlan }">
        {{ constantsDiversificationMeasureStep.diversificationPlanActions.title }}
      </legend>
      <v-checkbox
        hide-details="auto"
        class="ml-8 mt-2"
        v-model="diagnostic.diversificationPlanActions"
        :multiple="true"
        v-for="item in constantsDiversificationMeasureStep.diversificationPlanActions.items"
        :key="item.value"
        :value="item.value"
        :label="item.label"
        :readonly="readonly || !diagnostic.hasDiversificationPlan"
        :disabled="readonly || !diagnostic.hasDiversificationPlan"
      />
    </fieldset>

    <DsfrRadio
      :label="constantsDiversificationMeasureStep.vegetarianWeeklyRecurrence.title"
      v-model="diagnostic.vegetarianWeeklyRecurrence"
      hide-details
      :items="constantsDiversificationMeasureStep.vegetarianWeeklyRecurrence.items"
      :readonly="readonly"
      :disabled="readonly"
      optionClasses="ml-8"
      class="mt-3"
    />

    <DsfrRadio
      :label="constantsDiversificationMeasureStep.vegetarianMenuType.title"
      v-model="diagnostic.vegetarianMenuType"
      hide-details
      :items="constantsDiversificationMeasureStep.vegetarianMenuType.items"
      :readonly="readonly"
      :disabled="readonly"
      optionClasses="ml-8"
      class="mt-3"
    />

    <fieldset class="mt-3">
      <legend class="text-left mb-2 mt-3">
        {{ constantsDiversificationMeasureStep.vegetarianMenuBases.title }}
      </legend>
      <v-checkbox
        hide-details="auto"
        class="ml-8 mt-2"
        v-model="diagnostic.vegetarianMenuBases"
        :multiple="true"
        v-for="item in constantsDiversificationMeasureStep.vegetarianMenuBases.items"
        :key="item.value"
        :value="item.value"
        :label="item.label"
        :readonly="readonly"
        :disabled="readonly"
      />
    </fieldset>

    <v-divider aria-hidden="true" role="presentation" v-if="showExpeSegment" class="my-4"></v-divider>
    <div v-if="showExpeSegment">
      <h3 class="text-h6 font-weight-bold mb-4">
        Expérimentation de l'option végétarienne quotidienne pour les collectivités volontaires
      </h3>
      <p class="body-2">
        Pour participer à l'expérimentation d'une option végétarienne quotidienne, telle que prévue par la loi Climat et
        résilience, nous vous proposons de répondre à quelques questions sur la mise en œuvre de l'option végétarienne
        quotidienne dans votre établissement.
      </p>
      <p class="body-2">
        En particulier, les questions portent sur les catégories de plats végétariens servis, l'impact sur les pesées de
        gaspillage alimentaire, la fréquentation, la satisfaction des convives et le coût des repas. Il est également
        possible de participer si une option végétarienne quotidienne est déjà mise en place dans votre établissement.
      </p>
      <v-checkbox v-if="canteen" v-model="canteen.vegetarianExpeParticipant" @change="onExpeCheckboxChange">
        <template v-slot:label>
          <span class="body-2 grey--text text--darken-3">
            Je suis volontaire pour participer à l’expérimentation.
          </span>
        </template>
      </v-checkbox>
      <v-btn
        color="primary"
        class="body-2 mt-n2 mb-2"
        v-if="canteen.vegetarianExpeParticipant"
        outlined
        small
        @click="() => (showExpeModal = true)"
      >
        Mettre à jour mes données
      </v-btn>

      <v-dialog v-model="showExpeModal" :width="$vuetify.breakpoint.mdAndUp ? 900 : undefined">
        <ExpeVegetarian v-if="showExpeModal" @close="() => (showExpeModal = false)" :canteen="canteen" />
      </v-dialog>
    </div>
  </div>
</template>

<script>
import { applicableDiagnosticRules } from "@/utils"
import ExpeVegetarian from "@/components/KeyMeasureDiagnostic/ExpeModals/ExpeVegetarian"
import DsfrRadio from "@/components/DsfrRadio"
import Constants from "@/constants"

export default {
  props: {
    diagnostic: Object,
    readonly: {
      type: Boolean,
      default: false,
    },
    canteen: Object,
  },
  components: { ExpeVegetarian, DsfrRadio },
  data() {
    return {
      showExpeModal: false,
      constantsDiversificationMeasureStep: Constants.DiversificationMeasureStep,
    }
  },
  computed: {
    applicableRules() {
      return applicableDiagnosticRules(this.canteen)
    },
    showExpeSegment() {
      return !!this.canteen && window.ENABLE_XP_VEGE
    },
  },
  methods: {
    onExpeCheckboxChange(checked) {
      this.$store
        .dispatch("updateCanteen", {
          id: this.canteen.id,
          payload: { vegetarianExpeParticipant: checked },
        })
        .then((canteen) => {
          this.$emit("update:canteen", canteen)
        })
        .catch((e) => this.$store.dispatch("notifyServerError", e))

      if (checked) this.showExpeModal = true
    },
  },
}
</script>
