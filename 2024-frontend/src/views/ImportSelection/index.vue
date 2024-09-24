<script setup>
import { ref, computed, watch } from "vue"
import DsfrBooleanRadio from "@/components/DsfrBooleanRadio.vue"
import Constants from "@/constants.js"

const importTypes = []
Object.values(Constants.DiagnosticImportLevels).forEach((level) => {
  level.to = { name: "DiagnosticImportPage", params: { importUrlSlug: level.urlSlug } }
  importTypes.push(level)
})
Object.values(Constants.CentralKitchenImportLevels).forEach((level) => {
  level.to = { name: "DiagnosticImportPage", params: { importUrlSlug: level.urlSlug } }
  importTypes.push(level)
})
importTypes.push({
  key: "PURCHASES",
  title: "Importer des achats",
  help: "Vous voulez importer des données d'achat pour des cantines existantes",
  to: { name: "PurchasesImporter" },
})

const activeAccordion = ref("")

const quizSteps = [
  {
    key: "hasCanteens",
    title: "Cantines",
    question: "Est-ce que vos cantines sont déjà existantes sur la plateforme ma cantine ? ",
  },
  { key: "importPurchases", title: "Achats", question: "Souhaitez-vous importer des achats ?" },
  {
    key: "importDiagnostics",
    title: "Bilans",
    question: "Souhaitez-vous créer et/ou mettre à jour des bilans pour vos cantines ?",
  },
  {
    key: "isCentralKitchen",
    title: "Livreur de repas",
    question: "Est-ce que un ou plusieurs de ces établissements livrent des repas aux cantines ?",
  },
  {
    key: "hasSatelliteData",
    title: "Cantines satellites",
    question: "Est-ce que vous connaissez les totaux d'approvisionnement par cantine satellite ?",
  },
  {
    key: "hasDetailedDiagnosticData",
    title: "Déclaration détaillée",
    question: "Est-ce que vous connaissez les totaux des achats par famille de produit et par label de qualité ?",
  },
]
const currentStep = ref(1)
const stepTitles = quizSteps.map((step) => step.title)
const step = computed(() => quizSteps[currentStep.value - 1])
const currentAnswer = ref(undefined)
const answers = ref({})
const importSuggestionKey = ref("")
const importSuggestion = computed(() => {
  if (!importSuggestionKey.value) return
  const suggestion = importTypes.find((type) => type.key === importSuggestionKey.value)
  suggestion.to = suggestion.to || { name: "DiagnosticImportPage", params: { importUrlSlug: suggestion.urlSlug } }
  return suggestion
})
const revealAnswer = computed(() => !!importSuggestionKey.value)

const handleChoice = () => {
  const value = !!currentAnswer.value
  currentAnswer.value = undefined
  switch (step.value.key) {
    case "hasCanteens":
      if (value) break
      importSuggestionKey.value = "NONE"
      return
    case "importPurchases":
      if (!value) break
      importSuggestionKey.value = "PURCHASES"
      return
    case "importDiagnostics":
      if (value) break
      importSuggestionKey.value = "NONE"
      return
    case "isCentralKitchen":
      answers.value.isCentralKitchen = value
      if (value) break
      currentStep.value++ // skip satellite question
      break
    case "hasSatelliteData":
      answers.value.hasSatelliteData = value
      break
    case "hasDetailedDiagnosticData":
      if (answers.value.isCentralKitchen && !answers.value.hasSatelliteData) {
        importSuggestionKey.value = value ? "CC_COMPLETE" : "CC_SIMPLE"
      } else {
        importSuggestionKey.value = value ? "COMPLETE" : "SIMPLE"
      }
  }

  if (currentStep.value < quizSteps.length) currentStep.value++
}

const reset = () => {
  answers.value = {}
  currentStep.value = 1
  importSuggestionKey.value = ""
}

const back = () => {
  const skippedSatelliteQuestion = !answers.value.isCentralKitchen
  if (step.value.key === "hasDetailedDiagnosticData" && skippedSatelliteQuestion) currentStep.value--
  currentStep.value--
}

const backToLastQuestion = () => {
  importSuggestionKey.value = ""
}

watch(currentStep, () => (currentAnswer.value = undefined))
</script>

<template>
  <div>
    <h1>Importer vos données</h1>
    <p>Complétez le formulaire ci-dessous pour trouver le fichier adapté à votre situation.</p>
    <div class="fr-mb-8w">
      <div v-if="!revealAnswer">
        <DsfrStepper :steps="stepTitles" :currentStep />
        <DsfrBooleanRadio :legend="step.question" @change="handleChoice" :name="step.title" v-model="currentAnswer" />
        <DsfrButton @click="back" tertiary :disabled="currentStep === 1">
          Revenir à l'étape précédente
        </DsfrButton>
      </div>
      <div v-else>
        <div class="fr-col-md-6 fr-col-lg-5 fr-mb-4w">
          <DsfrCard :title="importSuggestion.title" :description="importSuggestion.help" :link="importSuggestion.to" />
        </div>
        <DsfrButton @click="backToLastQuestion" tertiary v-if="currentStep !== 1" class="fr-mr-2w">
          Revenir à l'étape précédente
        </DsfrButton>
        <DsfrButton @click="reset" secondary>Réessayer</DsfrButton>
      </div>
    </div>

    <DsfrAccordionsGroup v-model="activeAccordion">
      <DsfrAccordion id="import-list" title="Voir tous les imports disponibles" class="fr-my-4w">
        <div>
          <ul>
            <li v-for="importType in importTypes" :key="importType.key">
              <router-link :to="importType.to">{{ importType.title }}</router-link>
            </li>
          </ul>
        </div>
      </DsfrAccordion>
    </DsfrAccordionsGroup>
  </div>
</template>
