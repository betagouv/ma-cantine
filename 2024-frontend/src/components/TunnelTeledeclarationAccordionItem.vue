<script setup>
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useStoreCanteen } from '@/stores/canteen'
import CanteenDisplayInformations from '@/components/CanteenDisplayInformations.vue'

defineProps(["accordion", "id"])

/* Router */
const router = useRouter()

/* Stores */
const canteenStore = useStoreCanteen()
const { canteenInformations } = storeToRefs(canteenStore)

/* Data */
const header = [
  { key: "name", label: "Champ" },
  { key: "value", label: "Valeur" },
]

const goToStep = (page) => router.push(page)
</script>

<template>
  <DsfrAccordion :id="id" :title="accordion.title">
    <CanteenDisplayInformations
      v-if="accordion.isCanteenFields"
      :canteenInformation="canteenInformations"
      :canteenIsGroupe="canteenInformations.isGroupe"
    />
    <DsfrDataTable
      v-else
      title="Données enregistrées"
      no-caption
      :headersRow="header"
      :rows="accordion.rows"
      :no-scroll="true"
      class="fr-mb-2w fr-mt-0"
    />
    <DsfrButton label="Modifier ces données" @click="goToStep(accordion.to)" icon="ri-pencil-line" secondary size="sm" />
  </DsfrAccordion>
</template>
