<script setup>
import { ref } from "vue"
import { storeToRefs } from "pinia"
import { useStoreCanteen } from "@/stores/canteen.js"
import AppSeparator from "@/components/AppSeparator.vue"
import CanteenTableManagers from "@/components/CanteenTableManagers.vue"
import CanteenModalManagerAdd from "@/components/CanteenModalManagerAdd.vue"
import CanteenModalManagerRemove from "@/components/CanteenModalManagerRemove.vue"

const { canteenInformations } = storeToRefs(useStoreCanteen())

const addModalOpened = ref(false)
const removeModalOpened = ref(false)
const managerToRemove = ref(null)
const forceRerender = ref(0)

const openRemoveModal = (member) => {
  managerToRemove.value = member
  removeModalOpened.value = true
}

const closeRemoveModal = () => {
  removeModalOpened.value = false
  managerToRemove.value = null
}
</script>

<template>
  <div class="ma-cantine--flex-between ma-cantine--flex-gap-1 fr-mt-2w fr-mt-md-0 fr-mb-2w fr-mb-md-0">
    <h2 class="fr-h3 fr-mb-0">
      {{ canteenInformations.isGroupe ? "Gestionnaires" : "Mes gestionnaires" }}
    </h2>
    <DsfrButton
      primary
      label="Ajouter un gestionnaire"
      icon="fr-icon-add-circle-fill"
      @click="addModalOpened = true"
    />
  </div>
  <AppSeparator class="layout-sidebar-canteen__separator fr-mt-3w fr-mb-5w" />
  <p>
    Tous les gestionnaires peuvent modifier et supprimer une cantine, ainsi qu'ajouter et enlever des autres
    gestionnaires.
  </p>
  <CanteenTableManagers
    v-if="canteenInformations.id"
    :key="forceRerender"
    :canteen-id="canteenInformations.id"
    @delete="openRemoveModal"
  />
  <CanteenModalManagerAdd
    :opened="addModalOpened"
    :canteen="canteenInformations"
    @close="addModalOpened = false"
    @updated="forceRerender++"
  />
  <CanteenModalManagerRemove
    :opened="removeModalOpened"
    :canteen="canteenInformations"
    :manager="managerToRemove"
    @close="closeRemoveModal"
    @updated="forceRerender++"
  />
</template>
