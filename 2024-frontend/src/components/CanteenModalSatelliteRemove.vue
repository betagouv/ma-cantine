<script setup>
import { ref } from "vue"
import { useRootStore } from "@/stores/root"
import canteensService from "@/services/canteens"

const props = defineProps(["opened", "groupe", "satellite"])
const emit = defineEmits(["satelliteRemoved", "close"])
const store = useRootStore()
const loading = ref(false)

const unlinkSatellite = () => {
  loading.value = true
  canteensService
    .unlinkSatellite(props.groupe.id, props.satellite.id)
    .then((response) => {
      if (response.status === "error") store.notifyServerError(response)
      else {
        store.notify({
          title: "Retrait de la cantine effectué",
          message: `La cantine « ${props.satellite.name} » ne fait plus partie de votre groupe.`,
        })
        emit("satelliteRemoved")
      }
      emit('close')
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
    :opened="opened"
    class="canteen-button-unlink__modal fr-modal--opened"
    :title="`Souhaitez-vous vraiment retirer «&nbsp;${satellite.name}&nbsp;» de votre groupe ?`"
    @close="emit('close')"
    :actions="[
      {
        label: 'Je confirme le retrait de la cantine',
        onClick() {
          unlinkSatellite()
        },
      },
      {
        label: 'Annuler',
        secondary: true,
        onClick() {
          emit('close')
        },
      },
    ]"
  >
    <template #default>
      <p class="fr-mb-2w">
        En confirmant cette demande « {{ satellite.name }} » ne fera plus partie des cantines de votre
        groupe « {{ groupe.name }} » et donc :
      </p>
      <ul>
        <li>
          <p>
            vous ne pourrez plus télédéclarer ses données
          </p>
        </li>
        <li>
          <p>
            si vous avez déjà effecté une télédéclaration ses données seront conservées
          </p>
        </li>
      </ul>
    </template>
  </DsfrModal>
</template>
