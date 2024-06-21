<template>
  <DsfrTextField
    v-bind="$attrs"
    v-on="$listeners"
    label="Prénom et nom"
    autocomplete="name"
    spellcheck="false"
    :rules="rules || []"
  />
</template>

<script>
import DsfrTextField from "./DsfrTextField"

export default {
  name: "DsfrFullName",
  props: {
    rules: {
      type: Array,
      required: false,
    },
  },
  components: { DsfrTextField },
}
</script>
