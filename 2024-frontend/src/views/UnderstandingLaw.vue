<script setup>
import { useRoute } from "vue-router"
import { tiles } from "@/constants/understanding-law.js"
import AppNeedHelp from "@/components/AppNeedHelp.vue"

const route = useRoute()
</script>

<template>
  <section class="fr-col-12 fr-col-md-7 fr-mb-5w">
    <h1>{{ route.meta.title }}</h1>
    <p class="fr-mb-0">
      Donec ullamcorper nulla non metus auctor fringilla. Vestibulum id ligula porta felis euismod semper. Vestibulum id
      ligula porta felis euismod semper. Vivamus sagittis lacus vel augue laoreet rutrum faucibus dolor auctor. Nullam
      id dolor id nibh ultricies vehicula ut id elit. Maecenas sed diam eget risus varius blandit sit amet non magna.
    </p>
  </section>
  <section>
    <ul class="ma-cantine--unstyled-list fr-grid-row fr-grid-row--center fr-grid-row--gutters fr-my-5w fr-mb-8w">
      <li v-for="(tile, index) in tiles" :key="index" class="fr-col-12 fr-col-md-4">
        <DsfrTile
          class="understanding-law__tile"
          :title="tile.title"
          titleTag="h2"
          :imgSrc="tile.imgSrc"
          :details="tile.details"
          :to="tile.to"
        />
      </li>
    </ul>
  </section>
  <AppNeedHelp badge="Besoin d'aide" align="center" title="Vous ne trouvez pas ce que vous chercher ?">
    <p>
      Découvrez notre documentation complète qui centralise les ressources, contenus videos, documents, témoignages,
      articles, recettes, etc. Pour les acteurs et actrices de la restauration collective.
    </p>
    <a href="https://ma-cantine.crisp.help/fr/" target="_blank">Accéder à notre centre de ressources</a>
  </AppNeedHelp>
</template>

<style lang="scss">
.understanding-law {
  &__tile {
    .fr-tile__pictogram {
      overflow: visible;
    }
  }
}
</style>
