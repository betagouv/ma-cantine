<script setup>
defineProps(["opened"])
const emit = defineEmits(["close"])
</script>

<template>
  <DsfrModal
    :opened="opened"
    title="Export des informations de mes cantines"
    @close="emit('close')"
  >
    <p>
      Cet export contient l'ensemble des données d’information relatives aux cantines dont vous gérez.
      Vous pourrez modifier ce fichier et le ré-utiliser tel quel dans le module d’import “Modifier des cantines” pour mettre à jour vos informations en masse.
    </p>
    <DsfrHighlight text="Pour rappel, pour modifier les cantines via imports ou créer des bilans, vous devez être gestionnaire de celles-ci." class="fr-ml-0"/>
  </DsfrModal>
</template>
