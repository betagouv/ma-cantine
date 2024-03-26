<template>
  <DsfrTextField
    v-bind="$attrs"
    v-on="$listeners"
    ref="email"
    type="email"
    name="email"
    autocomplete="email"
    spellcheck="off"
    validate-on-blur
    :rules="[validators.email]"
  >
    <template v-slot:label>
      <span class="fr-label">Adresse électronique</span>
      <span class="fr-hint-text mt-1">Format attendu : nom@domaine.fr</span>
    </template>
  </DsfrTextField>
</template>

<script>
import DsfrTextField from "./DsfrTextField"
import validators from "@/validators"

export default {
  name: "DsfrEmail",
  components: { DsfrTextField },
  computed: {
    validators() {
      return validators
    },
    rules() {
      return [validators.email]
    },
  },
}
</script>
