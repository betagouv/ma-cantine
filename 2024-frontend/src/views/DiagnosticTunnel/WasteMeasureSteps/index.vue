<script setup>
import { onMounted } from "vue"

defineProps(["stepUrlSlug"])

const name = defineModel()

const steps = [
  {
    urlSlug: "example",
    title: "Step 1",
  },
  {
    urlSlug: "test",
    title: "Step 2",
  },
]
const emit = defineEmits(["update-steps"])
onMounted(() => {
  emit("update-steps", steps)
})
</script>

<template>
  <div v-if="stepUrlSlug === 'example'">
    <DsfrInput v-model="name" label="Nom" placeholder="Jean Dupont" label-visible required hint="Indiquez votre nom" />
  </div>
  <div v-else-if="stepUrlSlug === 'test'">
    <DsfrInput v-model="name" label="Autre champ" label-visible />
  </div>
  <div v-else>
    <p>Unknown step (shouldn't arrive here)</p>
  </div>
</template>
