<template>
  <div>
    <h1>Mon tableau de bord</h1>
    <div id="key-measures">
      <div class="measure measure-top">
        <h2>Données d'approvisionnements en produits durables et de qualité</h2>
        <div class="statistics-by-year">
          <div>
            <h3>Sur l'année 2019 :</h3>
            <SummaryStatistics :statistics="statistics['2019']"/>
          </div>
          <div class="separator"></div>
          <div>
            <h3>Sur l'année 2020 :</h3>
            <SummaryStatistics :statistics="statistics['2020']"/>
          </div>
        </div>
        <KeyMeasureResource :baseComponent='qualityMeasure.baseComponent'/>
      </div>
      <div class="measures-bottom">
        <div class="measures-left">
          <div class="measure measure-top-left">
            <h2>Initiatives contre le gaspillage alimentaire</h2>
            <div class="actions">
              <KeyMeasureAction
                :isDone="diagnostics['gaspillage-alimentaire'].hasMadeWastePlan"
                label="Mise en place d'un plan d'actions contre le gaspillage"
              />
              <KeyMeasureAction
                :isDone="diagnostics['gaspillage-alimentaire'].hasCovenant"
                label="Dons aux associations"
              />
            </div>
            <KeyMeasureResource :baseComponent='wasteMeasure.baseComponent'/>
          </div>
          <div class="measure measure-bottom-left">
            <h2>{{ noPlasticMeasure.shortTitle }}</h2>
            <h3>Dans l'établissement, ont été supprimé l'usage des :</h3>
            <div class="actions">
              <KeyMeasureAction
                :isDone="diagnostics['interdiction-du-plastique'].cookingFoodContainersSubstituted"
                label="Contenants de cuisson / de réchauffe en plastique"
              />
              <KeyMeasureAction
                :isDone="diagnostics['interdiction-du-plastique'].serviceFoodContainersSubstituted"
                label="Contenants de service en plastique"
              />
              <KeyMeasureAction
                :isDone="diagnostics['interdiction-du-plastique'].waterBottlesSubstituted"
                label="Bouteilles d'eau en plastique"
              />
              <KeyMeasureAction
                :isDone="diagnostics['interdiction-du-plastique'].disposableUtensilsSubstituted"
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
                :isDone="diagnostics['diversification-des-menus'].hasMadeDiversificationPlan"
                label="Mise en place d'un plan pluriannuel de diversification des protéines"
              />
              <KeyMeasureAction :isDone="hasVegetarianMenu" :label="vegetarianMenuActionLabel"/>
            </div>
            <KeyMeasureResource :baseComponent='diversificationMeasure.baseComponent'/>
          </div>
          <div class="measure measure-bottom-right">
            <h2>{{ informationMeasure.shortTitle }}</h2>
            <div class="actions">
              <KeyMeasureAction
                :isDone="diagnostics['information-des-usagers'].communicationSupport.length > 0"
                label="Communication à disposition des convives sur la qualité des approvisionnements"
              />
              <KeyMeasureAction
                :isDone="diagnostics['information-des-usagers'].communicateOnFoodPlan"
                label="Communication sur le plan alimentaire"
              />
            </div>
            <KeyMeasureResource baseComponent='InformDiners'/>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import { keyMeasures, diagnostics } from '@/data/KeyMeasures.js';
  import SummaryStatistics from '@/components/SummaryStatistics';
  import KeyMeasureResource from '@/components/KeyMeasureResource';
  import KeyMeasureAction from '@/components/KeyMeasureAction';

  export default {
    components: {
      SummaryStatistics,
      KeyMeasureResource,
      KeyMeasureAction,
    },
    data() {
      const quality2019 = diagnostics['qualite-des-produits']['2019'];
      const total2019 = quality2019.valueTotal;

      const quality2020 = diagnostics['qualite-des-produits']['2020'];
      const total2020 = quality2020.valueTotal;

      const vegetarianFrequency = diagnostics['diversification-des-menus'].vegetarianFrequency;
      const hasVegetarianMenu = vegetarianFrequency && vegetarianFrequency !== "less-than-once";

      return {
        keyMeasures,
        qualityMeasure: keyMeasures.find(measure => measure.id === 'qualite-des-produits'),
        wasteMeasure: keyMeasures.find(measure => measure.id === 'gaspillage-alimentaire'),
        diversificationMeasure: keyMeasures.find(measure => measure.id === 'diversification-des-menus'),
        noPlasticMeasure: keyMeasures.find(measure => measure.id === 'interdiction-du-plastique'),
        informationMeasure: keyMeasures.find(measure => measure.id === 'information-des-usagers'),
        diagnostics,
        statistics: {
          '2019': {
            bio: getPercentage(quality2019.valueBio, total2019),
            sustainable: getPercentage(quality2019.valueSustainable, total2019),
            fairTrade: getPercentage(quality2019.valueFairTrade, total2019),
          },
          '2020': {
            bio: getPercentage(quality2020.valueBio, total2020),
            sustainable: getPercentage(quality2020.valueSustainable, total2020),
            fairTrade: getPercentage(quality2020.valueFairTrade, total2020),
          }
        },
        vegetarianFrequency,
        hasVegetarianMenu,
        vegetarianMenuActionLabel: getVegetarianMenuActionLabel(hasVegetarianMenu, vegetarianFrequency),
      };
    },
  };

  function getPercentage(partialValue, totalValue) {
    return !!partialValue && !!totalValue ? Math.round((100 * partialValue) / totalValue) : '--';
  }

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
  h1 {
    font-weight: bold;
    font-size: 48px;
    color: $green;
    margin: 1em 0em;
  }

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

  .actions {
    display: flex;
    flex-direction: column;
    margin-top: 20px;
  }

  .measure-top {
    background-color: $light-orange;

    .statistics-by-year {
      display: flex;
      margin-top: 30px;

      .separator {
        border-left: 3px solid $dark-orange;
        margin: 0 20px;
      }
    }
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
