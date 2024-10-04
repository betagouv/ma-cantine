<template>
  <v-alert
    border="left"
    colored-border
    :icon="icon"
    :color="$attrs['color'] || '#6a6af4'"
    v-bind="$attrs"
    v-on="$listeners"
    @input="(v) => $emit('input', v)"
    style="background: #eeeeee;"
  >
    <!-- TODO: consider using a different component if we don't want role="alert" -->
    <slot />
  </v-alert>
</template>

<script>
export default {
  inheritAttrs: false,
  props: {
    noIcon: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    reformatIcon() {
      const icon = this.$el.getElementsByClassName("v-alert__icon")[0]
      icon.style.color = "#161616"
    },
  },
  computed: {
    icon() {
      return this.noIcon ? " " : this.$attrs["icon"] || "mdi-information-outline"
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
