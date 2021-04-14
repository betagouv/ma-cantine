<template>
  <component :is="baseComponent"/>
</template>

<script>
  import DiversificationMeasure from "./DiversificationMeasure";
  import InformDiners from "./InformDiners";
  import QualityMeasure from "./QualityMeasure";
  import WasteMeasure from "./WasteMeasure";

  export default {
    props: {
      baseComponent: String
    },
    components: {
      DiversificationMeasure,
      InformDiners,
      QualityMeasure,
      WasteMeasure
    }
  }
</script>

<style scoped lang="scss">
  .resource, /deep/ .resource {
    display: flex;
    width: 90%;
    margin: auto;
    margin-top: 3em;
    align-items: center;
    justify-content: space-between;
    background: $light-yellow;
    border: 4px solid $yellow;
    box-sizing: border-box;
    text-decoration: none;
  }

  /deep/ .resource-icon {
    font-size: 2em;
    padding: 0.5em;
    color: $orange;
  }

  /deep/ .fa-seedling {
    color: $green;
  }

  /deep/ .resource-prompt {
    text-align: left;
    color: $dark-orange;
    width: 100%;
  }
</style>
