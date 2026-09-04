<template>
  <DsfrTextField
    v-bind="$attrs"
    v-on="$listeners"
    type="email"
    name="email"
    autocomplete="email"
    spellcheck="false"
    validate-on-blur
    :rules="rules || [validators.email]"
  >
    <template v-slot:label>
      <span :class="labelClasses || 'fr-label mb-1'">{{ label || "Votre adresse électronique" }}</span>
      <span class="fr-hint-text">Format attendu : nom@domaine.fr</span>
    </template>
  </DsfrTextField>
</template>

<script>
import DsfrTextField from "./DsfrTextField"
import validators from "@/validators"

export default {
  name: "DsfrEmail",
  props: {
    rules: {
      type: Array,
      required: false,
    },
    label: {
      type: String,
      required: false,
    },
    labelClasses: {
      type: String,
      required: false,
    },
  },
  components: { DsfrTextField },
  computed: {
    validators() {
      return validators
    },
  },
}
</script>
