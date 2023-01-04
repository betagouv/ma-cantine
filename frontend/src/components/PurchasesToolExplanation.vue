<template>
  <v-expansion-panels hover accordion tile flat>
    <v-expansion-panel>
      <v-expansion-panel-header expand-icon="mdi-plus" disable-icon-rotate class="py-0">
        <v-row>
          <v-icon class="mr-2">$question-line</v-icon>
          <p class="my-3 caption">
            Comment utiliser le suivi d'achats ?
          </p>
        </v-row>
      </v-expansion-panel-header>
      <v-expansion-panel-content class="faq-answer">
        <v-card
          class="pa-3"
          :class="{ 'd-flex': true, 'flex-column': $vuetify.breakpoint.xs, 'align-center': $vuetify.breakpoint.xs }"
          outlined
        >
          <div
            :style="
              `max-width: ${
                $vuetify.breakpoint.xs ? '70%' : '50%'
              }; background: #333; border-radius: 10px; position: relative; overflow: hidden;`
            "
          >
            <iframe
              src="https://www.loom.com/embed/c22baca19c6f4df39d426d312da2a33f"
              frameborder="0"
              webkitallowfullscreen
              mozallowfullscreen
              allowfullscreen
              width="100%"
            ></iframe>
          </div>

          <div>
            <p class="ma-4">
              Régardez notre vidéo tutorial pour repondre aux questions les plus fréquentes.
              <br />
              <br />
              Si vous avez toujours des questions ou des problèmes, n'hésitez pas à nous contacter à
              <a href="mailto:contact@egalim.beta.gouv.fr">contact@egalim.beta.gouv.fr</a>
              .
            </p>
          </div>
        </v-card>
      </v-expansion-panel-content>
    </v-expansion-panel>
  </v-expansion-panels>
</template>

<script>
export default {
  name: "BadgesExplanation",
}
</script>
