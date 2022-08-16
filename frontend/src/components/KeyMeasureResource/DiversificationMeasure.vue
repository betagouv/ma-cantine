<template>
  <div>
    <v-card
      href="https://ma-cantine-1.gitbook.io/ma-cantine-egalim/diversification-des-sources-de-proteines-et-menus-vegetariens/guide-pour-la-mise-en-place-du-menu-vegetarien-en-milieu-scolaire"
      class="text-decoration-none text-left mt-4"
      target="_blank"
      rel="noopener"
      hover
    >
      <DsfrCallout icon="mdi-carrot" class="text-body-2 mb-0" color="#00A95F">
        Vous pouvez accéder à un guide sur le menu végétarien hebdomadaire en restauration scolaire ou notre livret de
        recettes pour menus végétariens dans nos ressources.
        <v-icon color="black" small class="pb-1">mdi-open-in-new</v-icon>
      </DsfrCallout>
    </v-card>
    <v-card
      href="https://ma-cantine-1.gitbook.io/ma-cantine-egalim/diversification-des-sources-de-proteines-et-menus-vegetariens/untitled"
      class="text-decoration-none text-left mt-4"
      target="_blank"
      rel="noopener"
      hover
    >
      <DsfrCallout icon="mdi-carrot" class="text-body-2 mb-0" color="#00A95F">
        Accéder le cadre général du plan pluriannuel de diversification des sources de protéines.
        <v-icon color="black" small class="pb-1">mdi-open-in-new</v-icon>
      </DsfrCallout>
    </v-card>
  </div>
</template>

<script>
import DsfrCallout from "@/components/DsfrCallout"

export default {
  components: { DsfrCallout },
}
</script>
