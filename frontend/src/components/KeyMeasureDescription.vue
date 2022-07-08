<template>
  <div class="description-container">
    <p class="description" v-if="measure.htmlDescription" v-html="measure.htmlDescription"></p>
    <p class="description" v-else-if="measure.description">{{ measure.description }}</p>
    <component :is="measure.descriptionComponent" v-if="measure.descriptionComponent" class="description" />
  </div>
</template>

<script>
import KeyMeasureDescriptionQuality from "@/components/KeyMeasureDescriptionQuality"
import KeyMeasureDescriptionLabels from "@/components/KeyMeasureDescriptionLabels"
import LogoBio from "@/components/LogoBio"

export default {
  name: "KeyMeasureDescription",
  props: {
    measure: Object,
  },
  components: {
    KeyMeasureDescriptionQuality,
    KeyMeasureDescriptionLabels,
    LogoBio,
  },
}
</script>

<style scoped lang="scss">
.description-container {
  flex: 4;
}

.description {
  font-size: 14px;
  font-weight: 400;
  line-height: 1.5em;
  white-space: pre-wrap;
}
</style>
