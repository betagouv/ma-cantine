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
  <h2> Quelques ressources pour répondre aux mesures</h2>
  <router-link :to="{ name: 'GeneratePosterPage' }" class="ressource poster" v-if="isIncomplete('convives-informes')">
    <div class="link-icon"><i class="fas fa-bullhorn"></i></div>
    <p>
      L’information convives, par mail et par affichage, de la part de bio,
      durable et commerce équitable est d’ores et déjà en vigueur. Pour générer votre affiche, tester notre formulaire.
    </p>
    <div class="link-icon"><i class="fas fa-arrow-circle-right"></i></div>
  </router-link>
  <a
    href="Diagnostic approvisionnement (ma-cantine-alpha) v0.2.ods"
    class="ressource calculator"
    download
    v-if="isIncomplete('cinquante') || isIncomplete('vingt')"
  >
    <div class="link-icon"><i class="fas fa-calculator"></i></div>
    <p>
      Si vous avez besoin d'aide pour calculer votre part de bios et de produits labélisés,
      vous pouvez tester notre calculateur sous format excel.
    </p>
    <div class="link-icon"><i class="fas fa-file-download"></i></div>
  </a>
  <a
    href="Convention de dons type - restauration collective.pdf"
    class="ressource"
    download
    v-if="isIncomplete('restes')"
  >
    <div class="link-icon"><i class="fas fa-clipboard"></i></div>
    <p>
      Vous voulez éviter le gaspillage ? Télécharger ce modèle type de convention
      aux associations auxquelles faire des dons.
    </p>
    <div class="link-icon"><i class="fas fa-file-download"></i></div>
  </a>
  <a href="https://www.inao.gouv.fr/Espace-professionnel-et-outils/Rechercher-un-produit" class="ressource" target="_blank">
    <div class="link-icon"><i class="fas fa-seedling"></i></div>
    <p>
      Trouver des catégories de produits en recherchant par labels, siqo et/ou régions
      avec le moteur de recherche de l'INAO.
    </p>
    <div class="link-icon"><i class="fas fa-external-link-alt"></i></div>
  </a>
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
  import _ from 'lodash';

  export default {
    components: {
      KeyMeasureTitle,
      KeyMeasureScore,
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
        let measuresHtml = '';
        this.keyMeasures.forEach(measure => {
          measuresHtml += `<p><b>${measure.shortTitle} :</b></p>`;
          measure.subMeasures.forEach(subMeasure => {
            measuresHtml += `<p>${subMeasure.shortTitle} : ${STATUSES[subMeasure.status] || ''}</p>`
          });
        });

        const requestOptions = {
          method: "POST",
          headers: { "Content-Type": "application/json", "api-key": process.env.VUE_APP_SENDINBLUE_API_KEY },
          body: JSON.stringify({
            sender: { email: process.env.VUE_APP_SENDER_EMAIL, name: "site web ma cantine" },
            to: [{ email: process.env.VUE_APP_CONTACT_EMAIL }],
            replyTo: { email: process.env.VUE_APP_CONTACT_EMAIL },
            subject: "Nouveau Béta-testeur ma cantine",
            htmlContent: `<!DOCTYPE html> <html> <body>` +
                         `<p><b>Cantine:</b> ${_.escape(this.form.school)}</p>` +
                         `<p><b>Ville:</b> ${_.escape(this.form.city)}</p>` +
                         `<p><b>Email:</b> ${_.escape(this.form.email)}</p>` +
                         `<p><b>Téléphone:</b> ${_.escape(this.form.phone || '')}</p>` +
                         `<p><b>Message:</b></p>` +
                         `<p>${_.escape(this.form.message || '')}</p>` +
                         `${measuresHtml}` +
                         `</body> </html>`,
          })
        };

        const response = await fetch("https://api.sendinblue.com/v3/smtp/email", requestOptions);

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

  .ressource {
    display: flex;
    width: 90%;
    margin: auto;
    margin-top: 3em;
    align-items: center;
    background: $light-yellow;
    border: 4px solid $yellow;
    box-sizing: border-box;
    text-decoration: none;

    .link-icon {
      font-size: 2em;
      padding: 0.5em;
    }

    .fa-clipboard {
      color: $orange;
    }

    .fa-file-download {
      color: $orange;
    }

    .fa-seedling {
      color: $green;
    }

    .fa-external-link-alt {
      color: $orange;
    }

    p {
      text-align: left;
      color: $dark-orange;
    }
  }

  .ressource.poster {
    background: $light-pink;
    border-color: $pink;

    .fa-bullhorn {
      color: $light-grey;
    }

    .fa-arrow-circle-right {
      color: $pink;
    }

    p {
      color: $pink;
    }
  }

  .ressource.calculator {
    background: $light-blue;
    border-color: $blue;

    .fa-calculator {
      color: $blue;
    }

    .fa-file-download {
      color: $blue;
    }

    p {
      color: $blue;
    }
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
