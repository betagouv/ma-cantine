<script setup>
import { ref } from "vue"
import { useRootStore } from "@/stores/root"
import canteensService from "@/services/canteens"

const props = defineProps(["id", "name"])
const loading = ref(false)
const store = useRootStore()

/* Ask to join */
const joinLabel = ref("Rejoindre la cantine")
const joinCanteen = () => {
  loading.value = true
  const userInfos = {
    email: store.loggedUser.email,
    name: `${store.loggedUser.firstName} ${store.loggedUser.lastName}`,
  }
  canteensService
    .teamJoinRequest(props.id, userInfos)
    .then(() => {
      store.notify({
        title: "Demande envoyée",
        message: `Nous avons contacté l'équipe de la cantine ${props.name}. Ces derniers reviendront vers vous pour accepter ou non votre demande.`,
      })
      joinLabel.value = "Demande envoyée"
    })
    .catch((e) => {
      loading.value = false
      store.notifyServerError(e)
    })
}
</script>

<template>
  <DsfrButton tertiary :label="joinLabel" @click="joinCanteen()" :disabled="loading" />
</template>
