<script setup>
defineProps(["opened"])
const emit = defineEmits(["close"])
</script>

<template>
  <DsfrModal
    class="canteen-modal-export"
    :opened="opened"
    title="Export des informations de mes cantines"
    @close="emit('close')"
  >
    <p>
      Cet export contient l'ensemble des données d’information relatives aux cantines dont vous gérez.
      Vous pourrez modifier ce fichier et le ré-utiliser tel quel dans le module d’import “Modifier des cantines” pour mettre à jour vos informations en masse.
    </p>
    <p class="ma-cantine--bold">Pour rappel, pour modifier les cantines via imports ou créer des bilans, vous devez être gestionnaire de celles-ci.</p>
    <div class="fr-grid-row fr-grid-row--gutters fr-grid-row--center fr-grid-row--middle fr-mt-4w">
      <div class="fr-col-12 fr-col-md-2 fr-h2 ma-cantine--text-center">
        <VIcon class="canteen-modal-export__icon" name="mdi-microsoft-excel" scale="1.5"/>
      </div>
      <div class="fr-col-12 fr-col-md-10">
        <DsfrFileDownload
          href="api/v1/export-cantines.xlsx"
          title="Télécharger l'export de la liste les cantines dont vous êtes gestionnaire sur la plateforme ma cantine"
          target="_blank"
          size="Taille du fichier inconnue"
          format="Excel (.xlsx)"
          download="export-cantines.xlsx"
        />
      </div>
    </div>
  </DsfrModal>
</template>

<style lang="scss" scoped>
.canteen-modal-export {
  &__icon {
    color: var(--text-action-high-blue-france) !important;
  }
}
</style>
