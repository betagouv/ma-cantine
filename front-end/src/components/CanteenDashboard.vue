<template>
  <div id="key-measures">
    <div class="measure measure-top">
      <h2>Données d'approvisionnements en produits durables et de qualité</h2>
      <div class="statistics-by-year">
        <div class="statistics-for-year">
          <h3>Sur l'année 2019 :</h3>
          <SummaryStatistics :qualityDiagnostic="previousDiagnostic"/>
        </div>
        <div class="separator"></div>
        <div class="statistics-for-year">
          <h3>Sur l'année 2020 :</h3>
          <SummaryStatistics :qualityDiagnostic="latestDiagnostic"/>
        </div>
      </div>
      <KeyMeasureResource :baseComponent='qualityMeasure.baseComponent' v-if="showResources"/>
    </div>
    <div class="measures-bottom">
      <div class="measures-left">
        <div class="measure measure-top-left">
          <h2>Initiatives contre le gaspillage alimentaire</h2>
          <div class="actions">
            <KeyMeasureAction
              :isDone="latestDiagnostic.hasMadeWasteDiagnostic"
              label="Réalisation d'un diagnostic sur le gaspillage alimenataire"
            />
            <KeyMeasureAction
              :isDone="latestDiagnostic.hasMadeWastePlan"
              label="Mise en place d'un plan d'actions contre le gaspillage"
            />
            <ul class="specifics-actions">
              <li v-for="action in latestDiagnostic.wasteActions" :key="action">
                - {{wasteActions[action]}}
              </li>
            </ul>
            <KeyMeasureAction
              :isDone="latestDiagnostic.hasDonationAgreement"
              label="Dons aux associations"
            />
          </div>
          <KeyMeasureResource :baseComponent='wasteMeasure.baseComponent' v-if="showResources"/>
        </div>
        <div class="measure measure-bottom-left">
          <h2>{{ noPlasticMeasure.shortTitle }}</h2>
          <h3>Dans l'établissement, ont été supprimé l'usage des :</h3>
          <div class="actions">
            <KeyMeasureAction
              :isDone="latestDiagnostic.cookingFoodContainersSubstituted"
              label="Contenants de cuisson / de réchauffe en plastique"
            />
            <KeyMeasureAction
              :isDone="latestDiagnostic.serviceFoodContainersSubstituted"
              label="Contenants de service en plastique"
            />
            <KeyMeasureAction
              :isDone="latestDiagnostic.waterBottlesSubstituted"
              label="Bouteilles d'eau en plastique"
            />
            <KeyMeasureAction
              :isDone="latestDiagnostic.disposableUtensilsSubstituted"
              label="Ustensiles à usage unique en plastique"
            />
          </div>
        </div>
      </div>
      <div class="measures-right">
        <div class="measure measure-top-right">
          <h2>{{ diversificationMeasure.shortTitle }}</h2>
          <div class="actions">
            <KeyMeasureAction
              :isDone="latestDiagnostic.hasMadeDiversificationPlan"
              label="Mise en place d'un plan pluriannuel de diversification des protéines"
            />
            <KeyMeasureAction :isDone="hasVegetarianMenu" :label="vegetarianMenuActionLabel"/>
          </div>
          <KeyMeasureResource :baseComponent='diversificationMeasure.baseComponent' v-if="showResources"/>
        </div>
        <div class="measure measure-bottom-right">
          <h2>{{ informationMeasure.shortTitle }}</h2>
          <div class="actions">
            <KeyMeasureAction
              :isDone="latestDiagnostic.communicateOnFoodPlan"
              label="Communication sur le plan alimentaire"
            />
            <KeyMeasureAction
              :isDone="latestDiagnostic.communicationSupports.length > 0"
              label="Communication à disposition des convives sur la qualité des approvisionnements"
            />
            <ul class="specifics-actions">
              <li v-for="action in latestDiagnostic.communicationSupports" :key="action">
                - {{communicationSupports[action]}}
              </li>
            </ul>
            <a
              v-if="latestDiagnostic.communicationSupportLink"
              :href="prepareHref(latestDiagnostic.communicationSupportLink)"
              class="communication-support-link"
              target="_blank"
            >
              Lien vers le support de communication <i class="fas fa-external-link-alt"></i>
            </a>
          </div>
          <KeyMeasureResource baseComponent='InformDiners' v-if="showResources"/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import { keyMeasures } from '@/data/KeyMeasures.js';
  import wasteActions from '@/data/waste-actions.json';
  import communicationSupports from '@/data/communication-supports.json';
  import SummaryStatistics from '@/components/SummaryStatistics';
  import KeyMeasureResource from '@/components/KeyMeasureResource';
  import KeyMeasureAction from '@/components/KeyMeasureAction';

  export default {
    components: {
      SummaryStatistics,
      KeyMeasureResource,
      KeyMeasureAction,
    },
    props: {
      diagnostics: Object,
      showResources: Boolean,
    },
    data() {
      const latestDiagnostic = this.diagnostics.latest;
      const vegetarianFrequency = latestDiagnostic.vegetarianFrequency;
      const hasVegetarianMenu = vegetarianFrequency && vegetarianFrequency !== "less-than-once";

      return {
        latestDiagnostic,
        previousDiagnostic: this.diagnostics.previous,
        wasteActions,
        communicationSupports,
        qualityMeasure: keyMeasures.find(measure => measure.id === 'qualite-des-produits'),
        wasteMeasure: keyMeasures.find(measure => measure.id === 'gaspillage-alimentaire'),
        diversificationMeasure: keyMeasures.find(measure => measure.id === 'diversification-des-menus'),
        noPlasticMeasure: keyMeasures.find(measure => measure.id === 'interdiction-du-plastique'),
        informationMeasure: keyMeasures.find(measure => measure.id === 'information-des-usagers'),
        vegetarianFrequency,
        hasVegetarianMenu,
        vegetarianMenuActionLabel: getVegetarianMenuActionLabel(hasVegetarianMenu, vegetarianFrequency),
      };
    },
    methods: {
      prepareHref(link) {
        return link.startsWith('http') ? link : '//' + link;
      }
    }
  };

  function getVegetarianMenuActionLabel(hasVegetarianMenu, vegetarianFrequency) {
    if (!hasVegetarianMenu) {
      return "Pas de menu végétarien";
    } else if (vegetarianFrequency === 'once') {
      return "Mise en place d'un menu végétarien";
    } else if (vegetarianFrequency === 'moreThanOnce') {
      return "Plusieurs menus végétariens";
    }
  }
