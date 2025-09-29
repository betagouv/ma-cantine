<script setup>
import { ref } from "vue"
import { useRootStore } from "@/stores/root"
import canteensService from "@/services/canteens"

const store = useRootStore()
const props = defineProps(["canteen", "satellite"])
const emit = defineEmits(["satelliteRemoved"])
const loading = ref(false)
const opened = ref(false)

const toggleModal = () => {
  opened.value = !opened.value
}

const unlinkSatellite = () => {
  loading.value = true
  canteensService
    .unlinkSatellite(props.canteen.id, props.satellite.id)
    .then(() => {
      store.notify({
        title: "Retrait de la cantine effectué",
        message: `La cantine ${props.satellite.name} ne fait plus partie de vos satellites.`,
      })
      loading.value = false
      toggleModal()
      emit("satelliteRemoved")
    })
    .catch((e) => {
      loading.value = false
      store.notifyServerError(e)
    })
}
</script>

<template>
  <DsfrButton
    secondary
    label="Retirer de mes satellites"
    @click="toggleModal()"
    :disabled="loading"
    icon="fr-icon-close-line"
    class="canteen-button-unlink"
  />
  <DsfrModal
    v-if="opened"
    :opened="opened"
    class="canteen-button-unlink__modal fr-modal--opened"
    :title="`Souhaitez-vous vraiment retirer le restaurant «&nbsp;${satellite.name}&nbsp;» de vos satellites ?`"
    @close="toggleModal()"
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
          toggleModal()
        },
      },
    ]"
  >
    <template #default>
      <p class="fr-mb-2w">
        En confirmant cette demande « {{ satellite.name }} » ne fera plus parti des restaurants fournis par votre
        établissement « {{ canteen.name }} » et donc :
      </p>
      <ul>
        <li>
          <p>
            vous ne pourrez plus télédéclarer ses données
          </p>
        </li>
        <li>
          <p>
            si vous avez déjà effecté une télédéclaration ses donnnées seront conservées
          </p>
        </li>
      </ul>
    </template>
  </DsfrModal>
</template>

<style lang="scss">
.canteen-button-unlink {
  color: var(--text-action-high-red-marianne) !important;
  box-shadow: inset 0 0 0 1px var(--text-action-high-red-marianne) !important;

  &__modal {
    white-space: initial !important;
  }
}
</style>
