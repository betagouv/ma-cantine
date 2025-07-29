<script setup>
import { computed } from "vue"

/* Props */
const props = defineProps(["canteensCount", "teledeclarationsCount"])

/* Teledeclaration */
const percent = computed(() => Math.round(props.teledeclarationsCount / props.canteensCount))
const teledeclarationTitle = computed(() =>
  props.teledeclarationsCount <= 1 ? "site télédéclaré" : "sites télédéclarés"
)

/* Tile */
const titleImgSrc = "/static/images/picto-dsfr/school.svg"
</script>
<template>
  <ul class="observatory-results-top ma-cantine--unstyled-list fr-grid-row fr-grid-row--gutters">
    <li class="fr-col-4">
      <div class="observatory-results-top__card fr-card fr-p-4w">
        <p class="fr-h5 fr-mb-1w">{{ canteensCount }}</p>
        <p class="fr-mb-2w">Nombre de cantines</p>
        <p class="fr-text--xs fr-mb-0">
          Au {date du jour} si avant fin de TD
          <br />
          Au {fin de campagne} 2025 si après fin TD
        </p>
      </div>
    </li>
    <li class="fr-col-4">
      <div class="observatory-results-top__card fr-card fr-p-4w">
        <p class="fr-h5 fr-mb-1w">{{ teledeclarationsCount }}</p>
        <p class="fr-mb-2w">{{ teledeclarationTitle }}</p>
        <p class="fr-text--xs fr-mb-0">Soit un pourcentage de {{ percent }}%</p>
      </div>
    </li>
    <li class="fr-col-4">
      <DsfrTile
        :imgSrc="titleImgSrc"
        :horizontal="true"
        title="Voir les cantines"
        description="Retrouvez les cantines correspondantes à votre recherche"
        details="Aller à la page “Trouver une cantine”"
      />
    </li>
  </ul>
</template>

<style lang="scss">
.observatory-results-top {
  &__card {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }
}
</style>
