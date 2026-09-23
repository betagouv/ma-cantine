<script setup>
import { computed } from "vue"
import AppErrorList from "@/components/AppErrorList.vue"

const props = defineProps(["opened", "errors"])
const emit = defineEmits(["close", "continue"])
const title = computed(() => props.errors.length > 1 ? "Erreurs détectées" : "Erreur détectée")
</script>

<template>
  <DsfrModal
    :opened="opened"
    :title="title"
    @close="emit('close')"
  >
    <p>Lors de l'enregistrement de vos données, nous avons détecté une ou plusieurs erreurs : </p>
    <AppErrorList :errors="errors.map((error) => error.field)" />
    <p>Vous n'êtes pas obligé de faire la correction maintenant mais vous devrez la faire avant de télédéclarer.</p>
    <div class="ma-cantine--flex-end">
      <DsfrButton
        secondary
        icon="fr-icon-edit-line"
        label="Revenir et corriger"
        @click="emit('close')"
        :icon-right="true"
      />
      <DsfrButton
        primary
        label="Continuer et corriger plus tard"
        @click="emit('continue')"
      />
    </div>
  </DsfrModal>
</template>
