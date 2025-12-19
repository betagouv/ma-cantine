<template>
  <v-form @submit.prevent>
    <div v-if="stepUrlSlug === 'plan'">
      <DsfrRadio
        :label="stepConstants.hasDiversificationPlan.title"
        v-model="payload.hasDiversificationPlan"
        hide-details
        yesNo
        optional
      />
      <fieldset class="mt-8 mb-3">
        <legend class="text-left mb-1 mt-3" :class="{ 'grey--text': !payload.hasDiversificationPlan }">
          {{ stepConstants.diversificationPlanActions.title }}
          <span :class="`fr-hint-text mt-2 ${!payload.hasDiversificationPlan && 'grey--text'}`">Optionnel</span>
        </legend>
        <v-checkbox
          hide-details="auto"
          class="mt-1"
          v-model="payload.diversificationPlanActions"
          :multiple="true"
          v-for="item in stepConstants.diversificationPlanActions.items"
          :key="item.value"
          :value="item.value"
          :label="item.label"
          :readonly="!payload.hasDiversificationPlan"
          :disabled="!payload.hasDiversificationPlan"
        />
      </fieldset>
    </div>
    <DsfrRadio
      v-else-if="stepUrlSlug === 'service'"
      :label="stepConstants.serviceType.title"
      :items="stepConstants.serviceType.items"
      v-model="payload.serviceType"
      hide-details
      optional
    />
    <div v-else-if="stepUrlSlug === 'menu'">
      <LastYearAutofillOption
        :canteen="canteen"
        :diagnostic="diagnostic"
        :fields="fields"
        @tunnel-autofill="onTunnelAutofill"
        class="mb-xs-6 mb-xl-16"
      />
      <DsfrRadio
        :label="stepConstants.vegetarianWeeklyRecurrence.title"
        :items="stepConstants.vegetarianWeeklyRecurrence.items"
        v-model="payload.vegetarianWeeklyRecurrence"
        hide-details
        optional
      />
    </div>
    <fieldset v-else-if="stepUrlSlug === 'composition'">
      <legend class="text-left mb-2 mt-3">
        {{ stepConstants.vegetarianMenuBases.title }}
        <span class="fr-hint-text mt-2">Optionnel</span>
      </legend>
      <v-checkbox
        hide-details="auto"
        class="mt-2"
        v-model="payload.vegetarianMenuBases"
        :multiple="true"
        v-for="item in stepConstants.vegetarianMenuBases.items"
        :key="item.value"
        :value="item.value"
        :label="item.label"
      />
    </fieldset>
  </v-form>
</template>

<script>
import DsfrRadio from "@/components/DsfrRadio"
import LastYearAutofillOption from "../LastYearAutofillOption"
import Constants from "@/constants"
import { applicableDiagnosticRules } from "@/utils"

const stepList = [
  {
    title: "Mise en place d’actions de diversification des protéines",
    urlSlug: "plan",
  },
  {
    title: "Options proposées aux convives",
    urlSlug: "service",
  },
  {
    title: "Mise en place d’un menu végétarien",
    urlSlug: "menu",
  },
  {
    title: "Composition du plat végétarien principal",
    urlSlug: "composition",
  },
  {
    title: "Synthèse",
    isSynthesis: true,
    componentName: "DiversificationMeasureSummary",
    urlSlug: "complet",
  },
]

export default {
  name: "DiversificationMeasureSteps",
  props: {
    canteen: {
      type: Object,
      required: true,
    },
    diagnostic: {
      type: Object,
      required: true,
    },
    stepUrlSlug: {
      type: String,
    },
  },
  components: { DsfrRadio, LastYearAutofillOption },
  data() {
    return {
      stepConstants: Constants.DiversificationMeasureStep,
      payload: {},
      fields: [
        "hasDiversificationPlan",
        "diversificationPlanActions",
        "serviceType",
        "vegetarianWeeklyRecurrence",
        "vegetarianMenuBases",
      ],
    }
  },
  computed: {
    steps() {
      // filter steps: init
      let idx
      let steps = JSON.parse(JSON.stringify(stepList))
      // - hide plan step if no diversification plan
      const applicableRules = applicableDiagnosticRules(this.canteen)
      if (!applicableRules.hasDiversificationPlan) {
        idx = steps.findIndex((step) => step.urlSlug === "plan")
        if (idx > -1) steps.splice(idx, 1)
      }
      // - 2024-12: hide options step (replaced with service step)
      // - hide options & composition steps if no vegetarian menu
      if (this.payload.vegetarianWeeklyRecurrence === "NEVER") {
        idx = steps.findIndex((step) => step.urlSlug === "options")
        if (idx > -1) steps.splice(idx, 1)
        idx = steps.findIndex((step) => step.urlSlug === "composition")
        if (idx > -1) steps.splice(idx, 1)
      }
      return steps
    },
    step() {
      const step = this.stepUrlSlug && this.steps.find((step) => step.urlSlug === this.stepUrlSlug)
      return step || this.steps[0]
    },
  },
  methods: {
    updatePayload() {
      this.$emit("update-payload", { payload: this.payload, formIsValid: true })
    },
    initialisePayload() {
      const payload = {}
      this.fields.forEach((f) => (payload[f] = this.diagnostic[f]))
      this.$set(this, "payload", payload)
    },
    onTunnelAutofill(e) {
      this.$set(this, "payload", e.payload)
      this.$emit("tunnel-autofill", e)
    },
  },
  mounted() {
    this.initialisePayload()
    this.updatePayload()
  },
  watch: {
    payload: {
      handler() {
        this.updatePayload()
      },
      deep: true,
    },
    steps: {
      handler() {
        this.$emit("update-steps", this.steps)
      },
      deep: true,
    },
    $route() {
      // it is possible to navigate without saving.
      // So must initialise payload every step to avoid saving something unintentionally
      this.initialisePayload()
    },
  },
}
</script>
