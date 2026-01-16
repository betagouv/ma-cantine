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
const deleleteButtonLabel = computed(() => `Je confirme vouloir supprimer « ${canteenName} »`)
const deleteCanteenLoading = ref(false)
const deleteCanteen = () => {
  deleteCanteenLoading.value = true
  canteenService
    .deleteCanteen(canteenId)
    .then((response) => {
      if(response.status === "error") displayError(response)
      else {
        store.notify({message: `« ${canteenName} » a bien été supprimé, s'il s'agit d'une erreur vous pouvez nous contacter à l'adresse support-egalim@beta.gouv.fr.`, status: "success", title: "Suppression effectuée"})
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
      La suppression d'une cantine entraîne aussi celle des bilans associés. Aucun gestionnaire ne sera en mesure
      d'accéder aux données après la suppression.
    </p>
    <DsfrButton primary :label="deleleteButtonLabel" icon="fr-icon-delete-line" @click="deleteCanteen" :disabled="deleteCanteenLoading" />
  </div>
</template>
