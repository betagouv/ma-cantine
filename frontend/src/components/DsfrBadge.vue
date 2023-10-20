<template>
  <v-chip
    v-bind="$attrs"
    v-on="$listeners"
    :color="modes[mode].backgroundColor"
    :style="`border-radius: 4px !important; color: ${modes[mode].color}`"
    small
    label
  >
    <v-icon :color="modes[mode].color" small class="mr-2">{{ modes[mode].icon }}</v-icon>
    <slot />
  </v-chip>
</template>

<script>
export default {
  inheritAttrs: false,
  props: {
    mode: {
      type: String,
      default: "INFO",
    },
  },
  data() {
    return {
      modes: {
        INFO: {
          backgroundColor: "rgb(232, 237, 255)",
          color: "rgb(0, 99, 203)",
          icon: "$information-fill",
        },
        ERROR: {
          backgroundColor: "rgb(255, 233, 233)",
          color: "rgb(206, 5, 0)",
          icon: "$error-warning-fill",
        },
        SUCCESS: {
          backgroundColor: "rgb(184, 254, 201)",
          color: "rgb(24, 117, 60)",
          icon: "$checkbox-fill",
        },
      },
    }
  },
}
</script>

<style scoped>
.v-chip {
  font-weight: 700;
  padding-left: 8px;
  padding-right: 8px;
}
</style>
