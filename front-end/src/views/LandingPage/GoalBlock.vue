<template>
  <div id="goal">
    <h3>Les enjeux de la restauration collective</h3>
    <div class="goal-information">
      La restauration collective représente près de <b>4 milliards de repas servis par an</b> dans plus de 70 000 sites de restauration, des cantines scolaires, des hopitaux, des EPHAD, des entreprises, des administrations...  Agir sur la composition des assiettes est un levier fort pour améliorer l'impact sur notre santé et sur l'environnement tout en influançant positivement les filières d'agriculture biologique et de qualité. Les mesures en faveur d'une alimentation plus durable peuvent contribuer à modifier les comportements alimentaires notamment chez les plus jeunes.
    </div>
    <div class="presentation-i-frame" v-show="iframeIsLoaded">
      <iframe
        src="https://www.youtube-nocookie.com/embed/kkQ3ttLFiD8"
        title="Vidéo présentation d'Egalim"
        @load="iframeLoad"
        class="presentation-video"
        frameborder="0"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowfullscreen
      />
    </div>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        iframeIsLoaded: false,
      };
    },
    methods: {
      iframeLoad() {
        this.iframeIsLoaded = true;
      }
    }
  }
</script>

<style scoped lang="scss">
  #goal {
    margin: 70px auto;
    max-width: 851px;
  }

  h3 {
    font-weight: bold;
    font-size: 37px;
    line-height: 52px;
    color: $green;
  }

  .goal-information {
    padding: 24px;
    border-radius: 20px;
    margin: auto;
    text-align: left;
    color: $green;
    background-color: $light-green;
    font-size: 20px;
  }

  .presentation-i-frame {
    position: relative;
    width: 90%;
    padding-top: 63%;
    margin: 50px auto;

    .presentation-video {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
    }
  }
</style>
