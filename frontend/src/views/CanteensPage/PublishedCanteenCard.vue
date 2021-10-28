<template>
  <v-card
    :to="{ name: 'CanteenPage', params: { canteenUrlComponent: $store.getters.getCanteenUrlComponent(canteen) } }"
    hover
    class="pa-4 text-left fill-height d-flex flex-column"
  >
    <v-card-title class="font-weight-black pt-1">
      {{ canteen.name }}
    </v-card-title>
    <v-card-subtitle v-if="canteen.dailyMealCount || canteen.city" class="pb-4">
      <CanteenIndicators :canteen="canteen" :singleLine="true" />
    </v-card-subtitle>
    <v-spacer></v-spacer>
    <v-divider class="pb-2"></v-divider>
    <v-spacer></v-spacer>
    <div class="grey--text text--darken-2">
      <v-card-text class="py-1" v-if="diagnostic">
        <v-row class="ma-0" v-if="hasPercentages">
          <p class="ma-0 mr-3" v-if="bioPercent">
            <span class="font-weight-black mr-1">{{ bioPercent }} %</span>
            <span>bio</span>
          </p>
          <p class="ma-0" v-if="sustainablePercent">
            <span class="font-weight-black mr-1">{{ sustainablePercent }} %</span>
            <span>de qualité et durables</span>
          </p>
        </v-row>
        <v-row class="ma-0 pt-3">
          <v-img
            max-width="30"
            contain
            :src="`/static/images/badges/${badge.key}${badge.earned ? '' : '-disabled'}.svg`"
            v-for="badge in orderedBadges"
            :key="badge.key"
            class="mr-2"
            :alt="badgeTitle(badge)"
            :title="badgeTitle(badge)"
          ></v-img>
        </v-row>
      </v-card-text>
      <v-card-text class="py-1" v-else>Pas de données renseignées pour {{ publicationYear }}</v-card-text>
    </div>
  </v-card>
</template>

<script>
import CanteenIndicators from "@/components/CanteenIndicators"
import { lastYear, getPercentage, isDiagnosticComplete, badges } from "@/utils"

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
    canteenBadges() {
      return badges(this.canteen, this.diagnostic, this.$store.state.sectors)
    },
    approBadge() {
      return this.canteenBadges.appro
    },
    orderedBadges() {
      return Object.keys(this.canteenBadges)
        .map((key) => {
          return { ...{ key }, ...this.canteenBadges[key] }
        })
        .sort((a, b) => {
          if (a.earned === b.earned) return 0
          return a.earned && !b.earned ? -1 : 1
        })
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
    badgeTitle(badge) {
      return `${badge.title}${badge.earned ? "" : " (à faire)"}`
    },
  },
}
</script>
