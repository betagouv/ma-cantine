<script setup>
import { ref } from "vue"
import { useRoute } from "vue-router"
import { tiles } from "@/constants/understanding-law.js"

const route = useRoute()
const iframeUrl = ref(null)
</script>

<template>
  <section class="fr-col-12 fr-col-md-7 fr-mb-5w">
    <h1>{{ route.meta.title }}</h1>
    <p>
      Donec ullamcorper nulla non metus auctor fringilla. Vestibulum id ligula porta felis euismod semper. Vestibulum id
      ligula porta felis euismod semper. Vivamus sagittis lacus vel augue laoreet rutrum faucibus dolor auctor. Nullam
      id dolor id nibh ultricies vehicula ut id elit. Maecenas sed diam eget risus varius blandit sit amet non magna.
    </p>
  </section>
  <ul class="ma-cantine--unstyled-list fr-grid-row fr-grid-row--center fr-grid-row--gutters">
    <li v-for="(tile, index) in tiles" :key="index" class="fr-col-4">
      <DsfrTile
        class="understanding-law__tile"
        :title="tile.title"
        :imgSrc="tile.imgSrc"
        :details="tile.details"
        :to="tile.to"
        @click.prevent="iframeUrl = tile.to"
      />
    </li>
  </ul>
  <DsfrModal :opened="iframeUrl" size="xl" class="understanding-law__modal" @close="iframeUrl = null">
    <iframe :src="iframeUrl" class="understanding-law__iframe"></iframe>
  </DsfrModal>
</template>

<style lang="scss">
.understanding-law {
  &__tile {
    .fr-tile__pictogram {
      overflow: visible;
    }
  }

  &__iframe {
    width: 100%;
    min-height: 80vh;
  }

  &__modal {
    .fr-modal__body {
      overflow: hidden;
    }
  }
}
</style>
