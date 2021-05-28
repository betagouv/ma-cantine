<template>
  <BaseModal @closeModal="$emit('closeModal')">
    <h2 id="modal-title" tabindex="-1">Vidéo d'introduction</h2>

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
        <i class="fas fa-spinner fa-spin"></i>
        Chargement de la vidéo de présentation
      </div>
    </div>

    <a
      class="calculator-download"
      href="/Diagnostic approvisionnement (ma-cantine-alpha) v0.4.ods"
      download
      @click="$emit('closeModal')"
    >
      Télécharger
    </a>
  </BaseModal>
</template>

<script>
import BaseModal from "@/components/BaseModal"

export default {
  components: {
    BaseModal,
  },
  props: ["closeModal"],
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

<style scoped lang="scss">
h2 {
  text-align: center;
}

.calculator-i-frame {
  position: relative;
  width: 100%;
  padding-top: 70%;

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
