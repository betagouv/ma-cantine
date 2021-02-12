<template>
  <div class="description-container">
    <p class="description" v-if="measure.htmlDescription" v-html="measure.htmlDescription"></p>
    <p class="description" v-else-if="measure.description">{{measure.description}}</p>
    <div id="logos" v-if="measure.id === 'cinquante'" :class="{ shrink: shrinkLogos }">
      <img src="@/assets/logos/label-rouge.png" alt="logo Label Rouge"/>
      <img src="@/assets/logos/Logo-AOC-AOP.png" alt="logo appellation d’origine"/>
      <img src="@/assets/logos/IGP.png" alt="logo indication géographique"/>
      <img src="@/assets/logos/STG.png" alt="logo Spécialité traditionnelle garantie"/>
      <img src="@/assets/logos/hve.png" alt="logo Haute Valeur Environnementale"/>
      <img src="@/assets/logos/logo_label-peche-durable.png" alt="logo écolabel pêche durable"/>
      <img src="@/assets/logos/rup.png" alt="logo Région Ultrapériphérique"/>
      <img src="@/assets/logos/logo_bio_eurofeuille.png" alt="logo Agriculture Biologique"/>
    </div>
  </div>
</template>

<script>
  export default {
    name: "KeyMeasureDescription",
    props: {
      measure: Object,
      shrinkLogos: Boolean
    }
  }
</script>

<style scoped lang="scss">
  .description-container {
    flex: 4;

    /deep/ .fa-check-square, /deep/ .fa-arrow-alt-circle-right {
      color: $green;
    }
  }

  .description {
    font-size: 14px;
    font-weight: 400;
    line-height: 1.5em;
    white-space: pre-wrap;
  }

  #logos {
    display: flex;
    justify-content: space-around;
    align-items: center;
    flex-wrap: wrap;
  }

  #logos > img {
    max-height: 65px;
    margin: 0.5em;
  }

  #logos.shrink > img {
    max-height: 3em;
    margin: 0.1em;
  }

  @media ( max-width: 480px ) {
    #logos > img {
      max-height: 3em;
    }
  }
</style>