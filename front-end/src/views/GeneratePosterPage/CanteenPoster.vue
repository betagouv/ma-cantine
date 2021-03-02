<template>
  <div class="poster-contents">
    <div id="heading">
      <img src="@/assets/toque.svg" id="hat" alt="">
      <div>
        <h1>Cantine {{ school || "_________" }}</h1>
        <p id="commune">{{ commune || "_________" }}</p>
        <p>Nous servons {{ servingsNumber || "___" }} repas par jour</p>
        <p>Dans la cantine de votre enfant, sur l'année de 2020, nous avons servi en valeur d'achats:</p>
      </div>
    </div>
    <p class="percentage"><span id="bio-percent" class="number">{{ bioPercent }} %</span> de produits bio</p>
    <p class="percentage"><span id="quality-percent" class="number">{{ qualityPercent }} %</span> de produits de qualité et durables (hors bio)</p>
    <p class="percentage" v-if="equitableNumber"><span id="equitable-percent" class="number">{{ equitablePercent }} %</span> produits issus du commerce équitable</p>
    <div id="about">
      <h2>Pourquoi je vois cette affiche ?</h2>
      <p>
        À partir du 1er janvier 2020, les usagers des restaurants collectifs devront être informés une fois par an,
        par voie d’affichage et de communication électronique, de la part des produits de qualité et durables entrant dans la composition des repas servis
        et des démarches entreprises pour développer des produits issus du commerce équitable.
      </p>
      <p>
        <b>Un bon moyen de savoir ce qu'il y a dans votre assiette et d'en discuter avec le personnel de votre restaurant !</b>
      </p>
    </div>
    <p><b>En savoir plus de la loi EGAlim:</b> <a href="https://ma-cantine.beta.gouv.fr">https://ma-cantine.beta.gouv.fr</a></p>
    <img src="@/assets/qr-code.svg" id="qr" alt="QR code vers https://ma-cantine.beta.gouv.fr">
  </div>
</template>

<script>
  export default {
    props: {
      school: String,
      commune: String,
      servingsNumber: Number,
      totalNumber: Number,
      bioNumber: Number,
      qualityNumber: Number,
      equitableNumber: Number
    },
    computed: {
      bioPercent() {
        return this.percentageString(this.bioNumber);
      },
      qualityPercent() {
        return this.percentageString(this.qualityNumber);
      },
      equitablePercent() {
        return this.percentageString(this.equitableNumber);
      }
    },
    methods: {
      percentageString(number) {
        if(!isNaN(number) && this.totalNumber) {
          const value = Math.floor(number / this.totalNumber * 1000) / 10;
          return value.toLocaleString("fr-FR");
        }
        return "__";
      }
    }
  }
</script>

<style scoped lang="scss">
  .poster-contents {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: calc(296mm - 40mm);
    padding: 20mm;
    // Need to repeat some styling directly here for PDF generation
    font-family: "Marianne";
    align-items: center;
  }

  #heading {
    display: flex;
    align-items: center;

    div {
      text-align: left;
    }

    h1 {
      font-size: 35px;
    }

    #commune {
      font-size: 25px;
      margin-top: -0.7em;
    }
  }

  #hat {
    width: 200px;
    margin-right: 1em;
  }

  p.percentage {
    display: flex;
    align-items: center;
    margin-top: 0;
  }

  #bio-percent {
    color: $green;
  }

  #quality-percent {
    color: $orange;
  }

  .number {
    font-size: 50px;
    font-weight: bold;
    margin-right: 6px;
  }

  #about {
    width: 100%;
    margin: 0.5em 0;
    padding: 0.5em 2em;
    background: $light-orange;
    border-radius: 43px;
    text-align: left;

    h2 {
      font-size: 18px;
    }

    p {
      font-size: 14px;
    }
  }

  a {
    color: $grey;
    text-decoration: none;
  }

  #qr {
    margin: 0.5em;
    width: 30mm;
    height: 30mmm; 
  }
</style>