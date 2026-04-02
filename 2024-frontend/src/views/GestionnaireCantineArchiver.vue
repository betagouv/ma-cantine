<script setup>
import { ref, computed } from "vue"
import { useRoute, useRouter } from "vue-router"
import { useRootStore } from "@/stores/root"
import urlService from "@/services/urls.js"
import canteenService from "@/services/canteens.js"

/* Store and Router*/
const store = useRootStore()
const route = useRoute()
const router = useRouter()

/* Canteen infos */
const canteenName = urlService.getCanteenName(route.params.canteenUrlComponent)
const canteenId = urlService.getCanteenId(route.params.canteenUrlComponent)

/* Delete */
const deleleteButtonLabel = computed(() => `Je confirme vouloir archiver « ${canteenName} »`)
const deleteCanteenLoading = ref(false)
const deleteCanteen = () => {
  deleteCanteenLoading.value = true
  canteenService
    .deleteCanteen(canteenId)
    .then((response) => {
      if(response.status === "error") displayError(response)
      else {
        store.notify({message: `L'établissement « ${canteenName} » a bien été archivé, s'il s'agit d'une erreur vous pouvez nous contacter à l'adresse support-egalim@beta.gouv.fr.`, status: "success", title: "Établissement archivé"})
        router.push({name: "GestionnaireTableauDeBord"})
      }
    })
    .catch(displayError)
}

const displayError = (error) => {
  store.notifyServerError(error)
  deleteCanteenLoading.value = false
}
</script>
<template>
  <div class="fr-col-12 fr-col-md-8 fr-mb-3w">
    <h1>{{ route.meta.title }} «&nbsp;{{ canteenName }}&nbsp;»</h1>
    <p>
      En archivant l'établissement :
    </p>
    <ul class="fr-mb-4w">
      <li>il sera automatiquement masqué de votre tableau de bord</li>
      <li>il sera retiré du registre national des cantines</li>
      <li>il sera retiré de l’annuaire des cantines</li>
      <li>tous les bilans déjà déclarés seront conservés</li>
    </ul>
    <DsfrButton primary :label="deleleteButtonLabel" @click="deleteCanteen" :disabled="deleteCanteenLoading" />
  </div>
</template>
