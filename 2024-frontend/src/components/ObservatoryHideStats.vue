<script setup>
import { ref } from "vue"
const props = defineProps(["reportNotPublished", "campaignNotFound"])
const text = ref(props.reportNotPublished || props.campaignNotFound)
</script>

<template>
  <DsfrHighlight :text="text" class="fr-ml-0" />
</template>
