<template>
  <v-card class="pa-6">
    <div class="mt-n6 mx-n6 mb-4 pa-4 d-flex" style="background-color: #F5F5F5">
      <v-spacer></v-spacer>
      <v-btn color="primary" outlined @click="$emit('closeModal')">
        Fermer
      </v-btn>
    </div>

    <div class="calculator-i-frame">
      <iframe
        src="https://www.youtube-nocookie.com/embed/3i5-eDwU9mc"
        @load="iframeLoad"
        v-show="iframeIsLoaded"
        class="calculator-video"
        title="Vidéo de présentation du calculateur"
        frameborder="0"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowfullscreen
      />

      <div class="video-loader" v-show="!iframeIsLoaded">
        <v-progress-circular indeterminate></v-progress-circular>
        Chargement de la vidéo de présentation
      </div>
    </div>

    <v-container>
      <p id="download-cta" class="mb-6"><b>Télécharger notre tableur</b></p>
      <v-row aria-labelledby="download-cta">
        <v-spacer></v-spacer>
        <v-btn :href="`/static/documents/${filename}.ods`" download class="primary mx-2">
          Format .ods
        </v-btn>
        <v-btn :href="`/static/documents/${filename}.xlsx`" download class="primary mx-2">
          Format .xlsx
        </v-btn>
        <v-spacer></v-spacer>
      </v-row>
    </v-container>
  </v-card>
</template>

<script>
export default {
  props: ["closeModal"],
  data() {
    return {
      iframeIsLoaded: false,
      filename: process.env.VUE_APP_APPRO_TABLE_NAME,
    }
  },
  methods: {
    iframeLoad() {
      this.iframeIsLoaded = true
    },
  },
}
</script>

<style scoped lang="scss">
h2 {
  text-align: center;
}

.calculator-i-frame {
  position: relative;
  width: 100%;
  padding-top: 70%;
  margin: 1em 0;

  .calculator-video {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
  }

  .video-loader {
    position: absolute;
    top: 50%;
    width: 100%;
    text-align: center;
    font-size: 26px;
  }
}

.calculator-download {
  display: block;
  width: 8em;
  padding: 0.4em;
  border-radius: 1.4em;
  text-align: center;
  margin: 30px auto 0 auto;
  color: $ma-cantine-white;
  font-size: 24px;
  background-color: $ma-cantine-orange;
  text-decoration: none;
}
</style>
