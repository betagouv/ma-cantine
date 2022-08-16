<template>
  <v-alert
    border="left"
    colored-border
    :icon="$attrs['icon'] || 'mdi-information-outline'"
    :color="$attrs['color'] || '#6a6af4'"
    v-bind="$attrs"
    v-on="$listeners"
    @input="(v) => $emit('input', v)"
    style="background: #eeeeee;"
  >
    <slot />
  </v-alert>
</template>

<script>
export default {
  inheritAttrs: false,
  methods: {
    reformatIcon() {
      const icon = this.$el.getElementsByClassName("v-alert__icon")[0]
      icon.style.color = "#161616"
    },
  },
  mounted() {
    this.reformatIcon()
  },
  updated() {
    this.reformatIcon()
  },
}
</script>

<style scoped>
::v-deep .v-alert__border {
  border-width: 2px;
}
</style>
