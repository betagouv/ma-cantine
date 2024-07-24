<script setup>
import { onMounted, reactive, watch, markRaw } from "vue"
import MeasurementPeriod from "./MeasurementPeriod.vue"
import TotalWaste from "./TotalWaste.vue"
import WasteDistinction from "./WasteDistinction.vue"
import PreparationExcess from "./PreparationExcess.vue"
import UnservedLeftovers from "./UnservedLeftovers.vue"
import PlateLeftovers from "./PlateLeftovers.vue"

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
    urlSlug: "excedents",
    title: "Gaspillage lié aux excédents de préparation",
    component: markRaw(PreparationExcess),
  },
  {
    urlSlug: "non-servies",
    title: "Gaspillage lié aux denrées présentées aux convives mais non servies",
    component: markRaw(UnservedLeftovers),
  },
  {
    urlSlug: "reste-assiette",
    title: "Gaspillage lié au reste assiette",
    component: markRaw(PlateLeftovers),
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
  <component :is="state.step.component" @provide-vuelidate="provideVuelidate" @update-payload="updatePayload" />
</template>
