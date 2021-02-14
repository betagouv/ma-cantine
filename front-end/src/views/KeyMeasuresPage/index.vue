<template>
  <div id="key-measures">
    <h1>Les 5 mesures phares de la loi EGAlim</h1>
    <div id="measures" v-for="measure in keyMeasures" :key="measure.id">
      <KeyMeasure :measure="measure"/>
    </div>
  </div>
</template>

<script src="./script.js"></script>
<style scoped lang="scss" src="./style.scss"></style>
