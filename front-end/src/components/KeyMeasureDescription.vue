<template>
  <div class="description-container">
    <p class="description" v-if="measure.htmlDescription" v-html="measure.htmlDescription"></p>
    <p class="description" v-else-if="measure.description">{{measure.description}}</p>
    <KeyMeasureDescriptionQuality v-if="measure.id === 'qualite-des-produits'"/>
    <KeyMeasureDescriptionLabels v-if="measure.id === 'cinquante'" class="description"/>
    <LogoBio id="bio-logo" v-if="measure.id === 'vingt'"/>
  </div>
</template>

<script>
  import KeyMeasureDescriptionQuality from '@/components/KeyMeasureDescriptionQuality';
  import KeyMeasureDescriptionLabels from '@/components/KeyMeasureDescriptionLabels';
  import LogoBio from '@/components/LogoBio';

  export default {
    name: "KeyMeasureDescription",
    props: {
      measure: Object,
    },
    components: {
      KeyMeasureDescriptionQuality,
      KeyMeasureDescriptionLabels,
      LogoBio
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

  #bio-logo {
    height: 2.9em;
    margin-top: 1em;
  }
</style>