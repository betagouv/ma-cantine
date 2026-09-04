<template>
  <div v-if="measure">
    <v-icon x-large class="mt-n2" :color="measure.mdiIconColor">{{ measure.mdiIcon }}</v-icon>
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
