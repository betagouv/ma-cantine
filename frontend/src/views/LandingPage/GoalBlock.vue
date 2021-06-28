<template>
  <div>
    <p class="text-h4 font-weight-black">Les enjeux de la restauration collective</p>
    <p class="text-left mt-8">
      La restauration collective représente près de
      <b>4 milliards de repas servis par an</b>
      dans plus de 90 000 sites de restauration, des cantines scolaires, des hopitaux, des EPHAD, des entreprises, des
      administrations... Agir sur la composition des assiettes est un levier fort pour améliorer l'impact sur notre
      santé et sur l'environnement tout en influançant positivement les filières d'agriculture biologique et de qualité.
      Les mesures en faveur d'une alimentation plus durable peuvent contribuer à modifier les comportements alimentaires
      notamment chez les plus jeunes.
    </p>

    <v-card elevation="0" color="secondary lighten-3" class="mt-8 pa-10">
      <v-card-text>
        <div style="position:relative;padding-bottom:56.25%;">
          <iframe
            src="https://www.youtube-nocookie.com/embed/kkQ3ttLFiD8"
            title="Vidéo présentation d'Egalim"
            frameborder="0"
            @load="iframeLoad"
            style="width:100%;height:100%;position:absolute;left:0px;top:0px;"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowfullscreen
          />
        </div>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
export default {
  data() {
    return {
      iframeIsLoaded: false,
    }
  },
  methods: {
    iframeLoad() {
      this.iframeIsLoaded = true
    },
  },
}
</script>
