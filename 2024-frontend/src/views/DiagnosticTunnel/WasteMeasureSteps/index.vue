<script setup>
import { onMounted, reactive, watch, markRaw, defineProps } from "vue"
import MeasurementPeriod from "./MeasurementPeriod.vue"
import TotalWaste from "./TotalWaste.vue"
import WasteDistinction from "./WasteDistinction.vue"
import BreakdownBySource from "./BreakdownBySource.vue"

const props = defineProps(["stepUrlSlug"])

const steps = [
  {
    urlSlug: "periode",
    title: "Période de mesure",
    component: markRaw(MeasurementPeriod),
  },
  {
    urlSlug: "totale",
    title: "Masse totale de gaspillage",
    component: markRaw(TotalWaste),
  },
  {
    urlSlug: "distinction",
    title: "Distinction du gaspillage en fonction de la source",
    component: markRaw(WasteDistinction),
  },
  {
    urlSlug: "preparation",
    title: "Gaspillage lié aux excédents de préparation",
    component: markRaw(BreakdownBySource),
    componentData: { source: "preparation" },
  },
  {
    urlSlug: "non-servies",
    title: "Gaspillage lié aux denrées présentées aux convives mais non servies",
    component: markRaw(BreakdownBySource),
    componentData: { source: "unserved" },
  },
  {
    urlSlug: "reste-assiette",
    title: "Gaspillage lié au reste assiette",
    component: markRaw(BreakdownBySource),
    componentData: { source: "leftovers" },
  },
]
const emit = defineEmits(["update-steps", "provide-vuelidate", "update-payload"])

const provideVuelidate = (v$) => {
  emit("provide-vuelidate", v$)
}

const updatePayload = (payload) => {
  emit("update-payload", payload)
}

const state = reactive({
  step: steps[0],
})

watch(props, () => {
  state.step = steps.find((s) => s.urlSlug === props.stepUrlSlug)
})

onMounted(() => {
  emit("update-steps", steps)
})
</script>

<template>
  <component
    :is="state.step.component"
    @provide-vuelidate="provideVuelidate"
    @update-payload="updatePayload"
    :data="state.step.componentData"
  />
</template>
