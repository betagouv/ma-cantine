<script setup>
import { storeToRefs } from "pinia"
import { useStoreTeledeclaration } from "@/stores/teledeclaration.js"

const teledeclarationStore = useStoreTeledeclaration()
const { diagnostic } = storeToRefs(teledeclarationStore)
</script>
<template>
  <div>
    <pre>{{ diagnostic }}</pre>
  </div>
</template>
