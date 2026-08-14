<script setup>
import { useRouter, useRoute } from "vue-router"
import { computed } from "vue"
import { storeToRefs } from "pinia"
import { useStoreCanteen } from "@/stores/canteen.js"
import AppLinkRouter from "@/components/AppLinkRouter.vue"
import CanteenSidebarTitle from "@/components/CanteenSidebarTitle.vue"
import CanteenDisplayInformations from "@/components/CanteenDisplayInformations.vue"

const route = useRoute()
const router = useRouter()
const canteenUrlComponent = route.params.canteenUrlComponent
const { canteenInformations } = storeToRefs(useStoreCanteen())
const title = computed(() => canteenInformations.value?.isGroupe ? 'Informations du groupe' : 'Informations de la cantine')
const editButtonLabel = computed(() => canteenInformations.value?.isGroupe ? 'Modifier les informations du groupe' : 'Modifier les informations de la cantine')

const goToEdit = () => {
  const pageName = canteenInformations.value.isGroupe ? "GestionnaireCantineGroupeModifier" : "GestionnaireCantineRestaurantModifier"
  router.push({ name: pageName })
}
</script>

<template>
  <CanteenSidebarTitle :title="title">
    <DsfrButton
      @click="goToEdit"
      :label="editButtonLabel"
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
      Archiver {{ canteenInformations.isGroupe ? "ce groupe" : "cette cantine" }}
    </h3>
    <div>
      <p class="fr-mb-0">
        <span v-if="canteenInformations.isGroupe">La gestion groupée des cantines du groupe n’est plus pertinente ?</span>
        <span v-else>Vous ne souhaitez plus faire apparaître cette cantine sur la plateforme <em>ma cantine</em> ?</span>
        <br />
        Vous pouvez l’archiver <AppLinkRouter :to="{ name: 'GestionnaireCantineArchiver', params: { canteenUrlComponent: canteenUrlComponent } }" title="en cliquant ici" />
      </p>
      <p v-if="canteenInformations.isGroupe" class="fr-mb-0 fr-mt-2w">
        Attention : si vous archivez un groupe, les cantines seront uniquement dissociées du groupe, mais ne seront pas archivées.
      </p>
    </div>
  </div>
</template>
