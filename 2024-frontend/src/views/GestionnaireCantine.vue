<script setup>
import { useRouter, useRoute } from "vue-router"
import { storeToRefs } from "pinia"
import { useStoreCanteen } from "@/stores/canteen.js"
import AppLinkRouter from "@/components/AppLinkRouter.vue"
import AppSeparator from "@/components/AppSeparator.vue"
import CanteenDisplayInformations from "@/components/CanteenDisplayInformations.vue"

const route = useRoute()
const router = useRouter()
const canteenUrlComponent = route.params.canteenUrlComponent
const { canteenInformations } = storeToRefs(useStoreCanteen())

const goToEdit = () => {
  const pageName = canteenInformations.value.isGroupe ? "GestionnaireCantineGroupeModifier" : "GestionnaireCantineRestaurantModifier"
  router.push({ name: pageName })
}
</script>

<template>
  <div class="ma-cantine--flex-between ma-cantine--flex-gap-1 fr-mt-2w fr-mt-md-0 fr-mb-2w fr-mb-md-0">
    <h2 class="fr-h3 fr-mb-0">
      {{ canteenInformations.isGroupe ? "Informations du groupe" : "Mes informations" }}
    </h2>
    <DsfrButton
      @click="goToEdit"
      :label="canteenInformations.isGroupe ? 'Modifier les informations du groupe' : 'Modifier mes informations'"
      icon="ri-pencil-line"
    />
  </div>
  <AppSeparator class="layout-sidebar-canteen__separator fr-mt-3w fr-mb-5w" />
  <CanteenDisplayInformations
    :canteen-is-groupe="canteenInformations.isGroupe"
    :canteen-information="canteenInformations"
  />
  <div class="fr-container fr-background-alt--red-marianne fr-p-4w fr-mt-3w">
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
