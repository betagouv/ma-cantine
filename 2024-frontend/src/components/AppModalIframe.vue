<script setup>
import { computed } from "vue"

const props = defineProps(["opened", "title", "src"])
defineEmits(["close"])

const iframeSrc = computed(() => `${props.src}/reader/`)
</script>

<template>
  <DsfrModal :opened="opened" class="fr-modal--opened" @close="$emit('close')" size="xl">
    <template #default>
      <iframe :title="title" :src="iframeSrc" class="ma-cantine--modal-iframe" frameborder="0"></iframe>
    </template>
  </DsfrModal>
</template>
