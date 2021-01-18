<template>
  <div class="measure-info-card">
    <div class="deadline" v-if="measure.deadline">
      <h4>🗓 Entrée en vigeur</h4>
      <p>{{ measure.deadline }}</p>
    </div>
    <SectorTags :tags="measure.tags" />
  </div>
</template>

<style scoped>
.measure-info-card {
  max-width: 274px;
  flex: 1;
  background: #F1F3EE;
  border-radius: 15px;
  padding: 1em 1.5em;
  margin-right: 2em;
}

.deadline > h4 {
  margin-top: 0.5em;
  font-weight: bold;
  font-size: 18px;
  margin-bottom: 1em;
  /* Dark 1 */
  color: #333333;
}

.deadline > p {
  font-size: 14px;
  color: #000000;
}
</style>

<script>
import SectorTags from "@/components/SectorTags.vue";

export default {
  name: "KeyMeasureInfoCard",
  props: {
    measure: Object
  },
  components: {
    SectorTags,
  },
};
</script>