<template>
  <div class="text-left">
    <BreadcrumbsNav />
    <v-row align="center">
      <v-col cols="12" sm="10" class="pb-12">
        <h1 class="text-h4 font-weight-black mb-8">Foire aux questions</h1>
        <p>
          Vous n'êtes pas familier avec les obligations réglementaires ? Vous vous posez des questions sur votre
          responsabilité ? Vous avez besoin d'aide sur plusieurs aspects techniques ou légaux ? Rassurez-vous ! Vous
          n'êtes pas les seuls à vous poser ces questions.
        </p>
      </v-col>
      <v-col cols="2">
        <v-img
          src="/static/images/doodles-dsfr/primary/ReadingDoodle.png"
          v-if="$vuetify.breakpoint.smAndUp"
          class="mx-auto rounded-0"
          contain
          max-width="100%"
        ></v-img>
      </v-col>
    </v-row>
    <FaqPanels id="faq" />
  </div>
</template>

<script>
import BreadcrumbsNav from "@/components/BreadcrumbsNav"
import FaqPanels from "./FaqPanels"

export default {
  name: "FaqPage",
  components: { FaqPanels, BreadcrumbsNav },
}
</script>
