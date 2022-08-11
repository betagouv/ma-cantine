<template>
  <v-card
    :to="{ name: 'CanteenPage', params: { canteenUrlComponent: $store.getters.getCanteenUrlComponent(canteen) } }"
    outlined
    class="pa-4 text-left fill-height d-flex flex-column dsfr"
  >
    <v-card-title class="font-weight-black pt-1">
      {{ canteen.name }}
    </v-card-title>
    <v-card-subtitle v-if="canteen.dailyMealCount || canteen.city" class="pb-4">
      <CanteenIndicators :canteen="canteen" :singleLine="true" />
    </v-card-subtitle>
    <v-spacer></v-spacer>
    <v-divider class="py-1"></v-divider>
    <div class="grey--text text--darken-2" :style="$vuetify.breakpoint.smAndDown ? '' : 'height: 95px;'">
      <v-card-text class="py-1 fill-height d-flex flex-column" v-if="diagnostic">
        <span>En {{ year }} :</span>
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
        <v-spacer v-else></v-spacer>
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
      <div v-else class="d-flex flex-column fill-height">
        <v-spacer></v-spacer>
        <v-card-text class="py-1">Pas de données renseignées</v-card-text>
        <v-spacer></v-spacer>
      </div>
    </div>
    <v-card-actions class="px-4 py-0">
      <v-spacer></v-spacer>
      <v-icon color="primary">mdi-arrow-right</v-icon>
    </v-card-actions>
  </v-card>
</template>

<script>
import CanteenIndicators from "@/components/CanteenIndicators"
import { getPercentage, getSustainableTotal, hasDiagnosticApproData, badges, latestCreatedDiagnostic } from "@/utils"

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
    const diagnostic = latestCreatedDiagnostic(this.canteen)
    return {
      diagnostic,
      year: diagnostic?.year,
    }
  },
  computed: {
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
      if (this.diagnostic && hasDiagnosticApproData(this.diagnostic))
        return getPercentage(getSustainableTotal(this.diagnostic), this.diagnostic.valueTotalHt)
      return null
    },
    hasPercentages() {
      return this.bioPercent || this.sustainablePercent
    },
  },
  methods: {
    diagValuePercent(valueKey) {
      if (!this.diagnostic || !hasDiagnosticApproData(this.diagnostic)) return null
      return getPercentage(this.diagnostic[valueKey], this.diagnostic.valueTotalHt)
    },
    badgeTitle(badge) {
      return `${badge.title}${badge.earned ? "" : " (à faire)"}`
    },
  },
}
</script>
