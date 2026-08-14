<script setup>
import { ref, computed } from "vue"
import { storeToRefs } from "pinia"
import { useStoreCanteen } from "@/stores/canteen.js"
import CanteenSidebarTitle from "@/components/CanteenSidebarTitle.vue"
import CanteenTableManagers from "@/components/CanteenTableManagers.vue"
import CanteenModalManagerAdd from "@/components/CanteenModalManagerAdd.vue"
import CanteenModalManagerRemove from "@/components/CanteenModalManagerRemove.vue"

const { canteenInformations } = storeToRefs(useStoreCanteen())

const addModalOpened = ref(false)
const removeModalOpened = ref(false)
const managerToRemove = ref(null)
const forceRerender = ref(0)
const title = computed(() => canteenInformations.value?.isGroupe ? 'Gestionnaires du groupe' : 'Gestionnaires de la cantine')

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
  <CanteenSidebarTitle :title="title">
    <DsfrButton
      primary
      label="Ajouter un gestionnaire"
      icon="fr-icon-add-circle-fill"
      @click="addModalOpened = true"
    />
  </CanteenSidebarTitle>
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
