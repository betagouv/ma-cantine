<script setup>
defineProps(["open"])
defineEmits(["close"])
</script>
<template>
  <DsfrModal :opened="open" title="Ajouter un restaurant satellite" @close="$emit('close')" size="xl">
    <p>Pour ajouter une cantine à votre groupe cette dernière doit : être enregistrée sur la plateforme, être de type "Restaurant satellite", ne doit pas déjà être associée à un groupe.</p>
  </DsfrModal>
</template>
