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
  .fa-apple-alt {
    color: $red;
  }
  
  .fa-bullhorn {
    color: $yellow;
  }

  .fa-hands {
    color: $orange;
  }

  .fa-leaf {
    color: $green;
  }

  .fa-wind {
    color: $blue;
  }
</style>