<script setup>
import { useRoute } from "vue-router"
const route = useRoute()
</script>

<template>
  <section class="fr-col-12 fr-col-md-7">
    <h1>{{ route.meta.title }}</h1>
    <p>
      Vous n'êtes pas familier avec les obligations réglementaires ? Vous vous posez des questions sur votre
      responsabilité ? Vous avez besoin d'aide sur plusieurs aspects techniques ou légaux ? Rassurez-vous ! Vous n'êtes
      pas les seuls à vous poser ces questions.
    </p>
  </section>
</template>
