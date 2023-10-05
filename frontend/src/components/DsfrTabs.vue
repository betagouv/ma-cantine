<template>
  <div>
    <v-tabs v-bind="$attrs" v-model="tab" v-on="$listeners">
      <slot name="tabs" />
    </v-tabs>

    <v-tabs-items v-model="tab">
      <slot name="items" />
    </v-tabs-items>
  </div>
</template>

<script>
export default {
  inheritAttrs: false,
  props: ["value"],
  data() {
    return {
      tab: null,
    }
  },
}
</script>

<style scoped>
.v-tabs >>> .v-tab:not(.selected) {
  background-color: rgb(227, 227, 253);
  color: rgb(58, 58, 58) !important;
}

.v-tabs >>> .v-tab.selected {
  border-left: 1px solid #ccc;
  border-right: 1px solid #ccc;
  /* transition: none !important; */
}
.v-tabs >>> .v-tab.selected::before {
  background-color: inherit;
  transition: none !important;
}

.v-tabs >>> .v-tabs-slider-wrapper {
  top: 0 !important;
  bottom: auto;
  margin-left: 1px;
}

.v-tabs >>> .v-tab {
  letter-spacing: normal;
}
</style>
