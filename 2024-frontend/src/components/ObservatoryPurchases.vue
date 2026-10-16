<script setup>
import { useStoreFilters } from "@/stores/filters"
import stringsService from "@/services/strings"
import AppLinkRouter from "@/components/AppLinkRouter.vue"
import ObservatoryBadgeTitle from "@/components/ObservatoryBadgeTitle.vue"
import GraphEgalim from "@/components/GraphEgalim.vue"
import ObservatoryGraphMeatFishEgalim from "@/components/ObservatoryGraphMeatFishEgalim.vue"
import ObservatoryGraphMeatFrance from "@/components/ObservatoryGraphMeatFrance.vue"
import ObservatoryGraphEgalim from "@/components/ObservatoryGraphEgalim.vue"

defineProps(["stats"])
const storeFilters = useStoreFilters()
const approBadge = "/static/images/badges/badge-appro.svg"
</script>

<template>
  <div class="observatory-purchases">
    <ObservatoryBadgeTitle class="fr-mb-4w" :image="approBadge" color="#316341" title="Produits EGalim">
      Distribuer {{ stringsService.prettyPercent(50) }} de produits EGalim dont
      {{ stringsService.prettyPercent(20) }} de produits bio et distribuer au moins
      {{ stringsService.prettyPercent(60) }} de produits EGalim dans la famille de denrées "viandes et poissons".
      <AppLinkRouter
        :to="{ name: 'ComprendreMesObligations' }"
        title="En savoir plus sur la loi"
      />
    </ObservatoryBadgeTitle>
    <DsfrNotice v-if="stats.notes.alert" :title="stats.notes.alert.title" :desc="stats.notes.alert.message" type="warning" class="fr-mb-4w" />
    <ol class="ma-cantine--ordered-list ma-cantine--unstyled-list">
      <li class="fr-mb-8w">
        <ObservatoryGraphEgalim :approPercent="stats.approPercent" />
      </li>
      <li class="fr-mb-8w">
        <GraphEgalim
          :bioPercent="stats.bioPercent"
          :egalimPercent="stats.egalimPercent"
          :bioObjective="stats.notes.bioPercentObjective"
          :egalimObjective="stats.notes.egalimPercentObjective"
          title="Produits EGalim dont les produits bio"
          :descriptionCustom="`pour la recherche ${storeFilters.getSelectionLabels()}`"
        />
      </li>
      <li class="fr-mb-8w">
        <ObservatoryGraphMeatFishEgalim
          :viandesVolaillesProduitsDeLaMerEgalimPercent="stats.viandesVolaillesProduitsDeLaMerEgalimPercent"
        />
      </li>
      <li class="fr-hidden">
        <ObservatoryGraphMeatFrance :viandesVolaillesFrancePercent="stats.viandesVolaillesFrancePercent"/>
      </li>
    </ol>
  </div>
</template>
