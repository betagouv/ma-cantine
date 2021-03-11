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
      <div class="location"></div>
      <div class="summary">
        <h2>{{ canteen.title }}</h2>
        <ul class="statistics">
          <li v-for="(statistic, key) in canteen.statistics" :key="key" class="statistic">
            <div class="vertically-align-header">
              <h3>{{ statisticTitle(key) }}</h3>
            </div>
            <p class="number">{{ statistic }} %</p>
          </li>
        </ul>
        <p class="meal-count">
          <i class="fas fa-utensils"></i> {{ canteen.mealCount }} repas par jour
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

  export default {
    data() {
      return {
        keyMeasures,
        canteens
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
        return keyMeasures.find((measure) => {
          return measure.subMeasures.find((subMeasure) => subMeasure.id === id);
        });
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
    padding: 1em 2em;

    .location {
      height: 10em;
      width: 10em;
      background-color: $orange;
      margin-right: 1em;
    }

    h2 {
      margin-bottom: 0;
      font-size: 2em;
      text-transform: uppercase;
    }

    .meal-count {
      margin-top: 0;
      color: $grey;
    }
  }

  .summary {
    padding: 1em;
  }

  .statistics {
    display: flex;
    justify-content: space-between;
  }

  .statistic {
    min-width: 30%;
    text-align: center;

    .vertically-align-header {
      height: 5em;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    h3 {
      font-size: 1em;
    }

    .number {
      font-size: 2.5em;
      margin-top: 0.2em;
    }
  }

  .completed-measures {
    border-left: 5px solid $dark-white;
    padding: 1em;
    padding-top: 0;
    width: 40%;
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

    .completed-measures {
      width: unset;
      border: none;
    }
  }

  @media (max-width: 920px) {
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
    }

    .meal-count {
      text-align: center;
      margin-bottom: 0;
    }
  }

  @media (max-width: 600px) {
    #welcome-block, #canteens-block {
      font-size: 12px;
    }

    #canteens-block {
      padding: 0.5em;
    }

    .canteen-card {
      width: 95%;
    }
  }
</style>