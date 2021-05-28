<template>
  <div v-if="measure">
    <i :class="`fas ${measure.faIcon}`" v-if="measure.faIcon"></i>
    <span class="ml-4">{{ measure.title }}</span>
  </div>
</template>

<script>
export default {
  name: "KeyMeasureTitle",
  props: {
    measure: Object,
  },
}
</script>

<style scoped lang="scss">
.fa-apple-alt {
  color: $ma-cantine-red;
}

.fa-bullhorn {
  color: $ma-cantine-yellow;
}

.fa-hands {
  color: $ma-cantine-orange;
}

.fa-leaf {
  color: $ma-cantine-green;
}

.fa-wind {
  color: $ma-cantine-blue;
}
</style>
