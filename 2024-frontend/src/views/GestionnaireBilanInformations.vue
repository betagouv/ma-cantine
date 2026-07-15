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
  <LayoutSidebarBilan v-slot="{ canteenIsGroupe }">
    <div class="ma-cantine--flex-between ma-cantine--flex-gap-1">
      <h2 class="fr-mb-0">{{ canteenIsGroupe ? 'Informations du groupe' : 'Mes informations' }}</h2>
      <DsfrButton @click="goToEdit(canteenIsGroupe)" :label="canteenIsGroupe ? 'Modifier les informations du groupe' : 'Modifier mes informations'" icon="ri-pencil-line" />
    </div>
    <pre>{{ canteenInformation }}</pre>
  </LayoutSidebarBilan>
</template>
