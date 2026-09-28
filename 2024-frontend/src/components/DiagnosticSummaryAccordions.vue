<script setup>
import { ref, computed } from "vue"
import { storeToRefs } from "pinia"
import { useStoreTeledeclaration } from "@/stores/teledeclaration.js"

const teledeclarationStore = useStoreTeledeclaration()
const { diagnostic } = storeToRefs(teledeclarationStore)

/* Data */
const getIsStarted = (key) => {
  console.log(key)
  return false
}

const getImage = (key) => {
  const suffix = getIsStarted(key) ? "" : "-disabled"
  return `/static/images/badges/badge-${key}${suffix}.svg`
}

/* Accordions */
const activeAccordion = ref()
const accordions = computed(() => {
  return [
    {
      title: "Approvisionnements",
      image: getImage("appro"),
      isStarted: getIsStarted("appro")
    },
    {
      title: "Informations convives",
      image: getImage("info"),
      isStarted: getIsStarted("info")
    },
    {
      title: "Lutte contre le gaspillage alimentaire",
      image: getImage("waste"),
      isStarted: getIsStarted("waste")
    },
    {
      title: "Diversification des sources de protéines et menus végétariens",
      image: getImage("diversification"),
      isStarted: getIsStarted("diversification")
    },
    {
      title: "Substitutions plastiques",
      image: getImage("plastic"),
      isStarted: getIsStarted("plastic")
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
      <p v-if="accordion.isStarted" class="fr-mb-0">Données saisies</p>
      <p v-else class="fr-mb-0">Ce volet n’a pas encore été renseigné.</p>
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
