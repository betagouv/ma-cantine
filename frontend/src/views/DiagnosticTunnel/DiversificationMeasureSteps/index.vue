<template>
  <fieldset v-if="stepUrlSlug === 'menu'">
    <legend class="text-left my-3">
      J'ai mis en place un menu végétarien dans ma cantine :
      <span class="fr-hint-text mt-2">Optionnel</span>
    </legend>
    <v-radio-group class="my-0" v-model="payload.vegetarianWeeklyRecurrence" hide-details @change="updatePayload">
      <v-radio v-for="item in frequency" :key="item.value" :label="item.label" :value="item.value"></v-radio>
    </v-radio-group>
  </fieldset>
  <fieldset v-else-if="stepUrlSlug === 'options'">
    <legend class="text-left my-3">
      Le menu végétarien proposé est :
      <span class="fr-hint-text mt-2">Optionnel</span>
    </legend>
    <v-radio-group class="my-0" v-model="payload.vegetarianMenuType" hide-details @change="updatePayload">
      <v-radio v-for="item in menuTypes" :key="item.value" :label="item.label" :value="item.value"></v-radio>
    </v-radio-group>
  </fieldset>
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
      @change="updatePayload"
    />
  </fieldset>
  <div v-else-if="stepUrlSlug === 'plan'">
    <fieldset>
      <legend class="text-left my-3">
        J'ai mis en place un plan pluriannuel de diversification des protéines incluant des alternatives à base de
        protéines végétales
      </legend>
      <v-radio-group class="my-0" v-model="payload.hasDiversificationPlan" hide-details @change="updatePayload">
        <v-row>
          <v-col>
            <v-radio label="Oui" :value="true"></v-radio>
          </v-col>
          <v-col>
            <v-radio label="Non" :value="false"></v-radio>
          </v-col>
        </v-row>
      </v-radio-group>
    </fieldset>
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
        @change="updatePayload"
      />
    </fieldset>
  </div>
  <component v-else :is="step.componentName" :canteen="canteen" :diagnostic="payload" />
</template>

<script>
import DiversificationMeasureSummary from "@/components/DiagnosticSummary/DiversificationMeasureSummary"
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
  components: {
    DiversificationMeasureSummary,
  },
  data() {
    const applicableRules = applicableDiagnosticRules(this.canteen)
    const steps = [
      {
        title: "Mise en place d’un menu végétarien",
        urlSlug: "menu",
      },
      {
        title: "Options proposées aux convives",
        urlSlug: "options",
      },
      {
        title: "Composition du plat végétarien principal",
        urlSlug: "composition",
      },
    ]
    if (applicableRules.hasDiversificationPlan) {
      steps.push({
        title: "Mise en place d’actions de diversification des protéines",
        urlSlug: "plan",
      })
    }
    return {
      steps: [
        ...steps,
        {
          title: "Synthèse",
          isSynthesis: true,
          componentName: "DiversificationMeasureSummary",
          urlSlug: "complet",
        },
      ],
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
      payload: {
        vegetarianWeeklyRecurrence: this.diagnostic.vegetarianWeeklyRecurrence,
        vegetarianMenuType: this.diagnostic.vegetarianMenuType,
        vegetarianMenuBases: this.diagnostic.vegetarianMenuBases,
        hasDiversificationPlan: this.diagnostic.hasDiversificationPlan,
        diversificationPlanActions: this.diagnostic.diversificationPlanActions,
      },
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
  },
  mounted() {
    this.$emit("update-steps", this.steps)
    this.updatePayload()
  },
}
</script>
