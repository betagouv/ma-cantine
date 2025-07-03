<script setup>
import { useRoute } from "vue-router"
import { groups } from "@/constants/questions-answers.js"
import AppNeedHelp from "@/components/AppNeedHelp.vue"
import AppLinkRouter from "@/components/AppLinkRouter.vue"
import AppMultipleAccordionsGroup from "@/components/AppMultipleAccordionsGroup.vue"

const route = useRoute()
const readingDoodleIllustration = "/static/images/doodles-dsfr/primary/ReadingDoodle.png"
</script>

<template>
  <section class="fr-col-12 fr-col-lg-8 fr-mb-4w fr-mb-md-10w">
    <h1>{{ route.meta.title }}</h1>
    <p>
      Vous n'êtes pas familier avec les obligations réglementaires ? Vous vous posez des questions sur votre
      responsabilité ? Vous avez besoin d'aide sur plusieurs aspects techniques ou légaux ? Rassurez-vous ! Vous
    </p>
  </section>
  <section class="fr-grid-row fr-grid-row--top fr-mb-4w fr-mb-md-10w">
    <div class="fr-col-12 fr-col-lg-8">
      <AppMultipleAccordionsGroup v-for="(group, index) in groups" :key="index" :group="group" />
    </div>
    <div class="fr-hidden fr-unhidden-lg fr-col-4 fr-grid-row fr-grid-row--right ma-cantine--sticky">
      <img :src="readingDoodleIllustration" class="faq__illustration" />
    </div>
  </section>
  <AppNeedHelp badge="Une suggestion" title="Vous ne trouvez pas ce que vous cherchez ?">
    <p>
      N'hésitez pas à nous soumettre une nouvelle question, en nous contactant
      <br />
      <AppLinkRouter title="via notre formulaire de contact" :to="{ name: 'Contact' }"></AppLinkRouter>
    </p>
  </AppNeedHelp>
</template>

<style lang="scss">
.faq {
  &__illustration {
    width: 10rem;
  }
}
</style>
