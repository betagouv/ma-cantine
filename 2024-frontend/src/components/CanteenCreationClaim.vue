<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import { useRootStore } from "@/stores/root"
import canteensService from "@/services/canteens"

defineProps(["id"])
const loading = ref(false)
const store = useRootStore()
const router = useRouter()

/* Claim a canteen */
const claimCanteen = (id) => {
  console.log("id", id)
  loading.value = true
  canteensService
    .claimCanteen(id)
    .then((response) => {
      loading.value = false
      if (response.id) {
        router.push({
          name: "DashboardManager",
          params: { canteenUrlComponent: response.id },
        })
      }
    })
    .catch((e) => {
      loading.value = false
      store.notifyServerError(e)
    })
}
</script>

<template>
  <DsfrButton tertiary label="Revendiquer la cantine" @click="claimCanteen(id)" :disabled="loading" />
</template>
