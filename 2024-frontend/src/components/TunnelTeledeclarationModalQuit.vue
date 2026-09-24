<script setup>
defineProps(["opened"])
const emit = defineEmits(["close", "continue"])
</script>

<template>
  <DsfrModal
    :opened="opened"
    title="Êtes-vous sûr de vouloir quitter ?"
    @close="emit('close')"
  >
    <p>Certaines de vos données n'ont pas été enregistrées. Si vous quittez maintenant, elles seront perdues.</p>
    <div class="ma-cantine--flex-end">
      <DsfrButton
        secondary
        label="Non, revenir sur la page"
        icon="fr-icon-arrow-left-line"
        @click="emit('close')"
      />
      <DsfrButton
        primary
        icon="fr-icon-check-line"
        :icon-right="true"
        label="Oui, quitter sans enregistrer"
        @click="emit('continue')"
      />
    </div>
  </DsfrModal>
</template>
