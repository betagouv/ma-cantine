<script setup>
import { onMounted, reactive, watch } from "vue"
import { useVuelidate } from "@vuelidate/core"
import { required, email } from "@vuelidate/validators"
import { formatError } from "@/utils.js"

defineProps(["stepUrlSlug"])

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
const emit = defineEmits(["update-steps", "provide-vuelidate", "update-payload"])

const payload = reactive({
  name: "",
  email: "",
})
const rules = {
  name: { required },
  email: { email },
}
const v$ = useVuelidate(rules, payload)

const updatePayload = () => {
  emit("update-payload", payload)
}

watch(payload, () => {
  updatePayload()
})

onMounted(() => {
  emit("update-steps", steps)
  emit("provide-vuelidate", v$)
})
</script>

<template>
  <div v-if="stepUrlSlug === 'example'">
    <p>This step allows for validation checking</p>
    <DsfrInputGroup
      v-model="payload.name"
      label="Nom"
      placeholder="Jean Dupont"
      label-visible
      hint="Indiquez votre nom"
      class="fr-mb-2w"
      :error-message="formatError(v$.name)"
    />
    <DsfrInputGroup
      v-model="payload.email"
      label="Email"
      label-visible
      class="fr-mb-2w"
      :error-message="formatError(v$.email)"
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
