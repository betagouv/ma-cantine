<template>
  <div class="text-left">
    <KeyMeasureTitle :measure="measure" class="text-h5 text-sm-h4 font-weight-bold mb-8 mt-4" />

    <v-row>
      <v-col cols="12" sm="4" md="3">
        <KeyMeasureInfoCard v-if="measure.tags" :measure="measure" />
      </v-col>
      <v-col>
        <KeyMeasureDescription :measure="measure" v-if="measure.description" />
        <div v-for="subMeasure in childSubMeasures" :key="subMeasure.id" :id="subMeasure.id">
          <div class="text-body-1 font-weight-bold mt-6 mb-2">{{ subMeasure.title }}</div>
          <div class="measure-details">
            <KeyMeasureInfoCard v-if="subMeasure.tags" :measure="subMeasure" />
            <div>
              <KeyMeasureDescription :measure="subMeasure" />
              <KeyMeasureResource :baseComponent="subMeasure.baseMeasureComponent" class="resource-block" />
            </div>
          </div>
        </div>
      </v-col>
    </v-row>

    <v-row v-for="subMeasure in independentSubMeasures" :key="subMeasure.id">
      <v-col cols="12" v-if="subMeasure.title" class="text-body-1 font-weight-bold">
        {{ subMeasure.title }}
      </v-col>
      <v-col cols="12" sm="4" md="3">
        <KeyMeasureInfoCard :measure="subMeasure" />
      </v-col>
      <v-col>
        <KeyMeasureDescription :measure="subMeasure" />
        <KeyMeasureResource :baseComponent="subMeasure.baseMeasureComponent" class="resource-block" />
      </v-col>
    </v-row>

    <v-row>
      <KeyMeasureResource :baseComponent="measure.baseMeasureComponent" class="resource-block" />
    </v-row>
  </div>
</template>

<script>
import KeyMeasureDescription from "@/components/KeyMeasureDescription"
import KeyMeasureInfoCard from "@/components/KeyMeasureInfoCard"
import KeyMeasureTitle from "@/components/KeyMeasureTitle"
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
  computed: {
    independentSubMeasures() {
      return this.measure.subMeasures.filter((x) => !!x.tags && x.tags.length > 0)
    },
    childSubMeasures() {
      return this.measure.subMeasures.filter((x) => !x.tags || x.tags.length === 0)
    },
  },
}
</script>
