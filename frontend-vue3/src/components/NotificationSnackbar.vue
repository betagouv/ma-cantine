<template>
  <v-snackbar class="notification-snackbar" v-model="show" :color="color" :location="location" timeout="-1">
    <div class="d-flex">
      <v-icon small class="mr-3" width="20" @click="$store.dispatch('removeNotification')">{{ icon }}</v-icon>
      <div class="flex-grow-1 d-flex flex-column justify-center">
        <p class="text-body-1 font-weight-bold mb-0" v-if="notification.title">
          {{ notification.title }}
        </p>
        <p class="body-2 mb-0" v-if="notification.message">
          {{ notification.message }}
        </p>
      </div>
      <v-btn
        class="ml-3"
        @click="$store.dispatch('removeNotification')"
        icon="mdi-close"
        density="compact"
        variant="flat"
        :color="color"
      ></v-btn>
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
  name: "NotificationSnackbar",
  computed: {
    color() {
      const colors = { success: "green", error: "red", warning: "amber darken-2" }
      if (!this.show) return "white"
      return Object.prototype.hasOwnProperty.call(colors, this.notification.status)
        ? colors[this.notification.status]
        : "indigo"
    },
    icon() {
      if (!this.notification || !this.notification.status) return null
      const icons = { success: "mdi-check-bold", error: "mdi-close-circle", warning: "mdi-alert" }
      return Object.prototype.hasOwnProperty.call(icons, this.notification.status)
        ? icons[this.notification.status]
        : null
    },
    isMobile() {
      return this.$vuetify.display.mobile
    },
    notification() {
      return this.$store.state.notification
    },
    show() {
      return !!this.notification.message || !!this.notification.title
    },
    location() {
      return (this.isMobile && "bottom") || "top right"
    },
  },
}
</script>
