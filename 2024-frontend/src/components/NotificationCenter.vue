<script setup>
import { computed } from "vue"

import { useRootStore } from "@/stores/root"
const store = useRootStore()

const notifications = computed(() => store.notifications)

const onClose = (notification) => {
  store.removeNotification(notification)
}
</script>

<template>
  <div id="notification-center" class="fr-col-12 fr-col-sm-8 fr-col-md-6 fr-col-lg-4">
    <DsfrAlert
      v-for="notification in notifications"
      :key="notification.id"
      :id="notification.id"
      :type="notification.status"
      :title="notification.title"
      :description="notification.message"
      :closeable="true"
      @close="onClose(notification)"
      role="alert"
      class="alert"
    />
  </div>
</template>

<style scoped>
#notification-center {
  position: fixed;
  z-index: 1000;
  height: fit-content;
  right: 0;
  top: 0;
}

.alert {
  background-color: #fff;
}
</style>
