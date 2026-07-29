<script setup>
import { useRouter, useRoute } from "vue-router"
import { storeToRefs } from "pinia"
import { useStoreCanteen } from "@/stores/canteen.js"
import AppLinkRouter from "@/components/AppLinkRouter.vue"
import CanteenSidebarTitle from "@/components/CanteenSidebarTitle.vue"
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
  <CanteenSidebarTitle :title="canteenInformations.isGroupe ? 'Informations du groupe' : 'Mes informations'">
    <DsfrButton
      @click="goToEdit"
      :label="canteenInformations.isGroupe ? 'Modifier les informations du groupe' : 'Modifier mes informations'"
      icon="ri-pencil-line"
    />
  </CanteenSidebarTitle>
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
