<script setup>
import { computed } from 'vue'
const displayBanner = computed(() => window.ENVIRONMENT !== "prod")
</script>
<template>
  <DsfrNotice v-if="displayBanner" class="banner-env" type="warning" title="ATTENTION : Plateforme de test et de démonstration.">
    <template #desc>
      Pour toute action officielle, rendez-vous sur la
      <a
        href="https://ma-cantine.agriculture.gouv.fr/"
        target="_blank"
        title="plateforme ma cantine - nouvelle fenêtre"
      >
        plateforme <em>ma cantine</em>
      </a>.
      Toutes les actions sont sans conséquence. Le comportement est figé sur la période de télédéclaration (possibilité de créer un bilan de l'année n-1 et de le télédéclarer / corriger jusqu'à la fin de l'année n)
    </template>
  </DsfrNotice>
</template>

<style scoped>
.banner-env {
  position: sticky;
  top: 0;
  z-index: 1000;
}
</style>
