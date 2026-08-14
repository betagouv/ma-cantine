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
  <p v-if="canteenInformations.isGroupe">
    Tous les gestionnaires du groupe peuvent : modifier les informations du groupe, archiver le groupe, rattacher ou retirer des cantines du groupe, ajouter des achats au fil de l’eau (via l’outil de suivi des achats), compléter et télédéclarer le bilan groupé de l’année n-1 (uniquement lors de la campagne de télédéclaration de l’année n), ajouter ou retirer des gestionnaires, consulter et télécharger les justificatifs de télédéclaration.
  </p>
  <p v-else>
    Tous les gestionnaires de la cantine peuvent : modifier les informations de la cantine, archiver la cantine, ajouter des achats au fil de l’eau (via l’outil de suivi des achats), compléter et télédéclarer le bilan de l’année précédente (uniquement lors de la campagne de télédéclaration), ajouter ou retirer des gestionnaires, consulter et télécharger les justificatifs de télédéclaration.
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
