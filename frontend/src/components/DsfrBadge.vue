<template>
  <v-chip
    v-bind="$attrs"
    v-on="$listeners"
    :color="modes[mode].backgroundColor"
    :style="`border-radius: 4px !important; color: ${modes[mode].color}; width: fit-content;`"
    small
    label
  >
    <v-icon v-if="showIcon" :color="modes[mode].color" small class="mr-2">{{ badgeIcon }}</v-icon>
    <slot />
  </v-chip>
</template>

<script>
export default {
  name: "DsfrBadge",
  inheritAttrs: false,
  props: {
    mode: {
      type: String,
      default: "INFO",
    },
    icon: {
      type: String,
      optional: true,
    },
    showIcon: {
      type: Boolean,
      default: true,
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
        WARNING: {
          backgroundColor: "rgb(254, 235, 208)",
          color: "rgb(105, 82, 64)",
          icon: "$error-warning-fill",
        },
        SUCCESS: {
          backgroundColor: "rgb(184, 254, 201)",
          color: "rgb(24, 117, 60)",
          icon: "$checkbox-fill",
        },
        NEUTRAL: {
          color: "rgb(0, 0, 0)",
        },
      },
    }
  },
  computed: {
    badgeIcon() {
      return this.icon || this.modes[this.mode].icon
    },
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
