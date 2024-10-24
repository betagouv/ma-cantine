<template>
  <div>
    <div v-for="section in sections" :key="section.title">
      <h2 class="mt-8 mb-4">{{ section.title }}</h2>
      <DsfrAccordion :items="section.questions">
        <template v-slot:content="{ item }">
          <component :is="item.component" />
        </template>
      </DsfrAccordion>
    </div>

    <div class="mt-6 d-flex">
      <v-btn large :to="{ name: 'ContactPage' }" outlined color="primary">
        <v-icon class="mr-2">mdi-help-circle</v-icon>
        Soumettre une nouvelle question
      </v-btn>
    </div>
  </div>
</template>

<script>
import faqSections from "@/data/faq-sections.json"
import DsfrAccordion from "@/components/DsfrAccordion"
import SiretRequired from "./AnswerComponents/SiretRequired"
import NoSiret from "./AnswerComponents/NoSiret"
import HowToSignUp from "./AnswerComponents/HowToSignUp"
import ProviderObligation from "./AnswerComponents/ProviderObligation"

export default {
  name: "FaqPanels",
  components: { DsfrAccordion, SiretRequired, NoSiret, HowToSignUp, ProviderObligation },
  data() {
    return {
      sections: faqSections,
    }
  },
}
</script>
