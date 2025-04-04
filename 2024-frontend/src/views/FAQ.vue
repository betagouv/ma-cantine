<script setup>
import { useRoute } from "vue-router"
import { groups } from "@/constants/questions-answers.js"

const route = useRoute()
</script>

<template>
  <section class="fr-col-12 fr-col-md-7 fr-mb-10w">
    <h1>{{ route.meta.title }}</h1>
    <p>
      Vous n'êtes pas familier avec les obligations réglementaires ? Vous vous posez des questions sur votre
      responsabilité ? Vous avez besoin d'aide sur plusieurs aspects techniques ou légaux ? Rassurez-vous ! Vous n'êtes
      pas les seuls à vous poser ces questions.
    </p>
  </section>
  <section>
    <DsfrAccordionsGroup v-for="(group, index) in groups" :key="index" class="fr-mb-5w">
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
</template>
