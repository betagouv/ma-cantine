<template>
  <div id="key-measures">
    <h1>Les 5 mesures phares de la loi EGAlim</h1>
    <ul id="measure-cards">
      <li v-for="measure in keyMeasures" :key="measure.id">
        <div class="measure-card">
          <p class="measure-title"><KeyMeasureTitle :measure="measure"/></p>
          <ul class="statuses">
            <li v-for="subMeasure in measure.subMeasures" :key="subMeasure.id">
              <p class="sub-measure-title" :title="STATUSES[subMeasure.status] || 'Statut inconnu'">
                <i class="fas fa-fw" :class="iconClass(subMeasure.status)" aria-hidden="true"></i>
                <span class="sr-only">{{ STATUSES[subMeasure.status] || "Statut inconnu" }}:</span>
                {{ subMeasure.shortTitle }}
              </p>
            </li>
          </ul>
        </div>
        <KeyMeasureScore :measure="measure" :stroke="4" :radius="45" />
      </li>
    </ul>
    <p id="contact">Vous souhaitez nous contacter : <a href="mailto:contact@egalim.beta.gouv.fr">contact@egalim.beta.gouv.fr</a>.</p>
    <div class="measure" v-for="measure in keyMeasures" :key="measure.id" :id="measure.id">
      <KeyMeasure :measure="measure"/>
    </div>
  </div>
</template>

<script>
  import KeyMeasure from '@/components/KeyMeasure'
  import { keyMeasures } from '@/data/KeyMeasures.js';
  import KeyMeasureTitle from '@/components/KeyMeasureTitle';
  import STATUSES from '@/data/STATUSES.json';
  import KeyMeasureScore from './KeyMeasureScore';

  export default {
    components: {
      KeyMeasure,
      KeyMeasureTitle,
      KeyMeasureScore,
    },
    data() {
      return {
        keyMeasures,
        STATUSES
      };
    },
    methods: {
      iconClass(status) {
        return {
          'fa-check-square': status === 'done',
          'fa-pencil-alt': status === 'planned',
          'fa-times': status === 'notDone',
          'fa-question': !status
        }
      }
    }
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
  }

  .measure-title {
    font-weight: bold;
  }

  .sub-measure-title {
    font-size: 15px;
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

  .fa-question {
    color: $grey;
  }

  #contact, #contact a {
    color: $grey;
  }

  @media (max-width: 480px) {
    #key-measures {
      text-align: center;
      padding: 1em 0.5em;
    }
  }
</style>
