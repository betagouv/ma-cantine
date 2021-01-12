<template>
  <div id="key-measures">
    <div id="banner">
      <img src="@/assets/online-groceries.svg" id="groceries" alt="">
      <div id="banner-content">
        <h1>Les 5 mesures-phares de la loi EGAlim</h1>
        <div id="actions">
          <a id="guide-download" download href="">Télécharger le guide du CNRC</a>
          <a id="about-cnrc" href="">Qu'est ce que le CNRC ?</a>
        </div>
      </div>
      <img src="@/assets/lighthouse.svg" id="lighthouse" alt="">
    </div>
    <div id="measures">
      <div class="measure" v-for="(measure, idx) in keyMeasures" :key="measure.id" :id="measure.id">
        <div class="measure-content">
          <p class="measure-x">MESURE {{idx + 1}}</p>
          <h2>{{measure.title}}</h2>
          <SectorTags :tags="measure.tags"/>
            <p class="deadline" v-if="measure.deadline">
              <span class="deadline-emoji">📅 </span>
              {{measure.deadline}}
            </p>
          <div v-for="subMeasure in measure.subMeasures" :key="subMeasure.id" :id="subMeasure.id">
            <h3>{{subMeasure.title}}</h3>
            <SectorTags :tags="subMeasure.tags"/>
            <p class="deadline" v-if="subMeasure.deadline">
              <span class="deadline-emoji">📅 </span>
              {{subMeasure.deadline}}
            </p>
            <div class="description-container">
              <p class="description" v-if="subMeasure.htmlDescription" v-html="subMeasure.htmlDescription"></p>
              <p class="description" v-if="subMeasure.description">{{subMeasure.description}}</p>
              <img v-if="subMeasure.id === 'vingt'" src="@/assets/logos/logo_bio_eurofeuille.png" id="eurofeuille">
            </div>
            <div id="logos" v-if="subMeasure.id === 'cinquante'">
              <img src="@/assets/logos/label-rouge.png" alt="logo Label Rouge"/>
              <img src="@/assets/logos/Logo-AOC-AOP.png" alt="logo appellation d’origine"/>
              <img src="@/assets/logos/IGP.png" alt="logo indication géographique"/>
              <img src="@/assets/logos/STG.png" alt="logo Spécialité traditionnelle garantie"/>
              <img src="@/assets/logos/hve.png" alt="logo Haute Valeur Environnementale"/>
              <img src="@/assets/logos/logo_label-peche-durable.png" alt="logo écolabel pêche durable"/>
              <img src="@/assets/logos/rup.png" alt="logo Région Ultrapériphérique"/>
            </div>
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
  /* TODO: supprimer ça quand on a des liens */
  display: none;
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

p.measure-x {
  font-weight: 400;
  margin-bottom: 0;
  font-size: 24px;
}

h2 {
  font-size: 32px;
  font-weight: 700;
}

.deadline {
  font-size: 18px;
  font-style: italic;
  font-weight: 400;
  line-height: 31px;
}

.deadline-emoji {
  font-style: normal;
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
  white-space: pre-wrap;
}

#logos {
  display: flex;
  justify-content: space-around;
  align-items: center;
}

#logos > img {
  max-height: 75px;
}

#vingt div.description-container {
  display: flex;
  align-items: center;
}

#eurofeuille {
  max-height: 66px;
  margin-left: 71px;
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
      SectorTags,
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