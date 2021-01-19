<template>
  <div class="measure-card">
    <div class="measure-info-card">
      <div class="deadline">
        <h4>🗓 {{ measure.deadline.type || "Entrée en vigeur" }}</h4>
        <p>{{ measure.deadline.display || measure.deadline }}</p>
      </div>
      <div class="tags">
        <h4>🍽 Pour qui ?</h4>
        <p v-if="measure.who">{{measure.who}}</p>
        <p class="tag" :class="tag" v-for="tag in measure.tags" :key="tag">
          {{ tagsInfo[tag] }}
        </p>
      </div>
    </div>
    <div class="calculator-card" v-if="includeCalculatorCard">
      <h4>👉 Suis-je en règle ?</h4>
      <p>Utilisez notre simulateur pour calculer votre répartition de produits durables et bio.</p>
      <a :href="`${publicPath}Diagnostic approvisionnement (ma-cantine-alpha) v0.1.ods`" download class="simulator-link">Vérifier mes achats</a>
    </div>
  </div>
</template>

<style scoped>
.measure-card {
  max-width: 274px;
  flex: 1.2;
  margin-right: 2em;
}

.measure-info-card, .calculator-card {
  background: #F1F3EE;
  border-radius: 15px;
  padding: 1em 1.5em;
}

h4 {
  margin-top: 0.5em;
  font-weight: bold;
  font-size: 18px;
  margin-bottom: 1em;
  /* Dark 1 */
  color: #333333;
  white-space: nowrap;
}

p {
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

.calculator-card {
  margin-top: 4em;
}

.simulator-link {
  font-size: 18px;
  text-align: center;
  color: rgba(255, 255, 255, 0.867527);
  font-weight: bold;
  text-decoration: none;
  white-space: nowrap;
  /* Green 1 */
  background: #748852;
  border-radius: 50px;
  padding: 0.5em 0.8em;
  line-height: 3.5em;
}

@media (max-width: 800px) {
  h4 {
    font-size: 16px;
  }

  .simulator-link {
    font-size: 14px;
  }
}

@media (max-width: 480px) {
  .measure-info-card {
    margin-right: 0em;
  }

  .simulator-link {
    font-size: 18px;
  }
}
</style>

<script>
import tags from "@/data/sector-tags.json";

export default {
  name: "KeyMeasureInfoCard",
  props: {
    measure: Object,
    includeCalculatorCard: Boolean
  },
  data() {
    return {
      tagsInfo: tags,
      publicPath: process.env.BASE_URL,
    }
  },
};
</script>