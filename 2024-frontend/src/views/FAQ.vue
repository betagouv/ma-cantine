<script setup>
import { useRoute } from "vue-router"
import { groups } from "@/constants/questions-answers.js"
import AppNeedHelp from "@/components/AppNeedHelp.vue"
import AppLinkRouter from "@/components/AppLinkRouter.vue"

const route = useRoute()
</script>

<template>
  <section class="fr-mb-4w fr-mb-lg-10w fr-grid-row">
    <div class="fr-col-12 fr-col-lg-8">
      <h1>{{ route.meta.title }}</h1>
      <p>
        Vous n'êtes pas familier avec les obligations réglementaires ? Vous vous posez des questions sur votre
        responsabilité ? Vous avez besoin d'aide sur plusieurs aspects techniques ou légaux ? Rassurez-vous ! Vous
        n'êtes pas les seuls à vous poser ces questions.
      </p>
    </div>
    <div class="fr-hidden fr-unhidden-lg fr-col-4 fr-grid-row fr-grid-row--center">
      <img src="/static/images/doodles-dsfr/primary/ReadingDoodle.png" class="faq-illustration" />
    </div>
  </section>
  <section class="fr-grid-row fr-grid-row--center">
    <DsfrAccordionsGroup v-for="(group, index) in groups" :key="index" class="fr-col-12 fr-col-lg-8 fr-mb-5w">
      <h2 class="fr-h5">{{ group.title }}</h2>
      <DsfrAccordion
        v-for="(accordion, index) in group.accordions"
        :key="index"
        :title="accordion.question"
        title-tag="h3"
      >
        <component v-if="accordion.component" :is="accordion.component"></component>
        <p v-else>{{ accordion.answer }}</p>
      </DsfrAccordion>
    </DsfrAccordionsGroup>
  </section>
  <AppNeedHelp badge="Une suggestion" title="Vous ne trouvez pas ce que vous cherchez ?">
    <p>
      N'hésitez pas à nous soumettre une nouvelle question, en nous contactant
      <br />
      <AppLinkRouter title="via notre formulaire de contact" :to="{ name: 'ContactPage' }"></AppLinkRouter>
    </p>
  </AppNeedHelp>
</template>

<style lang="scss">
.faq-illustration {
  width: 10rem;
}
</style>
