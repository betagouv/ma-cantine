<template>
  <div>
    <div id="key-measures">
      <h1>Les 5 mesures phares de la loi EGAlim</h1>
      <ul id="measure-cards">
        <li v-for="measure in keyMeasures" :key="measure.id">
          <router-link :to="{ name: 'KeyMeasurePage', params: { id: measure.id } }" class="measure-card">
            <p class="measure-title"><KeyMeasureTitle :measure="measure"/></p>
            <ul class="statuses">
              <li v-for="subMeasure in measure.subMeasures" :key="subMeasure.id">
                <p class="sub-measure-title">
                  {{ subMeasure.shortTitle }}
                </p>
              </li>
            </ul>
          </router-link>
        </li>
      </ul>
    </div>
    <router-link :to="{ name: 'DiagnosticPage' }">
      <div class="presentation-diagnostic">Savoir où j'en suis des mesures EGAlim</div>
    </router-link>
    <div class="resources">
      <h2>Quelques ressources pour répondre aux mesures</h2>
      <KeyMeasureResource baseComponent='QualityMeasure'/>
      <KeyMeasureResource baseComponent='InformDiners'/>
      <KeyMeasureResource baseComponent='WasteMeasure'/>
    </div>
  </div>
</template>

<script>
  import { keyMeasures } from '@/data/KeyMeasures.js';
  import KeyMeasureTitle from '@/components/KeyMeasureTitle';
  import KeyMeasureResource from '@/components/KeyMeasureResource';

  export default {
    components: {
      KeyMeasureTitle,
      KeyMeasureResource,
    },
    data() {
      return {
        keyMeasures,
      };
    },
  }
</script>

<style scoped lang="scss">
  #key-measures {
    text-align: center;
    padding: 1em 1em;

    h1 {
      font-weight: bold;
      font-size: 48px;
      color: $green;
      margin: 1em 0em;
    }

    .measure {
      text-align: left;
      display: flex;
      overflow: hidden;
      align-items: center;
      max-width: 1170px;
      margin: auto;
    }
  }

  a {
    text-decoration: none;
  }

  #measure-cards {
    display: flex;
    justify-content: space-evenly;
    flex-wrap: wrap;
  }

  .measure-card {
    background: $light-yellow;
    width: 11em;
    height: 15em;
    border-radius: 22px;
    padding: 0.5em 1em;
    margin: 0.5em;
    text-align: left;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    color: $black;
    transition: all ease .25s;
    border: 1px solid $light-yellow;
  }

  .measure-card:hover {
    border-color: $orange;
    transform: scale(1.02);
  }

  .measure-title {
    font-weight: bold;
    margin-bottom: 0;
  }

  .sub-measure-title {
    font-size: 15px;
    margin: 0.8em 0;
  }

  .presentation-diagnostic {
    display: inline-block;
    margin: auto;
    padding: 1em 2em;
    color: $white;
    background-color: $orange;
    border-radius: 50px;
    font-weight: bold;
    text-align: center;
  }

  h2 {
    margin-top: 50px;
  }

  .resources h2:only-child {
    display: none;
  }

  @media (max-width: 480px) {
    #key-measures {
      text-align: center;
      padding: 1em 0.5em;
    }
  }
</style>
