<template>
  <DsfrTextField
    :placeholder="$attrs['placeholder'] || 'Rechercher'"
    v-bind="$attrs"
    v-on="$listeners"
    @input="(v) => $emit('input', v)"
    clearable
    @click:clear="clearAction"
    @keyup.enter="searchAction"
    ref="text-field"
  >
    <template v-slot:append>
      <v-btn
        color="primary"
        class="mr-n3 search-button"
        width="40px"
        min-width="40px"
        max-width="40px"
        height="40px"
        @click="searchAction"
        aria-label="Rechercher"
      >
        <v-icon>$search-line</v-icon>
      </v-btn>
    </template>
  </DsfrTextField>
</template>

<script>
import DsfrTextField from "@/components/DsfrTextField"

export default {
  inheritAttrs: false,
  components: { DsfrTextField },
  props: ["searchAction", "clearAction"],
  computed: {
    lazyValue() {
      return this.$refs["text-field"].lazyValue
    },
    value() {
      return this.$refs["text-field"].value
    },
  },
  methods: {
    validate() {
      return this.$refs["text-field"].validate()
    },
  },
}
</script>

<style scoped>
.search-button {
  border-radius: 0 4px 0 0 !important;
}
</style>