</script>

<style scoped lang="scss">
  #key-measures {
    text-align: left;

    h2 {
      margin: 0;
      color: $dark-grey;
    }
  }

  .measure {
    padding: 30px;
    border-radius: 20px;
    margin-top: 20px;
  }

  .measure-top {
    background-color: $light-orange;
  }

  .measures-bottom {
    display: flex;
  }

  .measures-left {
    margin-right: 20px;
    display: flex;
    flex-direction: column;
    flex: 1;
  }

  .measures-right {
    display: flex;
    flex-direction: column;
    flex: 1;
  }

  .measure-top-left {
    background-color: $light-yellow;
    flex: 1;
  }

  .measure-bottom-left {
    background-color: $light-blue;
    flex: 1;
  }

  .measure-top-right {
    background-color: $light-green;
    flex: 1;
  }

  .measure-bottom-right {
    background-color: $light-pink;
    flex: 1;
  }

  .actions {
    display: flex;
    flex-direction: column;
    margin-top: 20px;
  }

  .specifics-actions {
    padding-left: 20px;
    margin-top: -5px;
  }

  .statistics-by-year {
    display: flex;
    margin-top: 30px;

    .statistics-for-year {
      flex: 1;
    }

    .separator {
      border-left: 3px solid $dark-orange;
      margin: 0 20px;
    }
  }

  .communication-support-link {
    color: $dark-grey;
  }

  @media (max-width: 750px) {
    .measure-top {
      .statistics-by-year {
        display: block;

        .separator {
          border-left: none;
          border-bottom: 3px solid $dark-orange;
          margin: 20px;
        }
      }
    }

    .measures-bottom {
      display: block;
    }
  }
</style>
