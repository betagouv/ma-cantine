<script setup>
import IconMacaronBase from "@/components/IconMacaronBase.vue"

defineProps(["label", "status"])
</script>

<template>
  <IconMacaronBase v-slot="{ fill }" color="#A858A5" :label="label" :status="status">
    <path d="M54.1612 28.525V31.1596C54.1612 43.8411 47.0834 49.6016 38.3537 49.6016H35.8482C36.1275 45.6339 37.3631 43.2325 40.5878 40.3793C42.1739 38.9764 42.0395 38.1662 41.2583 38.6312C35.8785 41.8322 33.2071 46.1582 33.0885 53.0661L33.0846 53.5535H30.45C30.45 51.758 30.6028 50.1285 30.9058 48.6374C30.6028 46.9328 30.45 44.6196 30.45 41.6979C30.45 34.4225 36.3475 28.525 43.6229 28.525C46.2575 28.525 48.892 29.8423 54.1612 28.525Z" :fill="fill" />
  </IconMacaronBase>
</template>
