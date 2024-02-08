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
      <fieldset>
        <legend class="mb-3">
          Je n’utilise plus de contenants alimentaires de cuisson / de réchauffe en plastique
        </legend>
        <v-radio-group class="my-0" v-model="payload.cookingPlasticSubstituted" hide-details>
          <v-radio v-for="item in boolOptions" :key="item.value" :label="item.label" :value="item.value"></v-radio>
        </v-radio-group>
      </fieldset>
      <fieldset class="mt-8">
        <legend class="mb-3">
          Je n’utilise plus de contenants alimentaires de service en plastique
        </legend>
        <v-radio-group class="my-0" v-model="payload.servingPlasticSubstituted" hide-details>
          <v-radio v-for="item in boolOptions" :key="item.value" :label="item.label" :value="item.value"></v-radio>
        </v-radio-group>
      </fieldset>
    </div>
    <div v-else-if="stepUrlSlug === 'ustensils-et-contenants'">
      <fieldset>
        <legend class="mb-3">
          Je ne mets plus à disposition des convives des bouteilles d’eau plate en plastique
        </legend>
        <v-radio-group class="my-0" v-model="payload.plasticBottlesSubstituted" hide-details>
          <v-radio v-for="item in boolOptions" :key="item.value" :label="item.label" :value="item.value"></v-radio>
        </v-radio-group>
      </fieldset>
      <fieldset class="mt-8">
        <legend class="mb-3">
          Je ne mets plus à disposition des convives des ustensiles à usage unique en matière plastique
        </legend>
        <v-radio-group class="my-0" v-model="payload.plasticTablewareSubstituted" hide-details>
          <v-radio v-for="item in boolOptions" :key="item.value" :label="item.label" :value="item.value"></v-radio>
        </v-radio-group>
      </fieldset>
    </div>
    <component v-else :is="step.componentName" :canteen="canteen" :diagnostic="payload" />
  </v-form>
</template>

<script>
import LastYearAutofillOption from "../LastYearAutofillOption"

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
  components: { LastYearAutofillOption },
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
      this.$emit("tunnel-autofill", { payload: this.payload })
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
