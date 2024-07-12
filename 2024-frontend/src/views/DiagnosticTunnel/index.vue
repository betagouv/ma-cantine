<script setup>
const props = defineProps(["canteenUrlComponent", "year", "measureId", "étape"])

// TODO: get steps from child tunnel component
const steps = [
  {
    id: "example",
    title: "Step 1",
  },
  {
    id: "test",
    title: "Step 2",
  },
]
const stepTitles = steps.map((s) => s.title)
const currentStep = (steps.findIndex((s) => s.id === props.étape) || 0) + 1
</script>

<template>
  <!-- TODO: mobile view optimisations -->
  <div class="tunnel">
    <div class="fr-container fr-pt-2w">
      <!-- TODO: tunnel icons -->
      <!-- TODO: save and quit -->
      <DsfrStepper :steps="stepTitles" :currentStep />
    </div>
    <div class="body">
      <div class="step fr-container fr-py-2w">
        <!-- TODO: setup steps in child folder -->
        <DsfrInput
          v-model="name"
          label="Nom"
          placeholder="Jean Dupont"
          label-visible
          required
          hint="Indiquez votre nom"
        />
      </div>
      <!-- TODO: setup synthesis -->
    </div>
    <div class="footer">
      <div class="content fr-container fr-grid-row fr-grid-row--right fr-p-2w">
        <!-- TODO: next tab text on synthesis view -->
        <!-- TODO: previous step link -->
        <DsfrButton label="Sauvegarder et continuer" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.tunnel {
  display: flex;
  flex-direction: column;
}
.tunnel,
.tunnel .footer {
  width: 100%;
  background-color: #f5f5fe;
}
.tunnel .body {
  overflow-y: scroll;
  overflow-x: hidden;
  background: #fff;
  flex-grow: 1;
}
.tunnel .footer {
  position: absolute;
  bottom: 0;
}
.scroll {
  overflow-y: scroll;
  overflow-x: hidden;
}
</style>
