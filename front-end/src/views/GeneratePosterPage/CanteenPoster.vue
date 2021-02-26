<template>
  <div id="canteen-poster">
    <div id="poster-contents">
      <div id="heading">
        <img src="@/assets/toque.svg" id="hat" alt="">
        <div>
          <h1>Cantine du {{ school || "_________" }}</h1>
          <p>Nous servons {{ servingsNumber || "___" }} enfants par jour</p>
          <p>Dans la cantine de votre enfant, sur l'année de 2020, nous avons servi en valeur d'achats:</p>
        </div>
      </div>
      <p class="percentage"><span id="bio-percent" class="number">{{ bioPercent }} %</span> de produits bio</p>
      <p class="percentage"><span id="quality-percent" class="number">{{ qualityPercent }} %</span> de produits de qualité et durables (sauf bio)</p>
      <p class="percentage"><span id="equitable-percent" class="number">{{ equitablePercent }} %</span> produits issus commerce équitable</p>
      <div id="about">
        <h2>Rappel de la loi</h2>
        <p>
          Une fois par an, les convives sont informés sur la part des produits de qualité et durables des repas servis et des démarches 
          entreprises pour l’acquisition de produits issus du commerce équitable. Cette information peut se faire par affichage 
          (dans l’espace commun par exemple) ou par email.
        </p>
      </div>
      <p><b>En savoir plus de la loi EGAlim:</b> <a href="https://ma-cantine.beta.gouv.fr">https://ma-cantine.beta.gouv.fr</a></p>
      <img src="@/assets/qr-code.svg" id="qr" alt="QR code vers https://ma-cantine.beta.gouv.fr">
    </div>
  </div>
</template>

<script>
  export default {
    props: {
      school: String,
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
  #canteen-poster {
    width: 210mm;
    min-width: 210mm;
    height: 296mm;
    min-height: 296mm;
    margin-left: 2em;
    border: 1px solid $grey;
  }

  #poster-contents {
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
  }

  #hat {
    width: 200px;
    margin-right: 1em;
  }

  p.percentage {
    display: flex;
    align-items: center;
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