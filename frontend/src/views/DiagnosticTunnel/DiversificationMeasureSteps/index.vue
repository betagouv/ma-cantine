<template>
  <v-form @submit.prevent>
    <div v-if="stepUrlSlug === 'menu'">
      <LastYearAutofillOption
        :canteen="canteen"
        :diagnostic="diagnostic"
        :fields="fields"
        @tunnel-autofill="onTunnelAutofill"
        class="mb-xs-6 mb-xl-16"
      />
      <DsfrRadio
        label="J'ai mis en place un menu végétarien dans ma cantine :"
        :items="frequency"
        v-model="payload.vegetarianWeeklyRecurrence"
        @change="calculateSteps"
        hide-details
        optional
      />
    </div>
    <DsfrRadio
      v-else-if="stepUrlSlug === 'options'"
      label="Le menu végétarien proposé est :"
      :items="menuTypes"
      v-model="payload.vegetarianMenuType"
      hide-details
      optional
    />
    <fieldset v-else-if="stepUrlSlug === 'composition'">
      <legend class="text-left mb-2 mt-3">
        Le plat principal de mon menu végétarien est majoritairement à base de :
        <span class="fr-hint-text mt-2">Optionnel</span>
      </legend>
      <v-checkbox
        hide-details="auto"
        class="mt-2"
        v-model="payload.vegetarianMenuBases"
        :multiple="true"
        v-for="item in menuBases"
        :key="item.value"
        :value="item.value"
        :label="item.label"
      />
    </fieldset>
    <div v-else-if="stepUrlSlug === 'plan'">
      <DsfrRadio
        label="J'ai mis en place un plan pluriannuel de diversification des protéines incluant des alternatives à base de
          protéines végétales"
        v-model="payload.hasDiversificationPlan"
        hide-details
        optionsRow
        yesNo
        optional
      />
      <fieldset class="my-3">
        <legend class="text-left mb-1 mt-3" :class="{ 'grey--text': !payload.hasDiversificationPlan }">
          Ce plan comporte, par exemple, les actions suivantes (voir guide du CNRC) :
          <span :class="`fr-hint-text mt-2 ${!payload.hasDiversificationPlan && 'grey--text'}`">Optionnel</span>
        </legend>
        <v-checkbox
          hide-details="auto"
          class="mt-1"
          v-model="payload.diversificationPlanActions"
          :multiple="true"
          v-for="item in diversificationPlanActions"
          :key="item.value"
          :value="item.value"
          :label="item.label"
          :readonly="!payload.hasDiversificationPlan"
          :disabled="!payload.hasDiversificationPlan"
        />
      </fieldset>
    </div>
  </v-form>
</template>

<script>
import DsfrRadio from "@/components/DsfrRadio"
import LastYearAutofillOption from "../LastYearAutofillOption"
import Constants from "@/constants"
import { applicableDiagnosticRules } from "@/utils"

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
      steps: [],
      diversificationPlanActions: [
        {
          label: "Les plats et les produits (diversification, gestion des quantités, recette traditionnelle, goût...)",
          value: "PRODUCTS",
        },
        {
          label: "La manière dont les aliments sont présentés aux convives (visuellement attrayants)",
          value: "PRESENTATION",
        },
        {
          label: "La manière dont les menus sont conçus en soulignant attributs positifs des plats",
          value: "MENU",
        },
        {
          label: "La mise en avant des produits (plats recommandés, dégustation, mode de production...)",
          value: "PROMOTION",
        },
        {
          label:
            "La formation du personnel, la sensibilisation des convives, l’investissement dans de nouveaux équipements de cuisine...",
          value: "TRAINING",
        },
      ],
      frequency: Constants.VegetarianRecurrence,
      menuTypes: Constants.VegetarianMenuTypes,
      menuBases: Constants.VegetarianMenuBases,
      payload: {},
      fields: [
        "vegetarianWeeklyRecurrence",
        "vegetarianMenuType",
        "vegetarianMenuBases",
        "hasDiversificationPlan",
        "diversificationPlanActions",
      ],
    }
  },
  computed: {
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
    calculateSteps() {
      const steps = []
      const applicableRules = applicableDiagnosticRules(this.canteen)
      if (applicableRules.hasDiversificationPlan) {
        steps.push({
          title: "Mise en place d’actions de diversification des protéines",
          urlSlug: "plan",
        })
      }
      steps.push({
        title: "Mise en place d’un menu végétarien",
        urlSlug: "menu",
      })
      if (this.payload.vegetarianWeeklyRecurrence !== "NEVER") {
        const menuDetailsSteps = [
          {
            title: "Options proposées aux convives",
            urlSlug: "options",
          },
          {
            title: "Composition du plat végétarien principal",
            urlSlug: "composition",
          },
        ]
        steps.push(...menuDetailsSteps)
      }
      steps.push({
        title: "Synthèse",
        isSynthesis: true,
        componentName: "DiversificationMeasureSummary",
        urlSlug: "complet",
      })
      this.steps = steps
      this.$emit("update-steps", this.steps)
    },
    onTunnelAutofill(e) {
      this.$set(this, "payload", e.payload)
      this.$emit("tunnel-autofill", e)
    },
  },
  mounted() {
    this.initialisePayload()
    this.updatePayload()
    this.calculateSteps()
  },
  watch: {
    payload: {
      handler() {
        this.updatePayload()
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
