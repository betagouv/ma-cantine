<script setup>
import { useRouter } from "vue-router"

const router = useRouter()
defineProps(["message", "opened"])
</script>

<template>
  <DsfrModal
    :opened="opened"
    class="fr-modal--opened"
    title="Le fichier a été importé avec succès"
    icon="fr-icon-checkbox-circle-fill"
    @close="$emit('close')"
    :actions="[
      {
        label: 'Aller sur mon tableau de bord',
        onClick() {
          router.push({ name: 'GestionnaireTableauDeBord' })
        },
      },
      {
        label: 'Importer un autre fichier',
        secondary: true,
        onClick() {
          $emit('close')
        },
      },
    ]"
  >
    <template #default>
      <p class="ma-cantine--bold">
        {{ message }}
      </p>
      <p>
        Depuis votre tableau de bord, vous devez télédéclarer vos données, lorsque la campagne de télédéclaration est
        ouverte.
      </p>
    </template>
  </DsfrModal>
</template>
