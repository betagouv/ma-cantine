<template>
  <DsfrTextField
    ref="text-field"
    :placeholder="$attrs['placeholder'] || 'Rechercher'"
    v-bind="$attrs"
    clearable
    @click:clear="clearAction"
    @keyup.enter="searchAction"
    @update:model-value="(v) => $emit('input', v)"
  >
    <template #append>
      <v-btn
        color="primary"
        class="ml-n4 search-button"
        width="45px"
        min-width="45px"
        max-width="45px"
        height="45px"
        aria-label="Rechercher"
        @click="searchAction"
      >
        <v-icon>$search-line</v-icon>
      </v-btn>
    </template>
  </DsfrTextField>
</template>

<script>
import DsfrTextField from "@/components/DsfrTextField"

export default {
  components: { DsfrTextField },
  inheritAttrs: false,
  props: {
    searchAction: {
      type: Function,
      default() {},
    },
    clearAction: {
      type: Function,
      default() {},
    },
  },
  emits: ["input"],
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
