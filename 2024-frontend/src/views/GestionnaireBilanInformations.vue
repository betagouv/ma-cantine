<script setup>
import { useRouter } from 'vue-router'
import LayoutSidebarBilan from '@/layouts/LayoutSidebarBilan.vue'

/* Edit dynamic button */
const router = useRouter()
const goToEdit = (canteenIsGroupe) => {
  const pageName = canteenIsGroupe ? 'GestionnaireCantineGroupeModifier' : 'GestionnaireCantineRestaurantModifier'
  router.push({ name: pageName })
}
</script>

<template>
  <LayoutSidebarBilan v-slot="{ canteenIsGroupe, canteenInformation }">
    <div class="ma-cantine--flex-between ma-cantine--flex-gap-1">
      <h2 class="fr-mb-0">{{ canteenIsGroupe ? 'Informations du groupe' : 'Mes informations' }}</h2>
      <DsfrButton @click="goToEdit(canteenIsGroupe)" :label="canteenIsGroupe ? 'Modifier les informations du groupe' : 'Modifier mes informations'" icon="ri-pencil-line" />
    </div>
    <ol class="ma-cantine--ordered-list ma-cantine--unstyled-list">
      <li>
        <h3>Caractéristiques</h3>
      </li>
      <li>
        <h3>Identification de l'établissement</h3>
      </li>
      <li v-if="!canteenIsGroupe">
        <h3>Informations générées</h3>
      </li>
      <li v-if="!canteenIsGroupe">
        <h3>Secteurs</h3>
      </li>
      <li v-if="canteenInformation.groupe !== null">
        <h3>Informations de mon groupe</h3>
      </li>
      <li v-if="!canteenIsGroupe">
        <h3>Description</h3>
      </li>
    </ol>
    <pre>{{ canteenInformation }}</pre>
  </LayoutSidebarBilan>
</template>
