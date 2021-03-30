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
  <div class="resources">
    <h2> Quelques ressources pour répondre aux mesures</h2>
    <KeyMeasureResource baseComponent='QualityMeasure' v-if="isIncomplete('cinquante') || isIncomplete('vingt')"/>
    <KeyMeasureResource baseComponent='InformDiners' v-if="isIncomplete('convives-informes')"/>
    <KeyMeasureResource baseComponent='WasteMeasure' v-if="isIncomplete('dons')"/>
  </div>
  <form id="publish-form" @submit.prevent="submit">
    <h2>Devenir béta-testeur</h2>
    <p>
      Nous sommes en version de test et cherchons continuellement à améliorer la plateforme.
      Pour cela nous cherchons des cantines prêtes à nous accompagner en devenant béta-testeur.
      Si vous souhaitez y participer merci de nous communiquer vos informations ci-dessous.
    </p>
    <label for="school" class="publish-label">Nom de votre cantine</label>
    <input id="school" class="publish-input" v-model="form.school" required>
    <label for="city" class="publish-label">Ville / commune</label>
    <input id="city" class="publish-input" v-model="form.city" required>
    <label for="email" class="publish-label">Votre email</label>
    <input id="email" class="publish-input" v-model="form.email" type="email" required>
    <label for="phone" class="publish-label" type="tel">Numéro de téléphone (optionnel)</label>
    <input id="phone" class="publish-input" v-model="form.phone">
    <label for="message" class="publish-label">Message (optionnel)</label>
    <textarea id="message" class="publish-input" v-model="form.message" />
    <input type="submit" id="submit" value="Je participe">
  </form>
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
        form: {},
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
      async submit() {
        const response = await fetch("http://localhost:3000/subscribe-beta-tester", {
          method: "POST",
          body: JSON.stringify({
            keyMeasures: this.keyMeasures,
            form: this.form
          })
        });

        if (response.status === 201) {
          this.form = {};
          alert("Merci de vôtre intérêt pour ma cantine, nous reviendrons vers vous dans les plus brefs délais.")
        } else {
          const error = await response.json();
          console.log(error);
          alert("Une erreur est survenue, vous pouvez nous contacter directement à contact@egalim.beta.gouv.fr")
        }
      },
      isIncomplete(subMeasureId) {
        return findSubMeasure(subMeasureId).status !== "done";
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

  h2 {
    margin-top: 50px;
  }

  .resources h2:only-child {
    display: none;
  }

  #publish-form {
    display: flex;
    flex-direction: column;
    width: 90%;
    margin: 50px auto;

    .publish-label {
      text-align: left;
      margin-top: 15px;
    }

    .publish-input {
      margin-top: 10px;
      border: none;
      border-bottom: 6px solid $light-orange;
      font-size: 1.2em;
      padding: 5px;
      background-color: $light-orange;
    }

    .publish-input:required {
      border-bottom-color: $orange;
    }

    .publish-input:required:invalid {
      outline: none;
      box-shadow: none;
    }

    .publish-input:required:valid {
      border-bottom-color: $light-orange;
    }

    #message {
      height: 100px;
    }

    #submit {
      width: 150px;
      font-size: 1.2em;
      margin: auto;
      margin-top: 30px;
      border: none;
      background: $orange;
      border-radius: 1em;
      padding: 0.5em;
      color: $white;
      float: right;
      font-weight: bold;
      cursor: pointer;
    }
  }

  @media (max-width: 480px) {
    #key-measures {
      text-align: center;
      padding: 1em 0.5em;
    }
  }
</style>
