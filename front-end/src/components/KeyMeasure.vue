<template>
  <div class="measure-content">
    <h2><KeyMeasureTitle :measure="measure"/></h2>
    <div class="measure-details">
      <KeyMeasureInfoCard v-if="measure.tags" :measure="measure" :includeCalculatorCard="measure.id === 'qualite-des-produits'"/>
      <div class="description-container">
        <KeyMeasureDescription :measure="measure" v-if="measure.description"/>
        <div v-for="subMeasure in measure.subMeasures" :key="subMeasure.id" :id="subMeasure.id">
          <fieldset class="measure-headline">
            <!-- Wrap legend in span to correctly position with flexbox in Safari -->
            <span><legend>{{subMeasure.title}}</legend></span>
          </fieldset>
          <div class="measure-details">
            <KeyMeasureInfoCard v-if="subMeasure.tags" :measure="subMeasure"/>
            <div>
              <KeyMeasureDescription :measure="subMeasure"/>
              <component :is="subMeasure.baseComponent + 'Resource'" class="resource-block"/>
            </div>
          </div>
        </div>
      </div>
    </div>
    <component :is="measure.baseComponent + 'Resource'" class="resource-block"/>
  </div>
</template>

<script>
  import KeyMeasureDescription from '@/components/KeyMeasureDescription'
  import KeyMeasureInfoCard from '@/components/KeyMeasureInfoCard'
  import KeyMeasureTitle from '@/components/KeyMeasureTitle'
  import tags from '@/data/sector-tags.json'
  import InformDinersResource from "@/components/KeyMeasureResources/InformDiners"
  import QualityMeasureResource from "@/components/KeyMeasureResources/QualityMeasure"
  import SaveLeftoversResource from "@/components/KeyMeasureResources/SaveLeftovers"

  export default {
    components: {
      KeyMeasureDescription,
      KeyMeasureInfoCard,
      KeyMeasureTitle,
      InformDinersResource,
      QualityMeasureResource,
      SaveLeftoversResource
    },
    props: {
      measure: Object,
    },
    data() {
      return {
        tags
      };
    }
  }
</script>

<style scoped lang="scss">
  .measure-content {
    text-align: left;
    margin: 2em;
  }

  h2 {
    font-weight: bold;
    font-size: 32px;
    color: $black;
  }

  .measure-details {
    display: flex;
    align-items: flex-start;
  }

  .description-container {
    flex: 4;
  }

  .measure-headline {
    border: none;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-inline-start: 0;
    margin-inline-end: 0;
    padding-block-start: 0;
    padding-block-end: 0;
    padding-inline-start: 0;
    padding-inline-end: 0;

    legend {
      font-weight: bold;
      font-size: 24px;
      color: $green;
      float: left;
      margin: 1em 0;
      margin-right: 1em;
    }
  }

  .resource-block {
    font-size: 14px;
  }

  @media (max-width: 1000px) {
    .measure-headline {
      flex-direction: column;
      align-items: flex-start;
      margin-bottom: 2em;
    }
  }

  @media (max-width: 650px) {
    .measure-content {
      margin: 0.5em;
    }

    .measure-details {
      flex-direction: column;
      align-items: center;
    }
  }
</style>
