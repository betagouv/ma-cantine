<template>
  <v-form v-model="formIsValid" @submit.prevent>
    <div v-if="stepUrlSlug === 'contenants-alimentaires'">
      <LastYearAutofillOption
        :canteen="canteen"
        :diagnostic="diagnostic"
        :fields="fields"
        @tunnel-autofill="onTunnelAutofill"
        class="mb-xs-6 mb-xl-16"
      />
      <DsfrRadio
        label="Je n’utilise plus de contenants alimentaires de cuisson / de réchauffe en plastique"
        v-model="payload.cookingPlasticSubstituted"
        hide-details
        optional
        :items="boolOptions"
      />
      <DsfrRadio
        label="Je n’utilise plus de contenants alimentaires de service en plastique"
        v-model="payload.servingPlasticSubstituted"
        hide-details
        optional
        :items="boolOptions"
        class="mt-8"
      />
    </div>
    <div v-else-if="stepUrlSlug === 'ustensils-et-contenants'">
      <DsfrRadio
        label="Je ne mets plus à disposition des convives des bouteilles d’eau plate en plastique"
        v-model="payload.plasticBottlesSubstituted"
        hide-details
        optional
        :items="boolOptions"
      />
      <DsfrRadio
        label="Je ne mets plus à disposition des convives des ustensiles à usage unique en matière plastique"
        v-model="payload.plasticTablewareSubstituted"
        hide-details
        optional
        :items="boolOptions"
        class="mt-8"
      />
    </div>
    <component v-else :is="step.componentName" :canteen="canteen" :diagnostic="payload" />
  </v-form>
</template>

<script>
import LastYearAutofillOption from "../LastYearAutofillOption"
import DsfrRadio from "@/components/DsfrRadio"

export default {
  name: "NoPlasticMeasureSteps",
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
  components: { LastYearAutofillOption, DsfrRadio },
  data() {
    return {
      formIsValid: true,
      steps: [
        {
          title: "Substitution des contenants alimentaires en plastique",
          urlSlug: "contenants-alimentaires",
        },
        {
          title: "Mise à disposition des convives d’ustensiles et contenants à usage unique",
          urlSlug: "ustensils-et-contenants",
        },
        {
          title: "Synthèse",
          isSynthesis: true,
          componentName: "NoPlasticMeasureSummary",
          urlSlug: "complet",
        },
      ],
      boolOptions: [
        {
          label: "Vrai",
          value: true,
        },
        {
          label: "Faux",
          value: false,
        },
      ],
      payload: {},
      fields: [
        "cookingPlasticSubstituted",
        "servingPlasticSubstituted",
        "plasticBottlesSubstituted",
        "plasticTablewareSubstituted",
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
    onTunnelAutofill(e) {
      this.$set(this, "payload", e.payload)
      this.$emit("tunnel-autofill", e)
    },
  },
  mounted() {
    this.$emit("update-steps", this.steps)
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
    formIsValid() {
      this.updatePayload()
    },
    $route() {
      // it is possible to navigate without saving.
      // So must initialise payload every step to avoid saving something unintentionally
      this.initialisePayload()
    },
  },
}
</script>
