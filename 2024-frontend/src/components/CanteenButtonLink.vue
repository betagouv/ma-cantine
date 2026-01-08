<script setup>
  import { ref } from "vue"
  import { useRootStore } from "@/stores/root"
  import canteensService from "@/services/canteens"

  const props = defineProps(["satId", "groupId"])
  const emit = defineEmits(["satelliteAdded"])
  const loading = ref(false)
  const store = useRootStore()

  /* Add Satellite */
  const label = ref("Ajouter ce restaurant satellite à mon groupe")
  const addSatellite = () => {
    loading.value = true
    label.value = "Ajout en cours..."
    canteensService
      .linkSatellite(props.groupId, props.satId)
      .then(() => {
        emit("satelliteAdded")
      })
      .catch((e) => {
        loading.value = false
        store.notifyServerError(e)
      })
  }
</script>

<template>
  <DsfrButton secondary :label="label" @click="addSatellite()" :disabled="loading" />
</template>
