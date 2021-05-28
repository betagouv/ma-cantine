<template>
  <div class="measure-content">
    <h1><KeyMeasureTitle :measure="measure" /></h1>
    <div class="measure-details">
      <KeyMeasureInfoCard v-if="measure.tags" :measure="measure" />
      <div class="description-container">
        <KeyMeasureDescription :measure="measure" v-if="measure.description" />
        <div v-for="subMeasure in measure.subMeasures" :key="subMeasure.id" :id="subMeasure.id">
          <h2 class="measure-headline">{{ subMeasure.title }}</h2>
          <div class="measure-details">
            <KeyMeasureInfoCard v-if="subMeasure.tags" :measure="subMeasure" />
            <div>
              <KeyMeasureDescription :measure="subMeasure" />
              <KeyMeasureResource :baseComponent="subMeasure.baseComponent" class="resource-block" />
            </div>
          </div>
        </div>
      </div>
    </div>
    <KeyMeasureResource :baseComponent="measure.baseComponent" class="resource-block" />
  </div>
</template>

<script>
import KeyMeasureDescription from "@/components/KeyMeasureDescription"
import KeyMeasureInfoCard from "@/components/KeyMeasureInfoCard"
import KeyMeasureTitle from "@/components/KeyMeasureTitle"
import tags from "@/data/sector-tags.json"
import KeyMeasureResource from "@/components/KeyMeasureResource"

export default {
  components: {
    KeyMeasureDescription,
    KeyMeasureInfoCard,
    KeyMeasureTitle,
    KeyMeasureResource,
  },
  props: {
    measure: Object,
  },
  data() {
    return {
      tags,
    }
  },
}
</script>

<style scoped lang="scss">
.measure-content {
  text-align: left;
  margin: 2em;
}

h1 {
  font-weight: bold;
  font-size: 32px;
  color: $ma-cantine-black;
}

.measure-details {
  display: flex;
  align-items: flex-start;
}

.description-container {
  flex: 4;
}

.measure-headline {
  font-weight: bold;
  font-size: 24px;
  color: $ma-cantine-green;
  margin: 1em 0;
  margin-right: 1em;
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
