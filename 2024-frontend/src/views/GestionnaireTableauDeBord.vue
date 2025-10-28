<script setup>
import { computed } from "vue"
import { computedAsync } from "@vueuse/core"
import { useRootStore } from "@/stores/root"
import canteenService from "@/services/canteens.js"
import GestionnaireGuides from "@/components/GestionnaireGuides.vue"
import GestionnaireCanteensCreate from "@/components/GestionnaireCanteensCreate.vue"

const store = useRootStore()

/* Title */
const canteenSentence = computed(() => {
  const count = store.canteenPreviews.length
  if (count === 0) return "vous n'avez pas encore de cantine"
  else if (count === 1) return "1 cantine"
  return `${count} cantines`
})

/* Table */
const header = ["Nom de la cantine", "Siret / Siren", "Commune et code postal", "Type", "Statut", "Actions"]
const rows = computedAsync(async () => {
  const canteens = await canteenService.fetchCanteensActions()
  const rows = []
  canteens.forEach((canteen) => {
    rows.push([
      canteen.name,
      canteen.siret || canteen.sirenUniteLegale,
      `${canteen.city} - ${canteen.postalCode}`,
      canteen.productionType,
      canteen.action,
      "",
    ])
  })
  return rows
}, [])
</script>

<template>
  <section>
    <h1>Bienvenue dans votre espace, {{ store.loggedUser.firstName }}</h1>
    <p class="fr-text--lead">{{ canteenSentence }}</p>
  </section>
  <section class="ma-cantine--stick-to-footer">
    <GestionnaireCanteensCreate v-if="store.canteenPreviews.length === 0" />
    <DsfrDataTable
      v-else
      class="gestionnaire-canteens-table"
      title="Vos cantines"
      no-caption
      :headers-row="header"
      :rows="rows"
    />
    <GestionnaireGuides />
  </section>
</template>
