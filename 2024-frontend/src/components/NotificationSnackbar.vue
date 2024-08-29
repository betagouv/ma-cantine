<script setup>
import { useRootStore } from "@/stores/root"
const store = useRootStore()

const props = defineProps(["notification"])

const onClose = (notification) => {
  store.removeNotification(notification)
}
</script>

<template>
  <DsfrAlert
    :id="props.notification.id"
    :type="props.notification.status"
    :title="props.notification.title"
    :description="props.notification.message"
    :closeable="true"
    @close="onClose(props.notification)"
    role="alert"
    class="alert"
  />
</template>

<style scoped>
.alert {
  background-color: #fff;
}
</style>
