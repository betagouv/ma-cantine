<template>
  <div id="key-measures">
    <div id="banner">
      <img src="@/assets/online-groceries.svg" id="groceries">
      <div id="banner-content">
        <h1>Les 5 mesures-phares de la loi EGAlim</h1>
        <div id="actions">
          <a id="guide-download" download href="">Télécharger le guide du CNRC</a>
          <a id="cnrc" href="">Qu’est ce que le CNRC ?</a>
        </div>
      </div>
      <img src="@/assets/lighthouse.svg" id="lighthouse">
    </div>
    <div id="measures">
      <div class="measure" v-for="(measure, idx) in keyMeasures" :key="measure.id" :id="measure.id">
        <div class="measure-content">
          <p class="mesure-x">MESURE {{idx + 1}}</p>
          <h2>{{measure.title}}</h2>
          <div class="tags" v-if="measure.tags">
            <p class="tag" v-for="tag in measure.tags" :key="tag" :style="tags[tag].style">
              {{tags[tag].title}}
            </p>
          </div>
          <p class="deadline" v-if="measure.deadline">{{measure.deadline}}</p>
          <div v-for="subMeasure in measure.subMeasures" :key="subMeasure.id">
            <h3>{{subMeasure.title}}</h3>
            <div class="tags" v-if="subMeasure.tags">
              <p class="tag" v-for="spTag in subMeasure.tags" :key="spTag" :style="tags[spTag].style">
                {{tags[spTag].title}}
              </p>
            </div>
            <p class="deadline" v-if="subMeasure.deadline">{{subMeasure.deadline}}</p>
            <p class="description">{{subMeasure.description}}</p>
          </div>
        </div>
        <div class="decorative-image">
          <img :src="images[measure.id]" alt=""/>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
#banner {
  display: flex;
  justify-content: space-around;
  padding: 5em 10em;
}

#banner-content {
  width: 60%;
}

h1 {
  font-size: 37px;
  color: rgba(64,64,64,0.87);
  font-weight: 700;
}

#actions {
  display: flex;
  justify-content: space-evenly;
  align-items: center;
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

#cnrc {
  text-decoration: none;
  color: rgba(64,64,64,0.87);
  font-weight: 400;
  font-size: 17px;
}

#cnrc:visited {
  color: rgba(64,64,64,0.87);
}

/* measures styling */
.measures {
  width: 100%;
}

.measure {
  display: flex;
  overflow: hidden;
  align-items: center;
}

.measure-content {
  margin: 2em;
}

.decorative-image {
  width: 20%;
}

p.mesure-x {
  font-weight: 400;
  margin-bottom: 0;
  font-size: 24px;
}

h2 {
  font-size: 32px;
  font-weight: 700;
}

.tags {
  display: flex;
}

.tag {
  font-size: 12px;
  font-style: normal;
  font-weight: 700;
  color: #FFF;
  text-align: center;
  line-height: 20px;

  border-radius: 50px;
  padding: 0 1em;
  margin: 0 0.3em;
}

.deadline {
  font-size: 18px;
  font-style: italic;
  font-weight: 400;
  line-height: 31px;
}

.deadline::before {
  content: "📅 ";
}

h3 {
  font-size: 20px;
  font-weight: 400;
  line-height: 23px;
}

.description {
  font-size: 14px;
  font-weight: 400;
  line-height: 18px;
}

/* alternating alignment of measures content left and right */
#qualite-durable, #contre-gaspillage, #plastiques {
  text-align: left;
}

#information, #diversification {
  text-align: right;
  flex-direction: row-reverse;
}

#information .tags, #diversification .tags {
  justify-content: flex-end;
}

#information div img, #diversification div img {
  position: relative;
  right: 250px;
}

</style>

<script>
import SectorTags from '@/components/SectorTags.vue'
import keyMeasures from '@/data/key-measures.json'

export default {
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