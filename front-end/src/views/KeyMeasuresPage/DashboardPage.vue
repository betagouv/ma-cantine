<template>
  <div id="key-measures">
    <h1>Mon tableau de bord</h1>
    <ul id="measure-cards">
      <li v-for="measure in keyMeasures" :key="measure.id">
        <router-link :to="{ name: 'KeyMeasurePage', params: { id: measure.id } }" class="measure-card">
          <p class="measure-title"><KeyMeasureTitle :measure="measure"/></p>
          <ul class="statuses">
            <li v-for="subMeasure in measure.subMeasures" :key="subMeasure.id">
              <p class="sub-measure-title" :title="getSubMeasureStatusTitle(subMeasure)">
                <i
                  class="fas fa-fw"
                  :class="iconClass(subMeasure.status)"
                  aria-hidden="true"
                ></i>
                <span class="sr-only">{{ STATUSES[subMeasure.status] || "Statut inconnu" }}:</span>
                {{ subMeasure.shortTitle }}
              </p>
              <p class="already-applicable" v-if="warnMissedDeadline(subMeasure)">
                Déjà applicable
              </p>
            </li>
          </ul>
        </router-link>
        <KeyMeasureScore :measure="measure"/>
      </li>
    </ul>
  </div>
  <div class="resources">
    <h2> Quelques ressources pour répondre aux mesures</h2>
    <KeyMeasureResource baseComponent='QualityMeasure' v-if="isIncomplete('cinquante') || isIncomplete('vingt')"/>
    <KeyMeasureResource baseComponent='InformDiners' v-if="isIncomplete('convives-informes')"/>
    <KeyMeasureResource baseComponent='WasteMeasure' v-if="isIncomplete('dons')"/>
  </div>
</template>

<script>
  import { keyMeasures, findSubMeasure } from '@/data/KeyMeasures.js';
  import KeyMeasureTitle from '@/components/KeyMeasureTitle';
  import STATUSES from '@/data/STATUSES.json';
  import KeyMeasureScore from '@/components/KeyMeasureScore';
  import KeyMeasureResource from '@/components/KeyMeasureResource';

  export default {
    components: {
      KeyMeasureTitle,
      KeyMeasureScore,
      KeyMeasureResource,
    },
    data() {
      return {
        keyMeasures,
        STATUSES,
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
      },
      isIncomplete(subMeasureId) {
        return findSubMeasure(subMeasureId).status !== "done";
      },
      getSubMeasureStatusTitle(subMeasure) {
        return STATUSES[subMeasure.status] || 'Statut inconnu';
      }
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
