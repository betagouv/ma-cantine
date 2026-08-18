<script setup>
import AppBadgeSiretSiren from "@/components/AppBadgeSiretSiren.vue"
import AppBadgeCanteen from "@/components/AppBadgeCanteen.vue"
import AppSeparator from "@/components/AppSeparator.vue"

defineProps(["canteen"])
</script>

<template>
  <div class="tunnel-teledeclaration-sidebar fr-background-alt--blue-france fr-col-12 fr-col-md-3 fr-hidden fr-unhidden-md">
    <div class="ma-cantine--z-index-1 fr-pt-4w">
      <div class="fr-mb-4w">
        <h2 class="fr-h4 fr-mb-1w">{{ canteen?.name }}</h2>
        <div>
          <AppBadgeCanteen :canteen="canteen" class="fr-mr-1w" />
          <AppBadgeSiretSiren :canteen="canteen" />
        </div>
      </div>
      <AppSeparator />
    </div>
  </div>
</template>

<style lang="scss" scoped>
.tunnel-teledeclaration-sidebar {
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
</style>
