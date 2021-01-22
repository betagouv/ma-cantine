<template>
  <div id="key-measures">
    <h1>Les 5 mesures phares de la loi EGAlim</h1>
    <p>Découvrez vos obligations légales selon votre secteur.</p>
    <!-- remove actions entirely? -->
    <div id="actions">
      <a id="guide-download" download href="">Télécharger le guide du CNRC</a>
      <a id="about-cnrc" href="">Qu'est ce que le CNRC ?</a>
    </div>
    <ul id="tag-filter" class="filter">
      <li>
        <FilterButton text="Tous les secteurs" :isActive="activeTags.includes(allSectorsId)" @toggle-activation="updateSectorFilter(allSectorsId)"/>
      </li>
      <li v-for="(tag, id) in tags" :key="tag">
        <FilterButton :text="tag" :isActive="activeTags.includes(id)" @toggle-activation="updateSectorFilter(id)"/>
      </li>
    </ul>
    <ul id="deadline-filter" class="filter">
      <li><FilterButton text="Toutes les mesures" :isActive="true"/></li>
      <li><FilterButton text="Seulement les mesures à venir"/></li>
    </ul>
    <div id="measures">
      <div class="measure" v-for="measure in measuresFilteredBySector" :key="measure.id" :id="measure.id">
        <div class="measure-content">
          <h2>{{measure.title}}</h2>
          <div class="measure-details">
            <InfoCard v-if="measure.tags" :measure="measure" :includeCalculatorCard="measure.id === 'qualite-durable'"/>
            <div class="description-container">
              <p v-if="measure.description">{{measure.description}}</p>
              <div v-for="subMeasure in measure.subMeasures" :key="subMeasure.id" :id="subMeasure.id">
                <h3>{{subMeasure.title}}</h3>
                <div class="measure-details">
                  <InfoCard v-if="subMeasure.tags" :measure="subMeasure"/>
                  <!-- refactor to a KeyMeasureDescription, which has all the HTML formatting when switch to fontawesome icons -->
                  <div class="description-container">
                    <p class="description" v-if="subMeasure.htmlDescription" v-html="subMeasure.htmlDescription"></p>
                    <p class="description" v-if="subMeasure.description">{{subMeasure.description}}</p>
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
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script src="./script.js"></script>
<style src="./style.css"></style>