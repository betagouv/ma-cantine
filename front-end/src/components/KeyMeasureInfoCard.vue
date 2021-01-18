<template>
  <div class="measure-info-card">
    <div class="deadline" v-if="measure.deadline">
      <h4>🗓 Entrée en vigeur</h4>
      <p>{{ measure.deadline }}</p>
    </div>
    <div class="tags" v-if="measure.tags">
      <h4>🍽 Pour qui ?</h4>
      <p class="tag" :class="tag" v-for="tag in measure.tags" :key="tag">
        {{ tagsInfo[tag] }}
      </p>
    </div>
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

h4 {
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

.tag {
  font-size: 14px;
  font-weight: bold;
  margin: 0.5em 0em;
  /* Green 1 */
  color: #748852;
}
</style>

<script>
import tags from "@/data/tags.json";

export default {
  name: "KeyMeasureInfoCard",
  props: {
    measure: Object
  },
  data() {
    return {
      tagsInfo: tags
    }
  },
};
</script>