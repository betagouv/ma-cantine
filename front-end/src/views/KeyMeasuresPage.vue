<template>
  <div id="key-measures">
    <h1>Les 5 mesures-phares de la loi EGAlim</h1>
    <p>Découvrez vos obligations légales selon votre secteur.</p>
    <!-- remove actions entirely? -->
    <div id="actions">
      <a id="guide-download" download href="">Télécharger le guide du CNRC</a>
      <a id="about-cnrc" href="">Qu'est ce que le CNRC ?</a>
    </div>
    <ul id="tag-filter" class="filter">
      <!-- refactor the button into a component: KeyMeasuresFilterOption -->
      <li><button type="button" class="filter-button is-active">Tous les secteurs</button></li>
    </ul>
    <ul id="deadline-filter" class="filter">
      <li><button type="button" class="filter-button is-active">Toutes les mesures</button></li>
      <li><button type="button" class="filter-button">Seulement les mesures à venir</button></li>
    </ul>
    <div id="measures">
      <div class="measure" v-for="measure in keyMeasures" :key="measure.id" :id="measure.id">
        <div class="measure-content">
          <h2>{{measure.title}}</h2>
          <div class="measure-details">
            <!-- Refactor into own component KeyMeasureInfoCard -->
            <div class="measure-info-card" v-if="measure.tags">
              <div class="deadline" v-if="measure.deadline">
                <h4>🗓  Entrée en vigeur</h4>
                <p>{{measure.deadline}}</p>
              </div>
              <SectorTags :tags="measure.tags"/>
            </div>
            <div class="sub-measures">
              <p v-if="measure.description">{{measure.description}}</p>
              <div v-for="subMeasure in measure.subMeasures" :key="subMeasure.id" :id="subMeasure.id">
                <h3>{{subMeasure.title}}</h3>
                <!-- Add KeyMeasureInfoCard here -->
                <!-- <SectorTags :tags="subMeasure.tags"/>
                <p class="deadline" v-if="subMeasure.deadline">
                  <span class="deadline-emoji">📅 </span>
                  {{subMeasure.deadline}}
                </p> -->
                <div class="description-container">
                  <!-- Is there a better way to manage the formatting of descriptions now more need HTML? -->
                  <p class="description" v-if="subMeasure.htmlDescription" v-html="subMeasure.htmlDescription"></p>
                  <p class="description" v-if="subMeasure.description">{{subMeasure.description}}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
#key-measures {
  text-align: center;
  padding: 1em 1em;
}
/* #banner {
  display: flex;
  justify-content: space-around;
  padding: 5em 10em;
}

#banner-content {
  width: 60%;
} */

h1 {
  font-weight: bold;
  font-size: 48px;
  /* Green 1 */
  color: #748852;
  margin: 1em 0em;
}

p {
  font-size: 18px;
  /* Dark 1 */
  color: #333333;
}

#actions {
  display: flex;
  justify-content: space-evenly;
  align-items: center;
  /* TODO: supprimer ça quand on a des liens */
  display: none;
}

.filter {
  display: flex;
  padding: 0.5em 10%;
  justify-content: center;
  align-items: center;
}

.filter-button {
  border: none;
  background-color: #fff;
  cursor: pointer;
  margin: 0 1em;
  font-weight: bold;
  font-size: 22px;
  /* Dark 1 */
  color: #333333;
}

.filter-button.is-active {
  width: 244px;
  height: 43px;
  left: 0px;
  top: 0px;

  /* Green 3 */
  background: #F1F3EE;
  border-radius: 42px;
  /* Green 1 */
  color: #748852;
}

#guide-download {
  border-radius: 25px;
  background: rgb(0,191,113);
  color: #FFF;
  padding: 0.7em 2em;
  text-decoration: none;
  font-weight: 700;
  font-size: 14px;
}

#about-cnrc {
  text-decoration: none;
  color: rgba(64,64,64,0.87);
  font-weight: 400;
  font-size: 17px;
}

#about-cnrc:visited {
  color: rgba(64,64,64,0.87);
}

/* measures styling */
#measures {
  text-align: left;
}

.measure {
  display: flex;
  overflow: hidden;
  align-items: center;
  max-width: 1170px;
  margin: auto;
}

.measure-content {
  margin: 2em;
}

h2 {
  font-weight: bold;
  font-size: 32px;
  color: #000000;
}

.measure-details {
  display: flex;
  align-items: flex-start;
}

.measure-info-card {
  max-width: 274px;
  flex: 1;
  background: #F1F3EE;
  border-radius: 15px;
  padding: 1em 1.5em;
  margin-right: 2em;
}

.sub-measures {
  flex: 4;
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

h3 {
  font-weight: bold;
  font-size: 24px;
  /* Green 1 */
  color: #748852;
}

.description {
  font-size: 14px;
  font-weight: 400;
  line-height: 18px;
  white-space: pre-wrap;
}
</style>

<script>
import SectorTags from '@/components/SectorTags'
import keyMeasures from '@/data/key-measures.json'

export default {
  components: {
    SectorTags
  },
  data() {
    return {
      keyMeasures
    };
  },
  computed: {
    images() {
      let images = {};
      keyMeasures.forEach((measure) =>
        images[measure.id] = require('@/assets/background/'+measure.image));
      return images;
    }
  }
}
</script>
