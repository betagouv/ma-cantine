<template>
  <div class="tags" v-if="tags">
    <h4>🍽 Pour qui ?</h4>
    <p class="tag" :class="tag" v-for="tag in tags" :key="tag">
      {{ tagsInfo[tag] }}
    </p>
  </div>
</template>

<script>
const tagsInfo = {
  scolaire: "Scolaire",
  administration: "Administration",
  universitaire: "Universitaire",
  medical: "Médical",
  social: "Social",
  creche: "Crèche",
  loisirs: "Loisirs",
  entreprises: "Entreprises"
};

export default {
  name: "SectorTags",
  props: {
    tags: Array
  },
  data() {
    return {
      tagsInfo: tagsInfo,
    };
  },
};
</script>

<style scoped>
h4 {
  font-weight: bold;
  font-size: 18px;
  margin-bottom: 1em;
  /* Dark 1 */
  color: #333333;
}

.tag {
  font-size: 14px;
  font-weight: bold;
  margin: 0.5em 0em;
  /* Green 1 */
  color: #748852;
}
</style>