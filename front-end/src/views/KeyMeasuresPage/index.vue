<template>
  <div id="key-measures">
    <h1>Les 5 mesures phares de la loi EGAlim</h1>
    <p>Découvrez vos obligations légales selon votre secteur.</p>
    <!-- remove actions entirely? -->
    <div id="actions">
      <a id="guide-download" download href="">Télécharger le guide du CNRC</a>
      <a id="about-cnrc" href="">Qu'est ce que le CNRC ?</a>
    </div>
    <div id="measures">
      <div class="measure" v-for="measure in keyMeasures" :key="measure.id" :id="measure.id">
        <div class="measure-content">
          <h2><KeyMeasureTitle :measure="measure"/></h2>
          <div class="measure-details">
            <KeyMeasureInfoCard v-if="measure.tags" :measure="measure" :includeCalculatorCard="measure.id === 'qualite-durable'"/>
            <div class="description-container">
              <KeyMeasureDescription :measure="measure" v-if="measure.description"/>
              <div v-for="subMeasure in measure.subMeasures" :key="subMeasure.id" :id="subMeasure.id">
                <h3>{{subMeasure.title}}</h3>
                <div class="measure-details">
                  <KeyMeasureInfoCard v-if="subMeasure.tags" :measure="subMeasure"/>
                  <KeyMeasureDescription :measure="subMeasure"/>
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
<style scoped lang="scss" src="./style.scss"></style>
