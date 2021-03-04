<template>
  <div class="description-container">
    <p class="description" v-if="measure.htmlDescription" v-html="measure.htmlDescription"></p>
    <p class="description" v-else-if="measure.description">{{measure.description}}</p>
    <LogoList v-if="measure.id === 'cinquante'" />
  </div>
</template>

<script>
  import LogoList from '@/components/LogoList'

  export default {
    name: "KeyMeasureDescription",
    components: {
      LogoList,
    },
    props: {
      measure: Object,
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
</style>
