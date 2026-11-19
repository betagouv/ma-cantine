<script setup>
import { storeToRefs } from "pinia"
import { useStoreCanteen } from "@/stores/canteen"

const storeCanteen = useStoreCanteen()
const { canteenInformations } = storeToRefs(storeCanteen)
</script>

<template>
  <p v-if="canteenInformations?.isGroupe">
    <span class="fr-text--bold">À noter :</span> Les cantines rattachées à votre groupe pourront télédéclarer leurs propres valeurs.
  </p>
</template>
