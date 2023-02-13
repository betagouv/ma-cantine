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
            <video
              ref="video"
              style="width: 100%; background: #333;"
              poster="/static/images/video-poster-achats.webp"
              controls
            >
              <source
                type="video/mp4"
                src="https://cellar-c2.services.clever-cloud.com/ma-cantine-egalim/videos/Mes achats - ma cantine - 3 January 2023.mp4"
              />
              Votre navigateur ne peut pas afficher des vidéos.
            </video>
          </div>

          <div>
            <p class="ma-4">
              Régardez notre vidéo tutorial pour repondre aux questions les plus fréquentes.
              <br />
              <br />
              Si vous avez toujours des questions ou des problèmes, n'hésitez pas à nous contacter à
              <a href="mailto:support-egalim@beta.gouv.fr">support-egalim@beta.gouv.fr</a>
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
