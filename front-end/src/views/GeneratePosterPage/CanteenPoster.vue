<template>
  <div id="canteen-poster">
    <div id="poster-contents">
      <h1>Cantine du {{ school || "___________" }}</h1>
      <h2>Nous servons {{ servingsNumber || "___" }} enfants par jour</h2>
      <p>Dans la cantine de votre enfant, sur l'année de 2020, nous avons servi en valeur d'achats:</p>
      <p><span id="bio-percent">{{ bioPercent || "__" }} %</span> de produits bio</p>
      <p><span id="quality-percent">{{ qualityPercent || "__" }} %</span> de produits de qualité et durables (sauf bio)</p>
      <p><span id="equitable-percent">{{ equitablePercent || "__" }} %</span> du commerce équitable</p>
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
        return this.calculatePercent(this.bioNumber);
      },
      qualityPercent() {
        return this.calculatePercent(this.qualityNumber);
      },
      equitablePercent() {
        return this.calculatePercent(this.equitableNumber);
      }
    },
    methods: {
      calculatePercent(number) {
        if(number && this.totalNumber) {
          return Math.floor(number / this.totalNumber * 1000) / 10;
        }
        return 0;
      }
    }
  }
</script>

<style scoped lang="scss">
  #canteen-poster {
    width: 210mm;
    min-width: 210mm;
    height: 297mm;
    min-height: 297mm;
    margin-left: 2em;
    border: 1px solid $grey;
  }

  #poster-contents {
    // border: 2px solid $light-grey;
    background-color: $white;
    // margin: 3mm;
    height: 290mm;
    display: flex;
    flex-direction: column;

    h1 {
      color: $orange;
    }
  }
</style>