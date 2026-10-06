<script setup>
import IconMacaronBase from "@/components/IconMacaronBase.vue"

defineProps(["label", "status"])
</script>

<template>
  <IconMacaronBase v-slot="{ fill }" color="#A89500" :label="label" :status="status">
    <path d="M53.7476 42.5277C54.6414 42.5277 55.3117 42.8181 55.7586 43.3991C56.3395 43.98 56.63 44.6503 56.63 45.41L45.1676 49.7L35.18 46.8177V33.9477H37.8612L48.3181 37.8355C49.0778 38.1483 49.4576 38.6622 49.4576 39.3772C49.4576 39.8688 49.3236 40.2486 49.0555 40.5167C48.6533 40.9189 48.2064 41.12 47.7148 41.12H43.76L41.2798 40.1145L40.8776 41.3881L43.76 42.5277H53.7476ZM26.6 33.9477H32.2976V49.7H26.6V33.9477Z" :fill="fill" />
  </IconMacaronBase>
</template>
