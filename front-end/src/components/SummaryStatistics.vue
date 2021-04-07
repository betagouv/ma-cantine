<template>
  <ul class="statistics">
    <li class="statistic">
      <div class="vertically-align-header">
        <h3>Produits bio :</h3>
      </div>
      <p class="number bio">{{ statistics.bio }} %</p>
    </li>

    <li class="statistic">
      <div class="vertically-align-header">
        <h3>Produits de qualité et durables :</h3>
      </div>
      <p class="number sustainable">{{ statistics.sustainable }} %</p>
    </li>

    <li class="statistic">
      <div class="vertically-align-header">
        <h3>Produits issus du commerce équitable :</h3>
      </div>
      <p class="number">{{ statistics.fairTrade }} %</p>
    </li>
  </ul>
</template>

<script>
  export default {
    props: {
      statistics: Object,
    }
  }
</script>

<style scoped lang="scss">
  .statistics {
    display: flex;
    justify-content: space-between;
  }

  .statistic {
    width: 30%;
    text-align: center;
  }

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

  .number {
    font-size: 2.5em;
    margin-top: 0.2em;
  }

  .bio {
    color: $green;
  }

  .sustainable {
    color: $orange;
  }

  @media (max-width: 850px) {
    .number {
      margin: 0;
      margin-bottom: 0.7em;
      font-size: 2em;
    }
  }
</style>
