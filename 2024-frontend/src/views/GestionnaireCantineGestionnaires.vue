<script setup>
import { ref } from "vue"
import LayoutSidebarCanteen from "@/layouts/LayoutSidebarCanteen.vue"
import CanteenTableManagers from "@/components/CanteenTableManagers.vue"
import CanteenModalManagerAdd from "@/components/CanteenModalManagerAdd.vue"
import CanteenModalManagerRemove from "@/components/CanteenModalManagerRemove.vue"

const addModalOpened = ref(false)
const removeModalOpened = ref(false)
const managerToRemove = ref(null)
const managersTable = ref(null)

const updateManagersList = (managementTeam) => {
  managersTable.value?.update(managementTeam)
}

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
  <LayoutSidebarCanteen>
    <template #titleName="{ canteenIsGroupe }">
      {{ canteenIsGroupe ? "Gestionnaires" : "Mes gestionnaires" }}
    </template>
    <template #titleButton>
      <DsfrButton
        primary
        label="Ajouter un gestionnaire"
        icon="fr-icon-add-circle-fill"
        @click="addModalOpened = true"
      />
    </template>
    <template #content="{ canteenInformation }">
      <p>
        Tous les gestionnaires peuvent modifier et supprimer une cantine, ainsi qu'ajouter et enlever des autres
        gestionnaires.
      </p>
      <CanteenTableManagers
        v-if="canteenInformation"
        ref="managersTable"
        :canteen-information="canteenInformation"
        @delete="openRemoveModal"
      />
      <CanteenModalManagerAdd
        v-if="canteenInformation"
        :opened="addModalOpened"
        :canteen="canteenInformation"
        @close="addModalOpened = false"
        @updated="updateManagersList"
      />
      <CanteenModalManagerRemove
        v-if="canteenInformation"
        :opened="removeModalOpened"
        :canteen="canteenInformation"
        :manager="managerToRemove"
        @close="closeRemoveModal"
        @updated="updateManagersList"
      />
    </template>
  </LayoutSidebarCanteen>
</template>
