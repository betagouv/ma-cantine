<script setup>
import { ref, computed } from "vue"
import { storeToRefs } from "pinia"
import { useStoreTeledeclaration } from "@/stores/teledeclaration.js"
import AppLinkRouter from "@/components/AppLinkRouter.vue"

/* Diagnostic */
const teledeclarationStore = useStoreTeledeclaration()
const { diagnostic, isTeledeclared, hasErrors, hasDiagnostic } = storeToRefs(teledeclarationStore)

/* Get data */
const getIsStarted = (key) => {
  if (key === "appro") return hasDiagnostic.value
  else return false
}

const getImage = (key) => {
  return `/static/images/badges/badge-${key}-disabled.svg`
}

const getSentence = (key) => {
  const isStarted = getIsStarted(key)
  if (!isStarted) return "Volet non renseigné."
  if (key === "appro") return hasErrors.value ? "Volet en attente de correction." : "Volet non télédéclaré."
  return isTeledeclared.value ? "Volet non télédéclaré." : "Volet non renseigné."
}

/* Accordions */
const activeAccordion = ref()
const accordions = computed(() => {
  return [
    {
      title: "Approvisionnements",
      image: getImage("appro"),
      sentence: getSentence("appro"),
      page: { name: "GestionnaireTunnelApproRecapitulatif" }
    },
    {
      title: "Informations convives",
      image: getImage("info"),
      sentence: getSentence("info"),
      page: { name: "GestionnaireTunnelConvives" }
    },
    {
      title: "Lutte contre le gaspillage alimentaire",
      image: getImage("waste"),
      sentence: getSentence("waste"),
      page: { name: "GestionnaireTunnelGaspillage" }
    },
    {
      title: "Diversification des sources de protéines et menus végétariens",
      image: getImage("diversification"),
      sentence: getSentence("diversification"),
      page: { name: "GestionnaireTunnelVegetarien" }
    },
    {
      title: "Substitutions plastiques",
      image: getImage("plastic"),
      sentence: getSentence("plastic"),
      page: { name: "GestionnaireTunnelPlastique" }
    }
  ]
})
</script>
<template>
  <DsfrAccordionsGroup v-model="activeAccordion" class="diagnostic-summary-accordions fr-mb-5w">
    <DsfrAccordion
      v-for="(accordion, index) in accordions"
      :key="accordion.title"
      :id="`diagnostic-summary-accordion-${index}`"
      :title="accordion.title"
    >
      <template #title>
        <span class="ma-cantine--flex-start ma-cantine--flex-gap-1">
          <img :src="accordion.image" alt="" class="diagnostic-summary-accordions__image" />
          {{ accordion.title }}
        </span>
      </template>
      <p v-if="!isTeledeclared" class="fr-mb-0">
        <span class="fr-text--bold">{{ accordion.sentence }}</span>
        <br>
        Consulter le volet <AppLinkRouter :to="accordion.page" :title="accordion.title.toLowerCase()"/>
      </p>
      <div v-else class="ma-cantine--flex-end">
        <DsfrButton @click="goToPage(accordion.page)" secondary :label="`Modifier le volet ${accordion.title.toLowerCase()}`" icon="fr-icon-edit-line" size="sm"/>
      </div>
    </DsfrAccordion>
  </DsfrAccordionsGroup>
  <pre>{{ diagnostic }}</pre>
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
