<template>
  <v-card
    :to="{ name: 'CanteenPage', params: { canteenUrlComponent: $store.getters.getCanteenUrlComponent(canteen) } }"
    hover
    class="pa-4 text-left fill-height"
  >
    <v-card-title class="font-weight-black">
      {{ canteen.name }}
    </v-card-title>
    <v-card-subtitle v-if="canteen.dailyMealCount || canteen.city" class="pb-2">
      <CanteenIndicators :canteen="canteen" />
    </v-card-subtitle>
    <v-card-text v-if="hasBadges || hasPercentages" class="grey--text text--darken-4">
      <v-row class="ma-0 pb-2" v-if="hasBadges">
        <v-img
          max-width="25"
          contain
          :src="`/static/images/badge-${key}.svg`"
          v-for="(badge, key) in earnedBadges"
          :key="key"
          class="mr-2"
          :alt="badge.title"
          :title="badge.title"
        ></v-img>
      </v-row>
      <v-row class="ma-0" v-if="hasPercentages">
        <p class="ma-0 mr-4" v-if="bioPercent">
          <span class="grey--text text-h5 font-weight-black text--darken-2 mr-1">{{ bioPercent }} %</span>
          <span class="caption grey--text text--darken-2">
            bio
          </span>
        </p>
        <p class="ma-0" v-if="sustainablePercent">
          <span class="grey--text text-h5 font-weight-black text--darken-2 mr-1">{{ sustainablePercent }} %</span>
          <span class="caption grey--text text--darken-2">
            durables et de qualité
          </span>
        </p>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script>
import CanteenIndicators from "@/components/CanteenIndicators"
import { lastYear, getPercentage, isDiagnosticComplete, earnedBadges } from "@/utils"

export default {
  name: "PublishedCanteenCard",
  props: {
    canteen: {
      type: Object,
      required: true,
    },
  },
  components: {
    CanteenIndicators,
  },
  data() {
    return {
      publicationYear: lastYear(),
    }
  },
  computed: {
    diagnostic() {
      return this.canteen.diagnostics.find((d) => d.year === this.publicationYear)
    },
    earnedBadges() {
      if (this.diagnostic) {
        return earnedBadges(this.canteen, this.diagnostic, this.$store.state.sectors)
      } else {
        return {}
      }
    },
    hasBadges() {
      return Object.keys(this.earnedBadges).length
    },
    bioPercent() {
      return this.diagValuePercent("valueBioHt")
    },
    sustainablePercent() {
      return this.diagValuePercent("valueSustainableHt")
    },
    hasPercentages() {
      return this.bioPercent || this.sustainablePercent
    },
  },
  methods: {
    diagValuePercent(valueKey) {
      if (!this.diagnostic || !isDiagnosticComplete(this.diagnostic)) return null
      return getPercentage(this.diagnostic[valueKey], this.diagnostic.valueTotalHt)
    },
  },
}
</script>
