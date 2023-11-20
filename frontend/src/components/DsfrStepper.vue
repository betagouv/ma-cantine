<template>
  <div>
    <div class="fr-stepper">
      <h1 class="fr-stepper__title mb-4">
        <span class="fr-stepper__state">Étape {{ currentStepIdx + 1 }} sur {{ stepTotal }}</span>
        {{ step.title }}
      </h1>
      <v-row class="fr-stepper__steps ma-0" :data-fr-current-step="currentStepIdx + 1" :data-fr-steps="stepTotal">
        <v-col v-for="(_, idx) in steps" :key="idx" :class="stepClass(idx)" />
      </v-row>
      <p v-if="nextStep" class="fr-stepper__details mt-4 mb-0">
        <span class="font-weight-bold">Étape suivante :</span>
        {{ nextStep.title }}
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: "DsfrStepper",
  props: {
    steps: {
      type: Array,
      required: true,
    },
    currentStepIdx: {
      type: Number,
      required: true,
    },
  },
  computed: {
    stepTotal() {
      return this.steps.length
    },
    step() {
      return this.steps[this.currentStepIdx]
    },
    nextStep() {
      if (this.currentStepIdx === this.steps.length - 1) return null
      return this.steps[this.currentStepIdx + 1]
    },
  },
  methods: {
    stepClass(idx) {
      const margins = idx === 0 ? "mr-1" : idx === this.stepTotal - 1 ? "ml-1" : "mx-1"
      return `${margins} mc-stepper__step ${idx <= this.currentStepIdx ? "completed" : "future"}`
    },
  },
}
</script>

<style>
/* DSFR STEPPER */
.fr-stepper {
  --title-spacing: 0;
  --text-spacing: 0;
  display: flex;
  flex-direction: column;
  margin-bottom: 2rem;
}
.fr-stepper__title {
  --title-spacing: 0 0 0.75rem 0;
  --text-spacing: 0 0 0.75rem 0;
  color: #161616;
  /* color: var(--text-title-grey); */
  font-size: 1.125rem;
  font-weight: 700;
  line-height: 1.5rem;
}
.fr-stepper__state {
  --title-spacing: 0 0 0.25rem 0;
  --text-spacing: 0 0 0.25rem 0;
  color: #666;
  /* color: var(--text-mention-grey); */
  font-size: 0.875rem;
  font-weight: 400;
  line-height: 1.5rem;
}
.fr-stepper__state:after {
  content: "\a";
  line-height: 2rem;
  white-space: pre;
}
.fr-stepper__details {
  color: #666;
  /* color: var(--text-mention-grey); */
  font-size: 0.75rem;
  line-height: 1.25rem;
  margin-top: 0.75rem;
}
/* .fr-stepper__steps {
  height: 6px;
} */
.mc-stepper__step {
  height: 6px;
  padding: 0;
}
.mc-stepper__step.completed {
  background-color: #000091;
}
.mc-stepper__step.future {
  background-color: #eee;
}
</style>
