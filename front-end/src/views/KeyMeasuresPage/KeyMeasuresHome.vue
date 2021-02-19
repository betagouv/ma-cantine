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
              <p class="already-applicable" v-if="warnMissedDeadline(subMeasure)">
                Déjà applicable
              </p>
            </li>
          </ul>
        </div>
        <KeyMeasureScore :measure="measure" />
      </li>
    </ul>
  </div>
</template>

<script>
  import { keyMeasures } from '@/data/KeyMeasures.js';
  import KeyMeasureTitle from '@/components/KeyMeasureTitle';
  import STATUSES from '@/data/STATUSES.json';
  import KeyMeasureScore from '@/components/KeyMeasureScore';

  export default {
    components: { 
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
      },
      warnMissedDeadline(measure) {
        let deadline = measure.deadline?.earliestISO;
        if(measure.status && measure.status !== 'done' && deadline) {
          return new Date(deadline) < new Date();
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
    align-items: stretch;
  }

  .measure-card {
    background: $light-yellow;
    width: 11em;
    height: calc(100% - 120px);
    min-height: 13em;
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
    margin-bottom: 0;
  }

  .sub-measure-title {
    font-size: 15px;
    margin: 0.8em 0;
  }

  .already-applicable {
    color: $red;
    font-weight: bold;
    font-size: 13px;
    margin-top: -0.5em;
    text-align: right;
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

  @media (max-width: 480px) {
    #key-measures {
      text-align: center;
      padding: 1em 0.5em;
    }
  }
</style>
