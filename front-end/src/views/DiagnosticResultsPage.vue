<template>
  <div id="diagnostic-results">
    <h1>Votre auto-évaluation mesures EGAlim</h1>
    <h2>Merci d’avoir répondu. Voici vos résultats d’auto-diagnostic.<br>Vous souhaitez nous contacter : <a href="mailto:contact@egalim.beta.gouv.fr" id="contact">contact@egalim.beta.gouv.fr</a>.</h2>
    <ul id="measure-cards">
      <li class="measure-card" v-for="measure in keyMeasures" :key="measure.id">
        <p class="measure-title"><KeyMeasureTitle :measure="measure"/></p>
        <ul class="statuses">
          <li v-for="subMeasure in measure.subMeasures" :key="subMeasure.id">
            <!-- TODO: improve a11y https://fontawesome.com/how-to-use/on-the-web/other-topics/accessibility -->
            <p class="sub-measure-title" :title="STATUSES[subMeasure.status || 'notDone']"><i class="fas fa-fw" :class="iconClass(subMeasure.status)"></i>
            {{ subMeasure.shortTitle }}</p>
          </li>
        </ul>
      </li>
    </ul>
  </div>
</template>

<script>
  import keyMeasures from '@/data/KeyMeasures.js';
  import KeyMeasureTitle from '@/components/KeyMeasureTitle';
  import STATUSES from '@/data/STATUSES.json';

  export default {
    components: {
      KeyMeasureTitle
    },
    data() {
      return {
        keyMeasures,
        STATUSES
      }
    },
    methods: {
      iconClass(status) {
        return {
          'fa-check-square': status === 'done',
          'fa-pencil-alt': status === 'planned',
          'fa-times': status === 'notDone' || !status
        }
      }
    }
  }
</script>

<style scoped lang="scss">
  #diagnostic-results {
    padding: 2em;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  h1 {
    font-size: 48px;
    color: $green;
    margin: 1em 0em;
  }

  h2 {
    color: $light-grey;
    width: 80%;
    font-weight: normal;
  }

  #contact {
    color: $light-grey;
  }

  #measure-cards {
    display: flex;
    justify-content: space-evenly;
    flex-wrap: wrap;
  }

  .measure-card {
    border: 1px solid $light-yellow;
    background: $light-yellow;
    border-radius: 22px;
    width: 12em;
    border-radius: 22px;
    padding: 0.5em 1em;
    margin: 0.5em;
    text-align: left;
    font-size: 14px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  .measure-title {
    font-weight: bold;
  }

  .fas {
    width: 0.3em;
  }

  .fa-check-square {
    color: $green;
  }

  .fa-pencil-alt {
    color: $yellow;
  }

  .fa-times {
    color: $red;
  }
</style>