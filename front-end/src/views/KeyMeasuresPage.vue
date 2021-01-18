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
      <li>
        <key-measures-filter-button text="Tous les secteurs" :isActive="activeTags.indexOf(allTagsId) > -1" @toggle-activation="toggleActivation(allTagsId)"/>
      </li>
      <li v-for="(tag, id) in tags" :key="tag">
        <key-measures-filter-button :text="tag" :isActive="activeTags.indexOf(id) > -1" @toggle-activation="toggleActivation(id)"/>
      </li>
    </ul>
    <ul id="deadline-filter" class="filter">
      <li><key-measures-filter-button text="Toutes les mesures" :isActive="true"/></li>
      <li><key-measures-filter-button text="Seulement les mesures à venir"/></li>
    </ul>
    <div id="measures">
      <div class="measure" v-for="measure in filteredKeyMeasures" :key="measure.id" :id="measure.id">
        <div class="measure-content">
          <h2>{{measure.title}}</h2>
          <div class="measure-details">
            <KeyMeasureInfoCard v-if="measure.tags" :measure="measure"/>
            <div class="description-container">
              <p v-if="measure.description">{{measure.description}}</p>
              <div v-for="subMeasure in measure.subMeasures" :key="subMeasure.id" :id="subMeasure.id">
                <h3>{{subMeasure.title}}</h3>
                <!-- Add KeyMeasureInfoCard here -->
                <div class="measure-details">
                  <KeyMeasureInfoCard v-if="subMeasure.tags" :measure="subMeasure"/>
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
  </div>
</template>

<style scoped>
#key-measures {
  text-align: center;
  padding: 1em 1em;
}

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
  padding: 0.5em 5%;
  justify-content: space-around;
  align-items: center;
  flex-wrap: wrap;
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

.description-container {
  flex: 4;
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
import KeyMeasureInfoCard from '@/components/KeyMeasureInfoCard.vue'
import KeyMeasuresFilterButton from '@/components/KeyMeasuresFilterButton.vue'
import keyMeasures from '@/data/key-measures.json'
import tags from '@/data/sector-tags.json'

const allTagsId = 'all';

export default {
  components: {
    KeyMeasureInfoCard,
    KeyMeasuresFilterButton
  },
  data() {
    return {
      keyMeasures,
      tags,
      activeTags: [allTagsId],
      allTagsId
    };
  },
  computed: {
    images() {
      let images = {};
      keyMeasures.forEach((measure) =>
        images[measure.id] = require('@/assets/background/'+measure.image));
      return images;
    },
    filteredKeyMeasures() {
      const activeTags = this.activeTags;
      function testTags(measure) {
        return (measure.tags || []).some((tag) => activeTags.indexOf(tag) > -1);
      }
      if(activeTags.indexOf(allTagsId) > -1) {
        return this.keyMeasures;
      } else {
        return this.keyMeasures.filter((measure) => {
          return testTags(measure) || (measure.subMeasures || []).some(testTags);
        }).map((measure) => {
          if(measure.subMeasures) {
            measure.subMeasures = measure.subMeasures.filter(testTags)
          }
          return measure;
        });
      }
    }
  },
  methods: {
    toggleActivation(id) {
      const tagIndex = this.activeTags.indexOf(id);
      if(tagIndex > -1) { // currently active, want to deactivate
        this.activeTags.splice(tagIndex, 1);
        // add back all to avoid losing all text on screen
        if(this.activeTags.length === 0) {
          this.activeTags.push(allTagsId);
        }
      } else if(id === allTagsId) {
        // reset to avoid having 'all' and other tags
        this.activeTags = [allTagsId];
      } else {
        this.activeTags.push(id);
        // remove 'all' to avoid having 'all' and other tags
        if(this.activeTags.indexOf(allTagsId) > -1) {
          this.activeTags.splice(this.activeTags.indexOf(allTagsId), 1);
        }
      }
    }
  }
}
</script>