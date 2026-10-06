<script setup>
import { ref, watch } from "vue"
import { useRouter } from "vue-router"
import AppLinkRouter from "@/components/AppLinkRouter.vue"

const props = defineProps(['volets', 'open', 'anchorName', 'isTeledeclared'])
const activeAccordion = ref(props.open)
watch(() => props.open, (value) => activeAccordion.value = value)

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
          <component :is="volet.macaron" status="empty" class="diagnostic-summary-accordions__image" />
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
