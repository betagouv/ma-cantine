<template>
  <span><i :class="'fas '+measure.faIcon" v-if="measure.faIcon"></i>
   {{measure.title}}</span>
</template>

<script>
  export default {
    name: "KeyMeasureTitle",
    props: {
      measure: Object
    },
  }
</script>

<style scoped lang="scss">
  .fa-apple-alt, .fa-hands, .fa-wind {
    color: $orange;
  }
  
  .fa-bullhorn, .fa-leaf {
    color: $green;
  }
</style>