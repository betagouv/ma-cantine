<script setup>
import { useRouter } from 'vue-router'
import LayoutSidebarBilan from '@/layouts/LayoutSidebarBilan.vue'
import AppFieldDisplay from '@/components/AppFieldDisplay.vue'
import cantines from '@/data/cantines.json'

/* Edit dynamic button */
const router = useRouter()
const goToEdit = (canteenIsGroupe) => {
  const pageName = canteenIsGroupe ? 'GestionnaireCantineGroupeModifier' : 'GestionnaireCantineRestaurantModifier'
  router.push({ name: pageName })
}

/* Value */
const getPrettyValue = (name, field) => {
  if (!name) return null
  return cantines[field].find(model => model.value === name).label
}
</script>

<template>
  <LayoutSidebarBilan v-slot="{ canteenIsGroupe, canteenInformation }">
    <div class="ma-cantine--flex-between ma-cantine--flex-gap-1">
      <h2 class="fr-mb-0">{{ canteenIsGroupe ? 'Informations du groupe' : 'Mes informations' }}</h2>
      <DsfrButton @click="goToEdit(canteenIsGroupe)" :label="canteenIsGroupe ? 'Modifier les informations du groupe' : 'Modifier mes informations'" icon="ri-pencil-line" />
    </div>
    <ol class="ma-cantine--ordered-list ma-cantine--unstyled-list">
      <li class="fr-my-3w">
        <h3>Caractéristiques</h3>
        <AppFieldDisplay v-if="!canteenIsGroupe" :label="cantines.economicModelName" :value="getPrettyValue(canteenInformation.economicModel, 'economicModel')" />
        <AppFieldDisplay :label="cantines.managementTypeName" :value="getPrettyValue(canteenInformation.managementType, 'managementType')" />
        <AppFieldDisplay :label="cantines.productionTypeName" :value="getPrettyValue(canteenInformation.productionType, 'productionType')" />
      </li>
      <li class="fr-my-3w">
        <h3>Identification de l'établissement</h3>
      </li>
      <li v-if="!canteenIsGroupe" class="fr-my-3w">
        <h3>Informations générées</h3>
      </li>
      <li v-if="!canteenIsGroupe" class="fr-my-3w">
        <h3>Secteurs</h3>
      </li>
      <li v-if="canteenInformation.groupe !== null" class="fr-my-3w">
        <h3>Informations de mon groupe</h3>
      </li>
      <li v-if="!canteenIsGroupe" class="fr-my-3w">
        <h3>Description</h3>
      </li>
    </ol>
    <pre>{{ canteenInformation }}</pre>
  </LayoutSidebarBilan>
</template>
