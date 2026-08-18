<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from "vue"
import { storeToRefs } from "pinia"
import { useRoute } from "vue-router"
import { useStoreCanteen } from "@/stores/canteen.js"
import urlService from "@/services/urls.js"
import AppLoader from "@/components/AppLoader.vue"
import TunnelTeledeclarationTopNav from "@/components/TunnelTeledeclarationTopNav.vue"
import TunnelTeledeclarationSidebar from "@/components/TunnelTeledeclarationSidebar.vue"

const route = useRoute()

/* Store */
const canteenUrlId = computed(() => urlService.getCanteenId(route.params.canteenUrlComponent))
const isLoading = ref(false)
const canteenStore = useStoreCanteen()
const { canteenInformations } = storeToRefs(canteenStore)
const loadStore = async () => {
  if (!canteenInformations.value || canteenInformations.value.id != canteenUrlId.value) {
    isLoading.value = true
    await canteenStore.initStore(canteenUrlId.value)
    isLoading.value = false
  }
}
onMounted(() => loadStore())
onUnmounted(() => canteenStore.deleteStore())
watch(canteenUrlId, () => loadStore())
</script>
<template>
  <AppLoader v-if="isLoading || !canteenInformations" />
  <div v-else class="ma-cantine--sticky__container ma-cantine--stick-to-footer">
    <TunnelTeledeclarationTopNav class="ma-cantine--sticky__top" />
    <div class="fr-grid-row">
      <TunnelTeledeclarationSidebar :canteen="canteenInformations" />
      <div class="fr-col-12 fr-col-md-9 fr-pl-0 fr-pl-md-2w">
        <RouterView />
      </div>
    </div>
  </div>
</template>
