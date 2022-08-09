<template>
  <div class="text-left">
    <BreadcrumbsNav :title="measure.shortTitle" />
    <h1 class="text-h5 text-xs-h2 font-weight-bold mb-sm-8 mt-4"><KeyMeasureTitle :measure="measure" /></h1>

    <v-row>
      <v-col cols="12" sm="4" md="3">
        <KeyMeasureInfoCard v-if="measure.tags" :measure="measure" :forMeasure="true" />
      </v-col>
      <v-col>
        <KeyMeasureDescription :measure="measure" v-if="measure.description || measure.descriptionComponent" />
        <div v-for="subMeasure in childSubMeasures" :key="subMeasure.id" :id="subMeasure.id">
          <h2 class="text-body-1 font-weight-bold mt-6 mb-2">{{ subMeasure.title }}</h2>
          <div>
            <KeyMeasureInfoCard v-if="subMeasure.tags" :measure="subMeasure" />
            <div>
              <KeyMeasureDescription :measure="subMeasure" />
              <KeyMeasureResource :baseComponent="subMeasure.baseMeasureComponent" />
            </div>
          </div>
        </div>
      </v-col>
    </v-row>

    <v-row v-for="subMeasure in independentSubMeasures" :key="subMeasure.id">
      <v-col cols="12" v-if="subMeasure.title">
        <h2 class="text-body-1 font-weight-bold">{{ subMeasure.title }}</h2>
      </v-col>
      <v-col cols="12" sm="4" md="3">
        <KeyMeasureInfoCard :measure="subMeasure" />
      </v-col>
      <v-col>
        <KeyMeasureDescription :measure="subMeasure" />
        <KeyMeasureResource :baseComponent="subMeasure.baseMeasureComponent" />
      </v-col>
    </v-row>

    <v-row class="px-3">
      <KeyMeasureResource :baseComponent="measure.baseMeasureComponent" />
    </v-row>
  </div>
</template>

<script>
import KeyMeasureDescription from "@/components/KeyMeasureDescription"
import KeyMeasureInfoCard from "@/components/KeyMeasureInfoCard"
import KeyMeasureTitle from "@/components/KeyMeasureTitle"
import KeyMeasureResource from "@/components/KeyMeasureResource"
import BreadcrumbsNav from "@/components/BreadcrumbsNav"

export default {
  components: {
    KeyMeasureDescription,
    KeyMeasureInfoCard,
    KeyMeasureTitle,
    KeyMeasureResource,
    BreadcrumbsNav,
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
