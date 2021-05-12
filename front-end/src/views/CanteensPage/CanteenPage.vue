<template>
  <div id="canteen-dashboard">
    <div id="canteen-infos">
      <div class="context">
        <h2>{{ canteen.title }}</h2>
        <div>
          <i class="far fa-compass" aria-hidden="true" title="Région"></i>
          <span class="sr-only">Région :</span>
          {{ canteen.region }}
        </div>
        <div>
          <i class="fas fa-utensils" aria-hidden="true"></i>
          {{canteen.mealCount}} repas par jour
        </div>
      </div>
      <div class="key-points">
        <h3>Nos initiatives mises en place&nbsp;:</h3>
        <ul>
          <li v-for="keyPoint in canteen.keyPoints" :key="keyPoint" class="key-point">
            {{ keyPoint }}
          </li>
        </ul>
      </div>
    </div>

    <CanteenDashboard :diagnostics="canteen.diagnostics"/>
  </div>
</template>

<script>
  import { getCanteenById } from '@/data/Canteens.js';
  import CanteenDashboard from '@/components/CanteenDashboard';

  export default {
    components: {
      CanteenDashboard
    },
    props: {
      id: String,
    },
    data() {
      return {
        canteen: getCanteenById(this.id),
      };
    },
    created() {
      document.title = `${this.canteen.title} - ma-cantine.beta.gouv.fr`;
    }
  }
</script>

<style scoped lang="scss">
  #canteen-dashboard {
    padding: 1em 0.5em;
    max-width: 1170px;
    margin: auto;
  }

  #canteen-infos {
    padding: 30px;
    border: 1px solid $orange;
    border-radius: 20px;
    text-align: left;
    display: flex;

    .context {
      display: flex;
      flex-direction: column;
      flex: 1;

      div {
        margin: 0.5em 0;
      }
    }

    h2 {
      font-weight: bold;
      font-size: 36px;
      color: $green;
      margin: 0;
      margin-bottom: 10px;
    }

    .key-points {
      flex: 1;
    }

    .key-point {
      margin: 0.5em 0;
    }
  }

  @media (max-width: 750px) {
    #canteen-infos {
      flex-direction: column;
    }
  }
</style>
