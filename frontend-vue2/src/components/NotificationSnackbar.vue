<template>
  <v-snackbar class="notification-snackbar" timeout="-1" :color="color" :value="show" right>
    <div class="d-flex">
      <v-icon small class="mr-3" width="20">
        {{ icon }}
      </v-icon>
      <div class="flex-grow-1 d-flex flex-column justify-center white--text">
        <p class="text-body-1 font-weight-bold mb-0" v-if="notification.title">
          {{ notification.title }}
        </p>
        <p class="body-2 mb-0" v-if="notification.message">
          {{ notification.message }}
        </p>
      </div>
      <v-btn class="ml-3" @click="$store.dispatch('removeNotification', notification)" icon aria-label="Fermer">
        <v-icon color="white" width="20">$close-line</v-icon>
      </v-btn>
    </div>
    <div v-if="notification.undoMessage && notification.undoAction">
      <v-btn @click="notification.undoAction" color="white" class="primary--text">
        {{ notification.undoMessage }}
      </v-btn>
    </div>
  </v-snackbar>
</template>

<script>
export default {
  name: "Notification",
  props: ["notification"],
  computed: {
    color() {
      const colors = { success: "#18753c" /*success-425*/, error: "#ce0500" /*error-425*/ }
      if (!this.show) return "white"
      return Object.prototype.hasOwnProperty.call(colors, this.notification.status)
        ? colors[this.notification.status]
        : "#0063cb" // info-425
    },
    icon() {
      if (!this.notification || !this.notification.status) return null
      const icons = { success: "mdi-check-bold", error: "mdi-close-circle" }
      return Object.prototype.hasOwnProperty.call(icons, this.notification.status)
        ? icons[this.notification.status]
        : null
    },
    isMobile() {
      return this.$vuetify.breakpoint.mobile
    },
    show() {
      return !!this.notification.message || this.notification.title
    },
  },
}
</script>

<style scoped>
.notification-snackbar {
  position: relative;
  height: unset;
  width: unset;
}
</style>
