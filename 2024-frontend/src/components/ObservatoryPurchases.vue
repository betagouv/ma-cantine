<script setup>
import { computed } from "vue"
import AppLinkRouter from "@/components/AppLinkRouter.vue"
import ObservatoryBadgeTitle from "@/components/ObservatoryBadgeTitle.vue"
import keyMeasures from "@/data/key-measures.json"
import GraphGauge from "@/components/GraphGauge.vue"

const props = defineProps(["bio", "sustainable"])

const approBadge = "/static/images/badges/appro.svg"
const keyMeasureId = keyMeasures[0].id

/* Verify stats */
const hasBio = computed(() => props.bio !== null && props.bio !== undefined)
const hasSustainable = computed(() => props.sustainable !== null && props.sustainable !== undefined)
</script>

<template>
  <div class="fr-card fr-p-4w">
    <ObservatoryBadgeTitle class="fr-mb-3w" :image="approBadge" color="#f44336" title="Produits durables et de qualité">
      Distribuer 50% de produits de qualité dont 20% de produits bio et distribuer au moins 60 % de produits durables et
      de qualité dans la famille de denrées “viandes et poissons“.
      <AppLinkRouter :to="{ name: 'KeyMeasurePage', params: { id: keyMeasureId } }" title="En savoir plus sur la loi" />
    </ObservatoryBadgeTitle>
    <div>
      <h3 class="fr-h6 fr-mb-2w">1. Produits durable et de qualité dont les produits bio</h3>
      <GraphGauge
        v-if="hasBio && hasSustainable"
        :objectives="[50, 20]"
        :stats="[sustainable, bio]"
        :legends="['durables et de qualité dont bio', 'bio et en conversion bio']"
      />
      <p v-else>
        Une erreur est survenue lors de l'affichage du graphique, veuillez recharger la page et si l'erreur persiste
        contactez-nous.
      </p>
    </div>
  </div>
</template>
