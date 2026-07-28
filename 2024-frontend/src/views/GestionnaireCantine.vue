<script setup>
import { useRouter, useRoute } from 'vue-router'
import LayoutSidebarCanteen from '@/layouts/LayoutSidebarCanteen.vue'
import AppLinkRouter from '@/components/AppLinkRouter.vue'
import CanteenDisplayInformations from '@/components/CanteenDisplayInformations.vue'

const route = useRoute()
const router = useRouter()
const canteenUrlComponent = route.params.canteenUrlComponent

/* Edit redirect */
const goToEdit = (canteenIsGroupe) => {
  const pageName = canteenIsGroupe ? 'GestionnaireCantineGroupeModifier' : 'GestionnaireCantineRestaurantModifier'
  router.push({ name: pageName })
}
</script>

<template>
  <LayoutSidebarCanteen>
    <template #titleName="{ canteenIsGroupe }">
      {{ canteenIsGroupe ? 'Informations du groupe' : 'Mes informations' }}
    </template>
    <template #titleButton="{ canteenIsGroupe }">
      <DsfrButton @click="goToEdit(canteenIsGroupe)" :label="canteenIsGroupe ? 'Modifier les informations du groupe' : 'Modifier mes informations'" icon="ri-pencil-line" />
    </template>
    <template #content="{ canteenIsGroupe, canteenInformation }">
      <CanteenDisplayInformations :canteen-is-groupe="canteenIsGroupe" :canteen-information="canteenInformation" />
      <div v-if="canteenUrlComponent" class="fr-container fr-background-alt--red-marianne fr-p-4w fr-mt-3w">
        <h3 class="fr-h6 fr-text-default--error fr-mb-2w">
          <span class="mdi mdi-archive"></span>
          Archiver cet établissement
        </h3>
        <p class="fr-mb-0">
          Vous ne souhaitez plus faire apparaître cet établissement sur la plateforme <em>ma cantine</em> ? <br />
          Vous pouvez l’archiver <AppLinkRouter :to="{ name: 'GestionnaireCantineArchiver', params: { canteenUrlComponent: canteenUrlComponent } }" title="en cliquant ici" />
        </p>
      </div>
    </template>
  </LayoutSidebarCanteen>
</template>
