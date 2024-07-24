<script setup>
import { defineProps } from "vue"

const props = defineProps(["name"])

const options = [
  {
    label: "Oui",
    id: `${props.name}-yes`,
    value: true,
  },
  {
    label: "Non",
    id: `${props.name}-no`,
    value: false,
  },
]
</script>

<template>
  <DsfrRadioButtonSet v-bind="$attrs" :options="options" />
</template>
