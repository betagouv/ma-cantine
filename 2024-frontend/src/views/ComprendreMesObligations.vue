<script setup>
import { ref } from "vue"
import { useRoute } from "vue-router"
import { tiles } from "@/constants/crisp-tiles.js"
import AppNeedHelp from "@/components/AppNeedHelp.vue"

const route = useRoute()

/* MODAL */
const article = ref(null)
const openModal = (tile) => {
  article.value = tile
}
const closeModal = () => {
  article.value = null
}
</script>

<template>
  <section class="fr-col-12 fr-col-md-7 fr-mb-5w">
    <h1>{{ route.meta.title }}</h1>
    <p class="fr-mb-0">
      La restauration collective se doit de respecter les obligations de la loi EGalim ainsi que la loi Climat et
      Résilience. En fonction des typologies des cantines il y a des spécificités à respecter. La documentation
      ci-dessous vous aide dans leur mise en place.
    </p>
  </section>
  <section>
    <ul class="ma-cantine--unstyled-list fr-grid-row fr-grid-row--center fr-grid-row--gutters fr-my-5w fr-mb-8w">
      <li v-for="(tile, index) in tiles" :key="index" class="fr-col-12 fr-col-md-4">
        <DsfrTile
          :title="tile.title"
          titleTag="h2"
          :imgSrc="tile.imgSrc"
          :details="tile.details"
          @click="openModal(tile)"
          class="ma-cantine--tile-no-overflow"
        />
      </li>
    </ul>
    <DsfrModal :opened="article" class="fr-modal--opened" @close="closeModal" size="xl">
      <template #default>
        <iframe
          :title="article.title"
          :src="`${article.to}/reader/compact/`"
          class="comprendre-mes-obligations__iframe"
          frameborder="0"
        ></iframe>
      </template>
    </DsfrModal>
  </section>
  <AppNeedHelp badge="En savoir plus" align="center" title="Pour les acteurs de la restauration collective">
    <p class="fr-mb-0">
      Retrouvez des ressources, contenus videos, documents, témoignages, articles, recettes,
      <a href="https://ma-cantine-1.gitbook.io/ma-cantine-egalim/" target="_blank">sur notre documentation</a>
      . Pour toute question, consultez
      <a href="https://ma-cantine.crisp.help/fr/" target="_blank">notre centre d'aide</a>
    </p>
  </AppNeedHelp>
</template>

<style lang="scss">
.comprendre-mes-obligations {
  &__iframe {
    width: 100%;
    height: 60vh;
  }
}
</style>
