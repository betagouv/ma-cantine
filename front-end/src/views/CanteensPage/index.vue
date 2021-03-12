<template>
  <div id="welcome-block">
    <h1>
      Découvrez les initiatives prises par nos cantines
      pour une alimentation plus durable
    </h1>
    <img src="@/assets/desktop.svg" alt="">
  </div>
  <ul id="canteens-block">
    <li v-for="canteen in canteens" :key="canteen.title" class="canteen-card">
      <div class="location" :title="map[canteen.region].title">
        <img :alt="map[canteen.region].title" :src="map[canteen.region].src">
        <p class="attribution">
          TUBS, <a href="https://creativecommons.org/licenses/by-sa/3.0/de/deed.en">CC BY-SA 3.0 DE</a>, via Wikimedia Commons
        </p>
      </div>
      <div class="summary">
        <h2>{{ canteen.title }}</h2>
        <ul class="statistics">
          <SummaryStatistic title="Produits bio" :value="canteen.statistics.bio" class="bio"/>
          <SummaryStatistic title="Produits durables" :value="canteen.statistics.sustainable" class="sustainable"/>
          <SummaryStatistic title="Produits issus du commerce équitable" :value="canteen.statistics.fairTrade"/>
        </ul>
        <p class="meal-count">
          <i class="fas fa-utensils"></i>&nbsp;
          {{ canteen.mealCount }} repas par jour
        </p>
      </div>
      <div class="completed-measures">
        <h3>Nos mesures mises en place :</h3>
        <ul>
          <li v-for="measureId in canteen.completedMeasures.slice(0, 3)" :key="measureId">
            {{ findSubMeasure(measureId).title }}
          </li>
        </ul>
      </div>
    </li>
  </ul>
</template>

<script>
  import { keyMeasures, findSubMeasure } from "@/data/KeyMeasures.js";
  import canteens from "@/data/canteens.json";
  import SummaryStatistic from './SummaryStatistic';

  const map = {
    "nouvelle-acquitaine": {
      src: "https://upload.wikimedia.org/wikipedia/commons/1/1e/Nouvelle-Aquitaine_in_France_2016.svg",
      title: "Nouvelle-Aquitaine"
    },
    "normandy": {
      src: "https://upload.wikimedia.org/wikipedia/commons/1/17/Normandy_in_France_2016.svg",
      title: "Normandie"
    }
  };

  export default {
    components: {
      SummaryStatistic
    },
    data() {
      return {
        keyMeasures,
        canteens,
        map
      }
    },
    methods: {
      findSubMeasure
    }
  }
</script>

<style scoped lang="scss">
  #welcome-block {
    display: flex;
    justify-content: center;
    padding: 3em;
    padding-bottom: 0;
    text-align: left;

    h1 {
      max-width: 730px;
    }

    img {
      height: 20em;
      padding-left: 3em;
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
    max-width: 1170px;

    .location {
      position: relative;

      img {
        height: 17vw;
        max-height: 17em;
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
      font-size: 1.1em;
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

  .completed-measures {
    padding: 2em 1em 3em 1em;
    width: 40%;
    align-self: flex-start;

    ul {
      padding-top: 1em;
    }

    li {
      padding-bottom: 2em;
    }
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