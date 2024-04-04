<template>
  <!-- TODO: check that the type/name/autocomplete values are good -->
  <DsfrTextField
    v-bind="$attrs"
    v-on="$listeners"
    type="telephone"
    name="telephone"
    autocomplete="telephone"
    spellcheck="false"
    validate-on-blur
    :rules="rules || [validators.isEmptyOrPhoneNumber]"
  >
    <template v-slot:label>
      <span :class="labelClasses || 'fr-label mb-1'">{{ label || "Numéro téléphone" }}</span>
      <span class="fr-hint-text">Format attendu : 07 01 02 03 04</span>
      <span class="fr-hint-text">Optionnel</span>
    </template>
  </DsfrTextField>
</template>

<script>
import DsfrTextField from "./DsfrTextField"
import validators from "@/validators"

export default {
  name: "DsfrPhoneNumber",
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
