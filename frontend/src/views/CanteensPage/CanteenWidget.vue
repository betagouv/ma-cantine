<template>
  <div class="text-left" v-if="canteen">
    <h1 class="text-h4 font-weight-black mb-1 mt-0">
      {{ canteen.name }}
    </h1>
    <CanteenIndicators :canteen="canteen" :singleLine="true" class="grey--text text--darken-3 caption" />
    <div class="my-6">
      <p class="text-body-1">
        <span class="font-weight-black">{{ bioPercent }} %</span>
        bio,
        <span class="font-weight-black">{{ sustainablePercent }} %</span>
        de qualité et durable
      </p>

      <v-card class="my-2">
        <v-tabs v-model="selectedBadgeKey">
          <v-tab v-for="badge in orderedBadges" :key="badge.key" max-width="30">
            <v-img
              max-width="30"
              contain
              :src="`/static/images/badges/${badge.key}${badge.earned ? '' : '-disabled'}.svg`"
              class="mx-4"
              :alt="badgeTitle(badge)"
              :title="badgeTitle(badge)"
            ></v-img>
          </v-tab>
        </v-tabs>
        <v-tabs-items v-model="selectedBadgeKey">
          <v-tab-item v-for="badge in orderedBadges" :key="badge.key">
            <v-card flat outlined>
              <v-card-title
                class="text-body-2 font-weight-bold px-2"
                :class="!badge.earned && 'grey--text text--darken-2'"
              >
                {{ badgeTitle(badge) }}
              </v-card-title>
              <v-card-subtitle
                class="text-body-2 px-2"
                :class="!badge.earned && 'grey--text text--darken-2'"
                v-text="badge.subtitle"
                v-if="badge.key !== 'appro' || applicableRules.qualityThreshold === 50"
              ></v-card-subtitle>
              <v-card-subtitle v-else class="text-body-2 px-2" :class="!badge.earned && 'grey--text text--darken-2'">
                Ce qui est servi dans les assiettes est au moins à {{ applicableRules.qualityThreshold }} % de produits
                durables et de qualité, dont {{ applicableRules.bioThreshold }} % bio, en respectant
                <a href="https://ma-cantine.agriculture.gouv.fr/blog/16" target="_blank">
                  les seuils d'Outre-mer
                  <v-icon small class="primary--text">mdi-open-in-new</v-icon>
                </a>
              </v-card-subtitle>
            </v-card>
          </v-tab-item>
        </v-tabs-items>
      </v-card>
    </div>
    <v-btn color="primary" class="mt-2" target="_blank" :href="link">
      Voir sur la plateforme
      <v-icon small class="ml-1">mdi-open-in-new</v-icon>
    </v-btn>
  </div>
</template>

<script>
import CanteenIndicators from "@/components/CanteenIndicators"
import labels from "@/data/quality-labels.json"
import { badges, latestCreatedDiagnostic, applicableDiagnosticRules, getSustainableTotal } from "@/utils"

export default {
  data() {
    return {
      canteen: undefined,
      labels,
      claimSucceeded: false,
      selectedBadgeKey: undefined,
    }
  },
  components: {
    CanteenIndicators,
  },
  props: {
    canteenUrlComponent: {
      type: String,
      required: true,
    },
  },
  computed: {
    link() {
      const l = document.location
      const prefixLength = "/widgets".length
      return `${l.origin}${l.pathname.slice(prefixLength)}?mtm_campaign=widget-cantine`
    },
    diagnosticSet() {
      if (!this.canteen) return
      if (!this.usesCentralKitchenDiagnostics) return this.canteen.diagnostics

      // Since the central kitchen might only handle the appro values, we will merge the diagnostics
      // from the central and satellites when necessary to show the whole picture
      return this.canteen.centralKitchenDiagnostics.map((centralDiag) => {
        const satelliteMatchingDiag = this.canteen.diagnostics.find((x) => x.year === centralDiag.year)
        if (centralDiag.centralKitchenDiagnosticMode === "APPRO" && satelliteMatchingDiag)
          return Object.assign(satelliteMatchingDiag, centralDiag)
        return centralDiag
      })
    },
    diagnostic() {
      if (!this.diagnosticSet) return
      return latestCreatedDiagnostic(this.diagnosticSet)
    },
    year() {
      return this.diagnostic?.year
    },
    bioPercent() {
      return Math.round(this.diagnostic.percentageValueBioHt * 100)
    },
    sustainablePercent() {
      return Math.round(getSustainableTotal(this.diagnostic) * 100)
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
    selectedBadge() {
      return this.canteenBadges[this.selectedBadgeKey]
    },
    applicableRules() {
      return applicableDiagnosticRules(this.canteen)
    },
  },
  methods: {
    setCanteen(canteen) {
      this.canteen = canteen
    },
    badgeTitle(badge) {
      return `${badge.title}${badge.earned ? "" : " (à faire)"}`
    },
  },
  beforeMount() {
    const previousIdVersion = this.canteenUrlComponent.indexOf("--") === -1
    const id = previousIdVersion ? this.canteenUrlComponent : this.canteenUrlComponent.split("--")[0]
    return fetch(`/api/v1/publishedCanteens/${id}`)
      .then((response) => {
        if (response.status != 200) throw new Error()
        response.json().then(this.setCanteen)
      })
      .catch(() => {
        this.$router.push({ name: "NotFound" })
      })
  },
  mounted() {
    if (this.$matomo) {
      const eventCategory = "iframe"
      const eventAction = "view"
      const eventName = "iframe-published-canteen"
      this.$matomo.trackEvent(eventCategory, eventAction, eventName)
    }
  },
  watch: {
    orderedBadges(badges) {
      this.selectedBadgeKey = badges[0].key
    },
  },
}
</script>

<style lang="scss" scoped>
.v-tab {
  min-width: 30px;
  max-width: 50px;
}
.v-tabs-slider-wrapper {
  width: 50px !important;
}
</style>
