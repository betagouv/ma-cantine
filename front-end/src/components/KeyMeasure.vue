<template>
  <div class="measure-content">
    <h2><KeyMeasureTitle :measure="measure"/></h2>
    <div class="measure-details">
      <KeyMeasureInfoCard v-if="measure.tags" :measure="measure" :includeCalculatorCard="measure.id === 'qualite-durable'"/>
      <div class="description-container">
        <KeyMeasureDescription :measure="measure" v-if="measure.description"/>
        <div v-for="subMeasure in measure.subMeasures" :key="subMeasure.id" :id="subMeasure.id">
          <h3>{{subMeasure.title}}</h3>
          <div class="measure-details">
            <KeyMeasureInfoCard v-if="subMeasure.tags" :measure="subMeasure"/>
            <KeyMeasureDescription :measure="subMeasure"/>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import KeyMeasureDescription from '@/components/KeyMeasureDescription'
  import KeyMeasureInfoCard from '@/components/KeyMeasureInfoCard'
  import KeyMeasureTitle from '@/components/KeyMeasureTitle'
  import tags from '@/data/sector-tags.json'

  export default {
    components: {
      KeyMeasureDescription,
      KeyMeasureInfoCard,
      KeyMeasureTitle
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

  h3 {
    font-weight: bold;
    font-size: 24px;
    color: $green;
  }

  @media (max-width: 480px) {
    .measure-content {
      margin: 0.5em;
    }

    .measure-details {
      flex-direction: column;
      align-items: center;
    }
  }
</style>
