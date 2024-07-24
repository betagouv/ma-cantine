<script setup>
import { onMounted, reactive, watch, computed } from "vue"
import { useVuelidate } from "@vuelidate/core"
import { helpers, required, email, sameAs } from "@vuelidate/validators"
import { formatError } from "@/utils.js"

const props = defineProps(["stepUrlSlug"])

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
  example: {
    name: "",
    email: "",
  },
  long2: {
    emailMatch: "",
  },
})

const emailForMatching = computed(() => payload.example.email)

const rules = {
  example: {
    name: { required },
    email: { email },
  },
  long2: {
    emailMatch: {
      sameAsEmail: helpers.withMessage(
        ({ $params }) => `Faut que ça soit le même que l'adresse mail ${$params.equalTo}`,
        sameAs(emailForMatching)
      ),
    },
  },
}
const v$ = useVuelidate(rules, payload)

const updatePayload = () => {
  emit("update-payload", payload[props.stepUrlSlug])
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
      v-model="payload[stepUrlSlug].name"
      label="Nom"
      placeholder="Jean Dupont"
      label-visible
      hint="Indiquez votre nom"
      class="fr-mb-2w"
      :error-message="formatError(v$[stepUrlSlug].name)"
    />
    <DsfrInputGroup
      v-model="payload[stepUrlSlug].email"
      label="Email"
      label-visible
      class="fr-mb-2w"
      :error-message="formatError(v$[stepUrlSlug].email)"
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
    <DsfrInputGroup
      v-model="payload[stepUrlSlug].emailMatch"
      label="Repeat email from first step"
      label-visible
      class="fr-mb-2w"
      :error-message="formatError(v$[stepUrlSlug].emailMatch)"
    />
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
