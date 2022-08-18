<template>
  <v-pagination
    prev-icon="$arrow-left-s-line"
    next-icon="$arrow-right-s-line"
    v-bind="$attrs"
    v-on="$listeners"
    @input="(v) => $emit('input', v)"
    previous-aria-label="Page précédente"
    current-page-aria-label="Page actuelle"
    next-aria-label="Page suivante"
  ></v-pagination>
</template>

<script>
export default {
  inheritAttrs: false,
}
</script>

<style scoped>
::v-deep .v-pagination__item,
::v-deep .v-pagination__navigation {
  border-radius: 0 !important;
  box-shadow: none !important;
}

::v-deep .v-pagination__item:not(.v-pagination__item--active):hover,
::v-deep .v-pagination__navigation:hover {
  background-color: #eeeeee !important;
}
</style>
