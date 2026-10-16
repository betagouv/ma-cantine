<script setup>
import { ref, watch, computed } from "vue"
import { useRouter } from "vue-router"
import AppLinkRouter from "@/components/AppLinkRouter.vue"
import GraphEgalim from "@/components/GraphEgalim.vue"

const props = defineProps(['volets', 'open', 'anchorName', 'isTeledeclared', 'diagnosticRecap'])
const activeAccordion = ref(props.open)
watch(() => props.open, (value) => activeAccordion.value = value)

/* Appro */
const approStats = computed(() => props.diagnosticRecap?.canteenDiagnosticApproStats)
const objectives = computed(() => props.diagnosticRecap?.notes)

/* Navigation */
const router = useRouter()
const goToPage = (page) => router.push(page)
</script>
<template>
  <DsfrAccordionsGroup v-model="activeAccordion" :id="anchorName" class="diagnostic-summary-accordions">
    <DsfrAccordion
      v-for="(volet, index) in volets"
      :key="volet.title"
      :id="`diagnostic-summary-accordion-${index}`"
      :title="volet.title"
    >
      <template #title>
        <span class="ma-cantine--flex-start ma-cantine--flex-gap-1">
          <component :is="volet.macaron" :status="volet.status" class="diagnostic-summary-accordions__image" />
          {{ volet.title }}
          <DsfrBadge v-if="volet.displayErrors" label="Erreurs" type="error"/>
        </span>
      </template>
      <p v-if="!isTeledeclared" class="fr-mb-0">
        <span class="fr-text--bold">{{ volet.sentence }}</span>
        <br>
        Consulter le volet <AppLinkRouter :to="volet.page" :title="volet.title.toLowerCase()"/>
      </p>
      <div v-else class="ma-cantine--flex-end">
        <DsfrButton @click="goToPage(volet.page)" secondary :label="`Modifier le volet ${volet.title.toLowerCase()}`" icon="fr-icon-edit-line" size="sm"/>
      </div>
      <GraphEgalim
        v-if="volet.key === 'appro' && isTeledeclared"
        :egalim-percent="approStats.pourcentageEgalim"
        :bio-percent="approStats.pourcentageBio"
        :viandes-poissons-egalim-percent="approStats.pourcentageViandesVolaillesProduitsDeLaMerEgalim"
        :egalim-objective="objectives.egalimPercentObjective"
        :bio-objective="objectives.bioPercentObjective"
        :description-custom="`pour le bilan ${diagnosticRecap.year}`"
      />
    </DsfrAccordion>
  </DsfrAccordionsGroup>
</template>

<style lang="scss" scoped>
.diagnostic-summary-accordions {
  &__image {
    flex: 0 0 auto;
    width: 2rem;
    height: 2rem;
  }
}
</style>
