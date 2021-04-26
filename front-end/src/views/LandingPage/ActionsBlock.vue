<template>
  <div>
    <div id="actions">
      <router-link class="action" :to="{ name: 'GeneratePosterPage' }">
        <h2>
          Vous connaissez déjà la part de bio, durable et produits issus
          du commerce équitable de votre cantine scolaire&nbsp;?
        </h2>
        <p>
          Vous pouvez générer une affiche à poser dans votre cantine ainsi qu’un email-type à destination
          des convives et parents d'élèves.
        </p>
        <img src="@/assets/inform-action.svg" alt="">
        <p class="call-to-action">
          J’informe mes convives &nbsp;<i class="fas fa-arrow-circle-right"></i>
        </p>
      </router-link>
      <div class="divider"></div>
      <div class="action" @click="showCalculatorModal">
        <h2>
          Vous avez besoin d’aide pour le calcul&nbsp;?
        </h2>
        <p>
          Si vous ne connaissez pas votre part de bio, produits durables, produits issues du commerce équitable,
          nous vous proposons un outil simple pour les calculer. Sous forme de tableur, remplissez vos achats HT
          suivant leurs labels et/ou sigles de qualité.
        </p>
        <img src="@/assets/calculator-action.svg" alt="">
        <p class="call-to-action">
          Télécharger notre tableur &nbsp;<i class="fas fa-arrow-circle-down"></i>
        </p>
      </div>
    </div>

    <CalculatorResourceModal v-if="calculatorModal" @closeModal="closeCalculatorModal"/>
  </div>
</template>

<script>
  import CalculatorResourceModal from '@/components/KeyMeasureResource/CalculatorResourceModal';

  export default {
    components: {
      CalculatorResourceModal
    },
    data() {
      return {
        calculatorModal: false,
      };
    },
    methods: {
      showCalculatorModal() {
        this.calculatorModal = true;
      },
      closeCalculatorModal() {
        this.calculatorModal = false;
      },
    }
  }
</script>

<style scoped lang="scss">
  #actions {
    display: flex;
    justify-content: center;
    align-items: stretch;
    margin: 2em;
  }

  .action {
    width: 40vw;
    max-width: 50em;
    padding: 2em;
    cursor: pointer;
    text-decoration: none;
    color: $black;
    text-align: left;
    border-bottom: 15px solid $white;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-between;

    h2 {
      font-size: 1.4em;
    }

    p {
      color: $grey;
    }

    img {
      max-width: 20em;
    }

    .call-to-action {
      width: 100%;
      text-align: right;
      color: $orange;
      font-weight: bold;
      font-size: 1.2em;
    }
  }

  .action:hover {
    border-bottom-color: $orange;
  }

  .divider {
    height: 30em;
    background-color: $dark-white;
    width: 8px;
    align-self: center;
  }

  @media (max-width: 750px) {
    #actions {
      margin: 2em 0;
      flex-wrap: wrap;
    }

    .action {
      width: 100%;
      padding: 1em;
    }

    .divider {
      display: none;
    }
  }
</style>
