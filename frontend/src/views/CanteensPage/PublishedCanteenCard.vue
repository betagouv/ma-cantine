<template>
  <v-card
    :to="{ name: 'CanteenPage', params: { canteenUrlComponent: $store.getters.getCanteenUrlComponent(canteen) } }"
    outlined
    class="pa-4 text-left fill-height d-flex flex-column dsfr"
  >
    <v-card-title class="pt-1">
      <h2 class="fr-h6 mb-1 font-weight-black">
        {{ canteen.name }}
      </h2>
    </v-card-title>
    <v-card-subtitle class="pb-4">
      <CanteenIndicators :useCategories="true" :canteen="canteen" :singleLine="true" />
      <div v-if="isCentralKitchen" class="tag body-2 font-weight-medium mt-2">
        <p class="d-flex align-center mb-0">
          <v-icon class="mr-1" small>$community-fill</v-icon>
          Cuisine centrale
        </p>
      </div>
    </v-card-subtitle>
    <v-spacer></v-spacer>
    <v-divider aria-hidden="true" role="presentation" class="py-1"></v-divider>
    <div class="grey--text text--darken-2" :style="$vuetify.breakpoint.smAndDown ? '' : 'height: 95px;'">
      <v-card-text class="py-1 fill-height d-flex flex-column" v-if="year">
        <p class="mb-0">En {{ year }} :</p>
        <v-row class="ma-0" v-if="hasPercentages">
          <p class="ma-0 mr-3" v-if="bioPercent">
            <span class="font-weight-black mr-1">{{ bioPercent }} %</span>
            bio
          </p>
          <p class="ma-0" v-if="sustainablePercent">
            <span class="font-weight-black mr-1">{{ sustainablePercent }} %</span>
            de qualité et durables
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
        <v-card-text class="py-1"><p class="mb-0">Pas de données renseignées</p></v-card-text>
        <v-spacer></v-spacer>
      </div>
    </div>
    <v-card-actions class="px-4 py-0">
      <v-spacer></v-spacer>
      <v-icon color="primary">$arrow-right-line</v-icon>
    </v-card-actions>
  </v-card>
</template>

<script>
import CanteenIndicators from "@/components/CanteenIndicators"
import { getSustainableTotal, badges } from "@/utils"

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
  computed: {
    year() {
      return this.canteen.latestYear
    },
    canteenBadges() {
      return badges(this.canteen)
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
    approDiagnostic() {
      if (!this.canteen.approDiagnostics) return
      return this.canteen.approDiagnostics.find((d) => d.year == this.year)
    },
    bioPercent() {
      if (!this.approDiagnostic) return
      return Math.round(this.approDiagnostic.percentageValueBioHt * 100)
    },
    sustainablePercent() {
      if (!this.approDiagnostic) return
      return Math.round(getSustainableTotal(this.approDiagnostic) * 100)
    },
    hasPercentages() {
      return this.bioPercent || this.sustainablePercent
    },
    isCentralKitchen() {
      return this.canteen.productionType === "central" || this.canteen.productionType === "central_serving"
    },
  },
  methods: {
    badgeTitle(badge) {
      return `${badge.title}${badge.earned ? "" : " (à faire)"}`
    },
  },
}
</script>

<style scoped>
.tag {
  background: #e0e0f2;
  left: 10px;
  padding: 3px 10px;
  border-radius: 4px;
  color: #333;
  display: inline-block;
}
</style>
