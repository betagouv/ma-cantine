<script setup>
import { onMounted, reactive, watch, markRaw } from "vue"
import MeasurementPeriod from "./MeasurementPeriod.vue"
import TotalWaste from "./TotalWaste.vue"
import WasteDistinction from "./WasteDistinction.vue"
import BreakdownBySource from "./BreakdownBySource.vue"

const props = defineProps(["stepUrlSlug"])
const emit = defineEmits(["update-steps", "provide-vuelidate", "update-payload"])

const firstSteps = [
  {
    urlSlug: "periode",
    title: "Période de mesure",
    component: markRaw(MeasurementPeriod),
  },
  {
    urlSlug: "total",
    title: "Masse totale des déchets alimentaires",
    component: markRaw(TotalWaste),
  },
  {
    urlSlug: "distinction",
    title: "Distinction des déchets alimentaires en fonction de la source",
    component: markRaw(WasteDistinction),
  },
]
const breakdownSteps = [
  {
    urlSlug: "preparation",
    title: "Déchets alimentaires issus de la préparation",
    component: markRaw(BreakdownBySource),
    componentData: { source: "preparation" },
  },
  {
    urlSlug: "non-servies",
    title: "Déchets alimentaires liés aux denrées présentées aux convives mais non servies",
    component: markRaw(BreakdownBySource),
    componentData: { source: "unserved" },
  },
  {
    urlSlug: "reste-assiette",
    title: "Déchets alimentaires liés aux restes assiettes",
    component: markRaw(BreakdownBySource),
    componentData: { source: "leftovers" },
  },
]
const steps = firstSteps.concat(breakdownSteps)

const state = reactive({
  step: steps[0],
})

watch(props, () => {
  state.step = steps.find((s) => s.urlSlug === props.stepUrlSlug)
})

onMounted(() => {
  emit("update-steps", steps)
})

const provideVuelidate = (v$) => {
  emit("provide-vuelidate", v$)
}

const updatePayload = (payload) => {
  emit("update-payload", payload)
  if (payload.isSortedBySource === false) {
    emit("update-steps", firstSteps)
  } else if (payload.isSortedBySource === true) {
    emit("update-steps", steps)
  }
}
</script>

<template>
  <component
    :is="state.step.component"
    @provide-vuelidate="provideVuelidate"
    @update-payload="updatePayload"
    :data="state.step.componentData"
  />
</template>
