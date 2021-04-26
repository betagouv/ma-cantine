<template>
  <div class="measure-info-card">
    <div class="deadline">
      <h3><i class="far fa-calendar-alt"></i> Entrée en vigueur</h3>
      <p>{{ measure.deadline.display }}</p>
    </div>
    <div class="for-who">
      <h3><i class="fas fa-chart-pie"></i> Pour qui ?</h3>
      <p v-if="measure.who">{{measure.who}}</p>
      <div class="sectors">
        <p class="sector" :class="sector" v-for="sector in measure.sectors" :key="sector">
          {{ sectors[sector] }}
        </p>
      </div>
    </div>
  </div>
</template>

<script>
  import sectors from "@/data/sectors.json";

  export default {
    name: "KeyMeasureInfoCard",
    props: {
      measure: Object,
    },
    data() {
      return {
        sectors,
      }
    },
  };
</script>

<style scoped lang="scss">
  .measure-info-card {
    background: $light-green;
    border-radius: 15px;
    margin-right: 2em;
    padding: 1em 1.5em;
    width: 12em;
    flex-shrink: 0;
  }

  h3 {
    margin-top: 0.5em;
    font-weight: bold;
    font-size: 18px;
    margin-bottom: 1em;
    color: $grey;
  }

  .deadline > h2, .for-who > h2 {
    white-space: nowrap;
  }

  p {
    font-size: 14px;
    color: $black;
  }

  .sector {
    font-size: 14px;
    font-weight: bold;
    margin: 0.5em 0em;
    color: $green;
  }

  .fa-calendar-alt, .fa-chart-pie {
    color: $grey;
  }

  @media (max-width: 800px) {
    h3 {
      font-size: 16px;
    }
  }

  @media (max-width: 650px) {
    .measure-info-card {
      width: 70%;
    }

    .sectors {
      column-count: 2;
    }
  }
</style>
