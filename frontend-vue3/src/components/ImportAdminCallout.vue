<script setup>
import { computed } from "vue"
import { useRootStore } from "@/stores/root"
const store = useRootStore()
const isAdmin = computed(() => store.loggedUser.isStaff )
</script>
<template>
  <DsfrCallout
    v-if="isAdmin"
    titleTag="h3"
    title="En tant que membre de l'équipe ma cantine"
    content="Vous pouvez modifier des cantines, vous n'avez pas besoin d'être gestionnaire de ces cantines et vous ne serez pas ajouté automatiquement à l'équipe de gestion."
  />
</template>
