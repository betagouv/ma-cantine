<template>
  <div id="welcome-block">
    <h1>
      Découvrez les initiatives prises pour par nos cantines
      pour une alimentation plus durable
    </h1>
    <img src="@/assets/desktop.svg" alt="">
  </div>
  <ul id="canteens-block">
    <li v-for="canteen in canteens" :key="canteen.title" class="canteen-card">
      <a class="location" :title="map[canteen.region].title" :href="map[canteen.region].href">
        <img :alt="map[canteen.region].alt" :src="map[canteen.region].src">
        <p class="attribution">{{ map[canteen.region].attribution }}</p>
      </a>
      <div class="summary">
        <h2>{{ canteen.title }}</h2>
        <ul class="statistics">
          <li v-for="(statistic, key) in canteen.statistics" :key="key" class="statistic">
            <div class="vertically-align-header">
              <h3>{{ statisticTitle(key) }}</h3>
            </div>
            <p class="number">{{ statistic }}&nbsp;%</p>
          </li>
        </ul>
        <p class="meal-count">
          <i class="fas fa-utensils"></i>&nbsp;
          {{ canteen.mealCount }} repas par jour
        </p>
      </div>
      <div class="completed-measures">
        <h3>Notre sous-mesures faits :</h3>
        <ul>
          <li v-for="measureId in canteen.completedMeasures" :key="measureId">
            {{ findSubMeasure(measureId).title }}
          </li>
        </ul>
      </div>
    </li>
  </ul>
</template>

<script>
  import { keyMeasures } from "@/data/KeyMeasures.js";
  import canteens from "@/data/canteens.json";

  const map = {
    "nouvelle-acquitaine": {
      href: "https://commons.wikimedia.org/wiki/File:Nouvelle-Aquitaine_in_France_2016.svg",
      src: "https://upload.wikimedia.org/wikipedia/commons/1/1e/Nouvelle-Aquitaine_in_France_2016.svg",
      title: "Nouvelle-Aquitaine",
      alt: "Nouvelle-Aquitaine",
      attribution: "TUBS, CC BY-SA 3.0 DE, via Wikimedia Commons"
    },
    "normandy": {
      href: "https://commons.wikimedia.org/wiki/File:Normandy_in_France_2016.svg",
      src: "https://upload.wikimedia.org/wikipedia/commons/1/17/Normandy_in_France_2016.svg",
      title: "Normandie",
      alt: "Normandie",
      attribution: "TUBS, CC BY-SA 3.0 DE, via Wikimedia Commons"
    }
  };

  export default {
    data() {
      return {
        keyMeasures,
        canteens,
        map
      }
    },
    methods: {
      statisticTitle(key) {
        return {
          bio: "Produits bio",
          quality: "Produits durables",
          equitable: "Produits issus du commerce équitable"
        }[key];
      },
      findSubMeasure(id) {
        for (let measureIdx = 0; measureIdx < keyMeasures.length; measureIdx++) {
          const measure = keyMeasures[measureIdx];
          const subMeasure = measure.subMeasures.find((subMeasure) => subMeasure.id === id);
          if(subMeasure) { return subMeasure; }
        }
      }
    }
  }
</script>

<style scoped lang="scss">
  #welcome-block {
    display: flex;
    justify-content: space-between;
    padding: 3em;
    padding-bottom: 0;
    text-align: left;

    img {
      height: 20em;
      margin-left: 1em;
    }
  }

  #canteens-block {
    background-color: $light-yellow;
    padding: 3em;
    margin-top: 0;
    text-align: left;
    font-size: 14px;
  }

  .canteen-card {
    background-color: $white;
    border-radius: 2em;
    /* offset-x | offset-y | blur-radius | spread-radius | color */
    box-shadow: 0px 0px 4px 0.5px $orange;
    margin: 2em auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 2em;

    .location {
      position: relative;

      img {
        max-height: 17vw;
      }

      .attribution {
        font-size: 0.6em;
        color: $grey;
        position: absolute;
        bottom: -0.7em;
        padding: 0.4em;
        background-color: $white;
      }
    }

    h2 {
      margin: 0;
      font-size: 2em;
      text-transform: uppercase;
    }

    .meal-count {
      margin-top: 0;
      color: $grey;
    }
  }

  .summary {
    margin: 2em;
    border-right: 5px solid $dark-white;
    padding-right: 2em;
  }

  .statistics {
    display: flex;
    justify-content: space-between;
  }

  .statistic {
    width: 30%;
    text-align: center;

    .vertically-align-header {
      height: 5em;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    h3 {
      font-size: 1em;
      font-weight: normal;
    }
  }

  .number {
    font-size: 2.5em;
    margin-top: 0.2em;
  }

  .completed-measures {
    padding: 2em 1em 3em 1em;
    width: 40%;
    align-self: flex-start;
  }

  @media (max-width: 1000px) {
    #welcome-block {
      margin-bottom: 3em;
      text-align: center;

      img {
        display: none;
      }
    }

    .canteen-card {
      flex-wrap: wrap;
      justify-content: left;
    }

    .summary {
      border: none;
      padding-right: 0;
      margin: 0.3em;
    }

    .completed-measures {
      width: unset;
      padding-top: 0;
    }
  }

  @media (max-width: 850px) {
    #canteens-block {
      h2 {
        text-align: center;
        margin-bottom: 0.3em;
      }
    }

    .canteen-card {
      padding: 0.5em;
      justify-content: center;
    }

    .location {
      display: none;
    }

    .number {
      margin: 0;
      margin-bottom: 0.7em;
      font-size: 2em;
    }

    .meal-count {
      text-align: center;
      margin-bottom: 0;
    }
  }

  @media (max-width: 600px) {
    #canteens-block {
      padding: 0.5em;
    }

    .canteen-card {
      width: 95%;
    }
  }
</style>