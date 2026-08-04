<script setup>
import { computed } from "vue"
import { storeToRefs } from "pinia"
import { useStoreCanteen } from "@/stores/canteen.js"
import CanteenSidebarTitle from "@/components/CanteenSidebarTitle.vue"

const canteenStore = useStoreCanteen()
const currentYear = new Date().getFullYear()
const { canteenInformations } = storeToRefs(canteenStore)
const title = computed(() => canteenInformations.value.isGroupe ? `Télédéclaration ${currentYear}` : `Ma télédéclaration ${currentYear}`)

const gotToAppro = () => {
  console.log("gotToAppro")
}
</script>

<template>
  <CanteenSidebarTitle :title="title">
    <DsfrButton
      @click="gotToAppro"
      label="Faire ma télédéclaration"
      icon="ri-send-plane-line"
    />
  </CanteenSidebarTitle>
</template>
