<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from "vue"
import { storeToRefs } from "pinia"
import { useRoute } from "vue-router"
import { useStoreCanteen } from "@/stores/canteen.js"
import urlService from "@/services/urls.js"
import AppLoader from "@/components/AppLoader.vue"
import AppBadgeSiretSiren from "@/components/AppBadgeSiretSiren.vue"
import AppBadgeCanteen from "@/components/AppBadgeCanteen.vue"
import AppSeparator from "@/components/AppSeparator.vue"
import TunnelTopNav from "@/components/TunnelTopNav.vue"

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
  <div v-else class="layout-tunnel-teledeclaration ma-cantine--sticky__container ma-cantine--stick-to-footer">
    <TunnelTopNav class="ma-cantine--sticky__top" />
    <div class="layout-tunnel-teledeclaration__content fr-grid-row">
      <div class="layout-tunnel-teledeclaration__sidebar fr-background-alt--blue-france fr-col-12 fr-col-md-3 fr-hidden fr-unhidden-md">
        <div class="ma-cantine--z-index-1 fr-pt-4w">
          <div class="fr-mb-4w">
            <h2 class="fr-h4 fr-mb-1w">{{ canteenInformations?.name }}</h2>
            <div>
              <AppBadgeCanteen :canteen="canteenInformations" class="fr-mr-1w" />
              <AppBadgeSiretSiren :canteen="canteenInformations" />
            </div>
          </div>
          <AppSeparator />
        </div>
      </div>
      <div class="fr-col-12 fr-col-md-9 fr-pl-0 fr-pl-md-2w">
        <RouterView />
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.layout-tunnel-teledeclaration {
  &__sidebar {
    position: relative;

    &:before {
      content: "";
      position: absolute;
      top: 0;
      right: 0;
      width: 100vw;
      height: 100%;
      background-color: inherit;
    }
  }
}
</style>
