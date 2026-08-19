<script setup>
import { computed } from "vue"
import AppBlueCard from "@/components/AppBlueCard.vue"

const props = defineProps(["canteenInformations"])

/* Content */
const hasSatellite = computed(() => props.canteenInformations.isGroupe)
const satellitesCount = computed(() => props.canteenInformations.satellitesCount)
const emptySatellitesCount = computed(() => hasSatellite.value && satellitesCount.value == 0)
</script>

<template>
  <AppBlueCard
    v-if="hasSatellite"
    title="Souhaitez-vous mettre à jour la liste de cantines de votre groupe ?"
    :alert="{
      description: emptySatellitesCount ? 'Obligatoire : vous devez lier au moins une cantine à vos approvisionnements groupés' : 'Optionnel : cette étape n’est pas obligatoire pour déclarer vos approvisionnements.',
      type: emptySatellitesCount ? 'error' : 'info',
    }"
    :button="{
      label: 'Mettre à jour mes cantines',
      to: 'GestionnaireCantineGroupe',
    }"
  >
    <p v-if="emptySatellitesCount">
      Vous n’avez aucune cantine lié à vos approvisionnements groupés.
    </p>
    <p v-else>
      Vous avez <strong>{{ satellitesCount }} {{ satellitesCount > 1 ? 'cantines liées' : 'cantine liée' }}</strong> à vos approvisionnements groupés
    </p>
  </AppBlueCard>
</template>
