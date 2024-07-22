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
    title: "A long step",
  },
  {
    urlSlug: "long2",
    title: "A second long step",
  },
]
const emit = defineEmits(["update-steps"])
onMounted(() => {
  emit("update-steps", steps)
})
</script>

<template>
  <div v-if="stepUrlSlug === 'example'">
    <DsfrInput
      v-model="name"
      label="Nom"
      placeholder="Jean Dupont"
      label-visible
      required
      hint="Indiquez votre nom"
      class="fr-mb-2w"
    />
  </div>
  <div v-else-if="stepUrlSlug === 'test'">
    <p>This is an example of a step that requires scrolling</p>
    <DsfrInput label="Autre champ" label-visible class="fr-mb-2w" />
    <DsfrInput label="Autre champ" label-visible class="fr-mb-2w" />
    <DsfrInput label="Autre champ" label-visible class="fr-mb-2w" />
    <DsfrInput label="Autre champ" label-visible class="fr-mb-2w" />
    <DsfrInput label="Autre champ" label-visible class="fr-mb-2w" />
    <DsfrInput label="Autre champ" label-visible class="fr-mb-2w" />
    <DsfrInput label="Autre champ" label-visible class="fr-mb-2w" />
    <DsfrInput label="Autre champ" label-visible class="fr-mb-2w" />
  </div>
  <div v-else-if="stepUrlSlug === 'long2'">
    <p>This is an example of a step that requires scrolling</p>
    <DsfrInput label="Autre champ" label-visible class="fr-mb-2w" />
    <DsfrInput label="Autre champ" label-visible class="fr-mb-2w" />
    <DsfrInput label="Autre champ" label-visible class="fr-mb-2w" />
    <DsfrInput label="Autre champ" label-visible class="fr-mb-2w" />
    <DsfrInput label="Autre champ" label-visible class="fr-mb-2w" />
    <DsfrInput label="Autre champ" label-visible class="fr-mb-2w" />
    <DsfrInput label="Autre champ" label-visible class="fr-mb-2w" />
    <DsfrInput label="Autre champ" label-visible class="fr-mb-2w" />
  </div>
  <div v-else>
    <p>Unknown step (shouldn't arrive here)</p>
  </div>
</template>
