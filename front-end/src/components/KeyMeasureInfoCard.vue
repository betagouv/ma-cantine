<template>
  <div class="measure-card">
    <div class="measure-info-card">
      <div class="deadline">
        <h4><i class="far fa-calendar-alt"></i> Entrée en vigueur</h4>
        <p>{{ measure.deadline.display }}</p>
      </div>
      <div class="tags">
        <h4><i class="fas fa-chart-pie"></i> Pour qui ?</h4>
        <p v-if="measure.who">{{measure.who}}</p>
        <p class="tag" :class="tag" v-for="tag in measure.tags" :key="tag">
          {{ tagsInfo[tag] }}
        </p>
      </div>
    </div>
    <div class="calculator-card" v-if="includeCalculatorCard">
      <h4><i class="fas fa-hand-point-right"></i> Vérifier où en suis-je de mes appros ?</h4>
      <p>Utilisez notre simulateur pour calculer votre répartition de produits durables et bio.</p>
      <CalculatorLink message="Vérifier mes achats" class="simulator-link"/>
    </div>
  </div>
</template>

<style scoped lang="scss">
  .measure-card {
    max-width: 274px;
    flex: 1.2;
    margin-right: 2em;
  }

  .measure-info-card, .calculator-card {
    background: $light-green;
    border-radius: 15px;
    padding: 1em 1.5em;
  }

  h4 {
    margin-top: 0.5em;
    font-weight: bold;
    font-size: 18px;
    margin-bottom: 1em;
    color: $grey;
  }

  .deadline > h2, .tags > h2 {
    white-space: nowrap;
  }

  p {
    font-size: 14px;
    color: $black;
  }

  .tag {
    font-size: 14px;
    font-weight: bold;
    margin: 0.5em 0em;
    color: $green;
  }

  .calculator-card {
    margin-top: 4em;
  }

  .simulator-link {
    font-size: 18px;
    text-align: center;
    color: $dark-white;
    font-weight: bold;
    text-decoration: none;
    white-space: nowrap;
    background: $green;
    border-radius: 50px;
    padding: 0.5em 0.8em;
    line-height: 3.5em;
  }

  .fa-calendar-alt, .fa-chart-pie, .fa-hand-point-right {
    color: $grey;
  }

  @media (max-width: 800px) {
    h4 {
      font-size: 16px;
    }

    .simulator-link {
      font-size: 14px;
    }
  }

  @media (max-width: 480px) {
    .measure-info-card {
      margin-right: 0em;
    }

    .simulator-link {
      font-size: 18px;
    }

    .calculator-card {
      margin-top: 1em;
    }
  }
</style>

<script>
  import tags from "@/data/sector-tags.json";
  import CalculatorLink from '@/components/CalculatorLink';

  export default {
    name: "KeyMeasureInfoCard",
    components: {
      CalculatorLink
    },
    props: {
      measure: Object,
      includeCalculatorCard: Boolean
    },
    data() {
      return {
        tagsInfo: tags,
      }
    },
  };
</script>
