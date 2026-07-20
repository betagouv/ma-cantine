<script setup>
import { ref, computed } from "vue"
import { useRootStore } from "@/stores/root"
import managersService from "@/services/managers.js"

const props = defineProps(["opened", "canteenId", "manager"])
const emit = defineEmits(["close", "updated"])
const store = useRootStore()
const loading = ref(false)

const modalActions = computed(() => {
  return [
    {
      label: loading.value ? 'Suppression en cours...' : 'Supprimer',
      disabled: loading.value,
      onClick() {
        confirmRemove()
      },
    },
    {
      label: 'Annuler',
      secondary: true,
      onClick() {
        closeModal()
      },
    },
  ]
})

const closeModal = () => {
  loading.value = false
  emit("close")
}

const confirmRemove = () => {
  if (!props.manager) return
  loading.value = true
  const email = props.manager.email.trim()
  managersService
    .removeManager(props.canteenId, email)
    .then((response) => {
      if (response.status === "error" || response instanceof Error) {
        store.notifyServerError(response)
      } else {
        store.notify({
          title: "Suppression effectuée",
          message: `${email} n'est plus gestionnaire de cet établissement.`,
          status: "success",
        })
        emit("updated", response)
        emit("close")
      }
      loading.value = false
    })
    .catch((e) => {
      loading.value = false
      store.notifyServerError(e)
    })
}
</script>

<template>
  <DsfrModal
    v-if="manager"
    :opened="opened"
    :title="`Voulez-vous supprimer ${manager.email} de la liste des gestionnaires de cet établissement ?`"
    @close="closeModal"
    :actions="modalActions"
  >
    <p>
      En le supprimant il ne sera plus en mesure de modifier l'établissement et de créer ou modifier ses télédéclarations.
    </p>
  </DsfrModal>
</template>
