<template>
  <div id="canteen-dashboard">
    <div id="canteen-infos">
      <div class="context">
        <h2>{{ canteen.title }}</h2>
        <div><i class="far fa-compass"></i> {{ canteen.region }}</div>
        <div><i class="fas fa-utensils"></i> {{canteen.mealCount}} repas par jour</div>
      </div>
      <div class="key-points">
        <h3>Nos mesures mises en place&nbsp;:</h3>
        <ul>
          <li v-for="keyPoint in canteen.keyPoints" :key="keyPoint">
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
      justify-content: space-between;
      flex: 1;
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
  }

  @media (max-width: 750px) {
    #canteen-infos {
      flex-direction: column;
    }
  }
</style>
