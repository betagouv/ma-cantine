<script setup>
import { computed } from "vue"
import { storeToRefs } from "pinia"
import { useStoreTeledeclaration } from "@/stores/teledeclaration.js"

const teledeclarationStore = useStoreTeledeclaration()
const { diagnostic } = storeToRefs(teledeclarationStore)
const isTeledeclared = computed(() => diagnostic.value.isTeledeclared)
</script>

<template>
  <div class="diagnostic-summary-tile">
    <div class="fr-tile" :class="{ 'fr-tile--blue': isTeledeclared }">
      <div class="fr-tile__body">
        <div class="fr-tile__title">
          <p>ici</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss">
.diagnostic-summary-tile {
  .fr-tile--blue .fr-tile__title::before {
    background-image: linear-gradient(0deg,var(--border-active-blue-france),var(--border-active-blue-france)) !important;
  }
}
</style>
