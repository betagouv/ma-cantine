<template>
  <div>
    <div class="resource calculator" @click="showCalculatorModal">
      <div class="resource-icon"><i class="fas fa-calculator"></i></div>
      <p class="resource-prompt">
        Si vous avez besoin d'aide pour calculer votre part de bios et de produits labélisés,
        vous pouvez tester notre calculateur sous format excel.
      </p>
      <div class="resource-icon"><i class="fas fa-file-download"></i></div>
    </div>
    <BaseModal v-if="calculatorModal" @closeModal="closeCalculatorModal">
      <h2 id="modal-title" tabindex="-1">Vidéo d'introduction</h2>

      <div class="calculator-i-frame">
        <iframe
          src="https://www.loom.com/embed/c1cb4020b3f44b24adec8367861ebc0d"
          frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen
          @load="iframeLoad"
          v-show="iframeIsLoaded"
          class="calculator-video"
          title="Vidéo de présentation du calculateur"
        />

        <div class="video-loader" v-show="!iframeIsLoaded">
          <i class="fas fa-spinner fa-spin"></i> Chargement de la vidéo de présentation
        </div>
      </div>

      <a
        class="calculator-download"
        href="/Diagnostic approvisionnement (ma-cantine-alpha) v0.4.ods"
        download
        @click="closeCalculatorModal"
      >
        Télécharger
      </a>
    </BaseModal>
    <a href="https://www.inao.gouv.fr/Espace-professionnel-et-outils/Rechercher-un-produit" class="resource" target="_blank">
      <div class="resource-icon"><i class="fas fa-seedling"></i></div>
      <p class="resource-prompt">
        Trouver des catégories de produits en recherchant par labels, siqo et/ou régions
        avec le moteur de recherche de l'INAO.
      </p>
      <div class="resource-icon"><i class="fas fa-external-link-alt"></i></div>
    </a>
    <a href="/Guide Pratique MP Gestion directe.pdf" class="resource" download>
      <div class="resource-icon"><i class="fas fa-archive"></i></div>
      <p class="resource-prompt">
        Télécharger le guide pratique de rédaction des marchés publics pour des appros
        durables à destination des acteurs de la restauration collective en gestion directe.
      </p>
      <div class="resource-icon"><i class="fas fa-file-download"></i></div>
    </a>
  </div>
</template>

<script>
  import BaseModal from '@/components/BaseModal';

  export default {
    components: {
      BaseModal
    },
    data() {
      return {
        calculatorModal: false,
        iframeIsLoaded: false,
      };
    },
    methods: {
      showCalculatorModal() {
        this.calculatorModal = true;
      },
      closeCalculatorModal() {
        this.calculatorModal = false;
      },
      iframeLoad() {
        this.iframeIsLoaded = true;
      }
    }
  }
</script>

<style scoped lang="scss">
  .resource.calculator {
    background: $light-blue;
    border-color: $blue;
    cursor: pointer;

    .fa-calculator {
      color: $blue;
    }

    .fa-file-download {
      color: $blue;
    }

    .resource-prompt {
      color: $blue;
    }
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
    color: $white;
    font-size: 24px;
    background-color: $orange;
    text-decoration: none;
  }
</style>
