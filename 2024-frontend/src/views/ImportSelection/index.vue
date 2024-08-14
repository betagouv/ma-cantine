<script setup>
import { ref, computed } from "vue"
import BreadcrumbsNav from "@/components/BreadcrumbsNav.vue"
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

const expandedId = ref("")

const quizSteps = [
  {
    title: "Cantines",
    question: "Est-ce que vos cantines sont déjà créées ?",
  },
  { title: "Achats", question: "Souhaitez-vous importer des achats ?" },

  { title: "Bilans", question: "Souhaitez-vous créer et/ou mettre à jour des bilans pour vos cantines ?" },
  { title: "Cuisine centrale", question: "Est-ce que vous gérez une ou plusieurs cuisines centrales ?" },
  {
    title: "Cantine satellites",
    question: "Est-ce que vous connaissez les totaux d'approvisionnement par cantine satellite ?",
  },
  {
    title: "Bilans détaillés",
    question: "Est-ce que vous connaissez les totaux des achats par famille de produit et par label de qualité ?",
  },
]
const currentStep = ref(1)
const stepTitles = quizSteps.map((step) => step.title)
const step = computed(() => quizSteps[currentStep.value - 1])
const currentAnswer = ref("")
const revealAnswer = ref(false)

const handleChoice = () => {
  if (currentStep.value !== quizSteps.length) currentStep.value++
  else revealAnswer.value = true
  currentAnswer.value = ""
}
</script>

<template>
  <div>
    <BreadcrumbsNav :links="[{ title: 'Mon tableau de bord', to: { name: 'ManagementPage' } }]" />
    <h1>Importer vos données</h1>
    <p>
      Vous êtes en mesure d'exporter vos données en format CSV ? Utilisez notre outil d'import pour ajouter vos cantines
      rapidement&nbsp;!
    </p>
    <p>
      Sinon, utilisez notre
      <router-link :to="{ name: 'NewCanteen' }">formulaire pour ajouter une nouvelle cantine</router-link>
      tout en simplicité depuis votre navigateur.
    </p>
    <div>
      <h2>Remplissez ce quiz pour trouver le bon import pour votre situation</h2>
      <div v-if="!revealAnswer">
        <DsfrStepper :steps="stepTitles" :currentStep />
        <DsfrBooleanRadio :legend="step.question" @change="handleChoice" :name="step.title" v-model="currentAnswer" />
      </div>
      <div v-else>
        <p>You're a winner!</p>
      </div>
    </div>

    <DsfrAccordion id="import-list" title="Tous les imports" :expanded-id="expandedId" @expand="expandedId = $event">
      <div>
        <ul>
          <li v-for="importType in importTypes" :key="importType.key">
            <router-link :to="importType.to">{{ importType.title }}</router-link>
          </li>
        </ul>
      </div>
    </DsfrAccordion>
  </div>
</template>
