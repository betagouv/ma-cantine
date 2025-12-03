<template>
  <div class="text-left" v-if="canteen">
    <h1 class="text-h4 font-weight-black mb-1 mt-0">
      {{ canteen.name }}
    </h1>
    <CanteenIndicators :canteen="canteen" :singleLine="true" class="grey--text text--darken-3 caption" />
    <div class="my-6">
      <p v-if="hasPercentages" class="text-body-1">
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
              :src="`/static/images/badges/${badge.key}${badgeIsEarned(badge) ? '' : '-disabled'}.svg`"
              class="mx-4"
              :alt="badgeTitle(badge)"
              :title="badgeTitle(badge)"
            ></v-img>
          </v-tab>
        </v-tabs>
        <v-tabs-items v-model="selectedBadgeKey">
          <v-tab-item v-for="badge in orderedBadges" :key="badge.key">
            <v-card flat outlined>
              <v-card-title :class="!badgeIsEarned(badge) && 'grey--text text--darken-2'">
                <h2 class="text-body-2 font-weight-bold mb-1">
                  {{ badgeTitle(badge) }}
                </h2>
              </v-card-title>
              <v-card-subtitle
                :class="!badgeIsEarned(badge) && 'grey--text text--darken-2'"
                v-if="badge.key !== 'appro' || applicableRules.qualityThreshold === 50"
              >
                <p class="text-body-2 mb-0">{{ badge.subtitle }}</p>
              </v-card-subtitle>
              <v-card-subtitle v-else :class="!badgeIsEarned(badge) && 'grey--text text--darken-2'">
                <p class="text-body-2 mb-0">
                  Ce qui est servi dans les assiettes est au moins à {{ applicableRules.qualityThreshold }} % de
                  produits durables et de qualité, dont {{ applicableRules.bioThreshold }} % bio, en respectant
                  <a
                    href="https://ma-cantine.agriculture.gouv.fr/blog/16"
                    target="_blank"
                    title="les différents seuils fixés pour l'Outre-mer - ouvre une nouvelle fenêtre"
                  >
                    les différents seuils fixés pour l'Outre-mer
                    <v-icon small class="primary--text">mdi-open-in-new</v-icon>
                  </a>
                </p>
              </v-card-subtitle>
            </v-card>
          </v-tab-item>
        </v-tabs-items>
      </v-card>
    </div>
    <v-btn
      color="primary"
      class="mt-2"
      target="_blank"
      :href="link"
      title="Voir sur la plateforme - ouvre une nouvelle fenêtre"
    >
      Voir sur la plateforme
      <v-icon small class="ml-1">mdi-open-in-new</v-icon>
    </v-btn>
  </div>
</template>

<script>
import CanteenIndicators from "@/components/CanteenIndicators"
import labels from "@/data/quality-labels.json"
import { applicableDiagnosticRules, getSustainableTotal, toPercentage } from "@/utils"
import badges from "@/badges"

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
    year() {
      return this.canteen?.badges.year
    },
    approDiagnostic() {
      return this.canteen?.approDiagnostic
    },
    bioPercent() {
      return toPercentage(this.approDiagnostic?.percentageValueBio)
    },
    sustainablePercent() {
      if (!this.approDiagnostic) return
      return toPercentage(getSustainableTotal(this.approDiagnostic))
    },
    hasPercentages() {
      return this.bioPercent || this.sustainablePercent
    },
    canteenBadges() {
      return this.canteen?.badges
    },
    orderedBadges() {
      return Object.values(badges).sort((a, b) => {
        const aIsEarned = this.badgeIsEarned(a)
        const bIsEarned = this.badgeIsEarned(b)
        if (aIsEarned === bIsEarned) return 0
        return aIsEarned && !bIsEarned ? -1 : 1
      })
    },
    selectedBadge() {
      return badges[this.selectedBadgeKey]
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
      return `${badge.title}${this.badgeIsEarned(badge) ? "" : " (à faire)"}`
    },
    badgeIsEarned(badge) {
      return this.canteen?.badges[badge.key]
    },
  },
  beforeMount() {
    const previousIdVersion = this.canteenUrlComponent.indexOf("--") === -1
    const id = previousIdVersion ? this.canteenUrlComponent : this.canteenUrlComponent.split("--")[0]
    return fetch(`/api/v1/publicCanteenPreviews/${id}`)
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
