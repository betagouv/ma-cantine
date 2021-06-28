<template>
  <v-card class="pa-6">
    <div class="mt-n6 mx-n6 mb-4 pa-4 d-flex" style="background-color: #F5F5F5">
      <v-spacer></v-spacer>
      <v-btn color="primary" outlined @click="$emit('closeModal')">
        Fermer
      </v-btn>
    </div>

    <div>
      <video
        ref="video"
        style="width: 100%; background: #333;"
        poster="/static/images/video-poster-tableur.webp"
        controls
      >
        <source
          type="video/mp4"
          src="https://cellar-c2.services.clever-cloud.com/ma-cantine-egalim/videos/demo-tableur-approvisionnements.mp4"
        />
        Votre navigateur ne peut pas afficher des vidéos.
      </video>
    </div>

    <v-container>
      <p id="download-cta" class="mb-6"><b>Télécharger notre tableur</b></p>
      <v-row aria-labelledby="download-cta">
        <v-spacer></v-spacer>
        <v-btn :href="`${filepath}.ods`" download class="primary mx-2">
          Format .ods
        </v-btn>
        <v-btn :href="`${filepath}.xlsx`" download class="primary mx-2">
          Format .xlsx
        </v-btn>
        <v-spacer></v-spacer>
      </v-row>
    </v-container>
  </v-card>
</template>

<script>
export default {
  data() {
    return {
      filepath: "/static/documents/Diagnostic approvisionnement (ma-cantine-alpha) v0.5",
    }
  },
  methods: {
    stopVideo() {
      this.$refs.video.pause()
      this.$refs.video.currentTime = 0
    },
  },
}
</script>
