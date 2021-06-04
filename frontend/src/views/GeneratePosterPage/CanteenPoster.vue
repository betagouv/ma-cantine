<template>
  <div class="poster-contents">
    <div id="heading">
      <img src="/static/images/toque.svg" id="hat" alt="" />
      <div>
        <h1>Cantine {{ canteen.name || "_________" }}</h1>
        <p id="commune">{{ canteen.city || "_________" }}</p>
        <p>Nous servons {{ canteen.dailyMealCount || "___" }} repas par jour</p>
        <p>Dans la cantine de votre enfant, sur l'année de 2020, nous déclarons avoir servi en valeur d'achats:</p>
      </div>
    </div>
    <SummaryStatistics :qualityDiagnostic="diagnostic" />
    <LogoList id="logos" />
    <div id="about">
      <h2>Pourquoi je vois cette affiche ?</h2>
      <p>
        Depuis le 1er janvier 2020, les gestionnaires de restaurant collectif doivent informer les convives une fois par
        an de la part des produits de qualité et durables entrant dans la composition des repas servis ainsi des
        démarches entreprises pour développer des produits issus du commerce équitable. Ces informations sont fonction
        de la valeur totale des achats réalisés sur l'année.
      </p>
      <p>
        <b>
          Un bon moyen de savoir ce qu'il y a dans votre assiette et d'en discuter avec le personnel de votre restaurant
          !
        </b>
      </p>
    </div>
    <div id="more-information">
      <p class="url">
        <span>En savoir plus de la loi EGAlim :</span>
        <a href="https://ma-cantine.beta.gouv.fr">https://ma-cantine.beta.gouv.fr</a>
      </p>
      <img src="/static/images/qr-code.svg" id="qr" alt="QR code vers https://ma-cantine.beta.gouv.fr" />
    </div>
  </div>
</template>

<script>
import LogoList from "@/components/LogoList"
import SummaryStatistics from "@/components/SummaryStatistics"

export default {
  components: {
    LogoList,
    SummaryStatistics,
  },
  props: {
    canteen: Object,
    diagnostic: Object,
  },
  computed: {
    bioPercent() {
      return this.percentageString(this.diagnostic.valueBio)
    },
    sustainablePercent() {
      return this.percentageString(this.diagnostic.valueSustainable)
    },
    fairTradePercent() {
      return this.percentageString(this.diagnostic.valueFairTrade)
    },
  },
  methods: {
    percentageString(number) {
      if (!isNaN(number) && this.diagnostic.valueTotal) {
        const value = Math.floor((number / this.diagnostic.valueTotal) * 1000) / 10
        return value.toLocaleString("fr-FR")
      }
      return "__"
    },
  },
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
  color: $ma-cantine-green;
}

#sustainable-percent {
  color: $ma-cantine-orange;
}

.number {
  font-size: 50px;
  font-weight: bold;
  margin-right: 6px;
}

#logos {
  width: 100%;
}

#about {
  width: 100%;
  margin: 0.5em 0;
  padding: 0.5em 2em;
  background: $ma-cantine-light-orange;
  border-radius: 43px;
  text-align: left;

  h2 {
    font-size: 18px;
  }

  p {
    font-size: 14px;
  }
}

#more-information {
  width: 100%;
  display: flex;
  justify-content: space-around;
  max-height: 30mm;

  .url {
    display: flex;
    flex-direction: column;
    justify-content: space-around;

    span {
      font-weight: bold;
    }

    a {
      color: $ma-cantine-grey;
      text-decoration: none;
    }
  }

  #qr {
    margin: 0.5em;
    width: 30mm;
    height: 30mmm;
  }
}
</style>
