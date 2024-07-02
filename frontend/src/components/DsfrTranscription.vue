<template>
  <v-expansion-panels hover accordion tile flat class="dsfr-transcription">
    <v-expansion-panel>
      <v-expansion-panel-header class="px-3 fr-accordion__btn" v-slot="{ open }">
        <component :is="titleLevel" class="fr-text d-flex align-center" :class="open && 'active-panel'">
          <v-icon small color="primary" class="mr-2">$menu-2-fill</v-icon>
          Transcription
        </component>
      </v-expansion-panel-header>
      <v-expansion-panel-content>
        <div class="px-4 pt-4 pb-4">
          <slot />
        </div>
        <div class="transcription-footer pa-2">
          <v-dialog
            v-model="transcriptionModal"
            :fullscreen="$vuetify.breakpoint.smAndDown"
            :width="$vuetify.breakpoint.mdAndUp ? 900 : undefined"
          >
            <template v-slot:activator="{ on, attrs }">
              <v-btn v-bind="attrs" v-on="on" text class="primary--text">
                Agrandir
                <v-icon small class="ml-2">mdi-arrow-expand-all</v-icon>
              </v-btn>
            </template>

            <v-card class="px-sm-4 pt-6 pb-8 text-left">
              <v-row class="justify-end ma-0">
                <v-btn @click="transcriptionModal = false" class="primary--text" text>
                  Fermer
                  <v-icon small color="primary" class="ml-2">$close-line</v-icon>
                </v-btn>
              </v-row>
              <v-card-title>
                <!-- TODO: should this be configurable? -->
                <h1 class="fr-h2 mb-4">Transcription</h1>
              </v-card-title>

              <v-card-text>
                <slot />
              </v-card-text>
            </v-card>
          </v-dialog>
        </div>
      </v-expansion-panel-content>
    </v-expansion-panel>
  </v-expansion-panels>
</template>

<script>
export default {
  name: "DsfrTranscription",
  props: {
    titleLevel: {
      type: String,
      default: "h3",
    },
  },
  data() {
    return {
      transcriptionModal: false,
    }
  },
}
</script>

<style>
.dsfr-transcription .v-expansion-panel {
  box-shadow: inset 1px 1px 0 0 #ddd, 1px 1px 0 0 #ddd;
}
.dsfr-transcription .v-expansion-panel-content__wrap {
  padding: 0;
}
.dsfr-transcription .v-expansion-panel-header {
  color: rgb(0, 0, 145);
}
.dsfr-transcription .v-expansion-panel-header i {
  color: rgb(0, 0, 145) !important;
}
.dsfr-transcription .v-expansion-panel--active > .v-expansion-panel-header {
  min-height: unset;
}
.dsfr-transcription .fr-accordion__btn[aria-expanded="true"] {
  --background-open-blue-france: rgb(227, 227, 253);
  background-color: #e3e3fd;
  background-color: var(--background-open-blue-france);
}
.dsfr-transcription .fr-accordion__btn[aria-expanded="true"]:hover {
  --background-open-blue-france-hover: rgb(193, 193, 251);
  background-color: var(--background-open-blue-france-hover);
}
.transcription-footer {
  box-shadow: inset 1px 1px 0 0 #ddd, 1px 1px 0 0 #ddd;
  text-align: right;
}
</style>
