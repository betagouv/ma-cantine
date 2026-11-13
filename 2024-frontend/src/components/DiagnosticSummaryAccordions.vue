<script setup>
import { ref, watch } from "vue"
import { useRouter } from "vue-router"
import AppLinkRouter from "@/components/AppLinkRouter.vue"
import DiagnosticSummaryAppro from "@/components/DiagnosticSummaryAppro.vue"
import DiagnosticSummaryThematiques from "@/components/DiagnosticSummaryThematiques.vue"

const props = defineProps(['volets', 'open', 'anchorName', 'isTeledeclared', 'diagnosticRecap'])
const activeAccordion = ref(props.open)
watch(() => props.open, (value) => activeAccordion.value = value)

/* Navigation */
const router = useRouter()
const goToPage = (page) => router.push(page)

/* Sentence */
const getSentence = (volet) => {
  if (volet.isFilled && !volet.hasErrors) return "Volet non télédéclaré."
  if (volet.isFilled && volet.hasErrors && !volet.isAppro) return "Volet en attente de finalisation."
  if (volet.isFilled && volet.hasErrors) return "Volet en attente de correction."
  return "Volet non renseigné."
}

const isVoletTeledeclared = (volet) => {
  if (props.isTeledeclared && volet.isAppro) return true
  if (props.isTeledeclared && !volet.isAppro && !volet.hasErrors && volet.isFilled) return true
  return false
}

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
          <component :is="volet.macaron" :status="volet.macaronStatus" class="diagnostic-summary-accordions__image" />
          {{ volet.title }}
          <DsfrBadge v-if="volet.hasErrors" :label="volet.isAppro ? 'Erreurs' : 'Non finalisé'" type="error"/>
        </span>
      </template>
      <p v-if="!isVoletTeledeclared(volet)" class="fr-mb-0">
        <span class="fr-text--bold">{{ getSentence(volet) }}</span>
        <br>
        Consulter le volet <AppLinkRouter :to="volet.page" :title="volet.title.toLowerCase()"/>
      </p>
      <DiagnosticSummaryAppro
        v-if="volet.isAppro && isTeledeclared"
        :diagnostic-recap="diagnosticRecap"
      />
      <DiagnosticSummaryThematiques
        v-else-if="isTeledeclared && isVoletTeledeclared(volet)"
        :diagnostic-recap="diagnosticRecap"
        :volet-key="volet.key"
      />
      <div v-if="isVoletTeledeclared(volet)" class="ma-cantine--flex-end fr-mt-2w">
        <DsfrButton v-if="!volet.isAppro" @click="goToPage(volet.page)" secondary :label="`Modifier le volet ${volet.title.toLowerCase()}`" icon="fr-icon-edit-line" size="sm"/>
      </div>
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
