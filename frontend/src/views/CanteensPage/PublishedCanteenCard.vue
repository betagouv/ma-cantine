<template>
  <v-card
    :to="{ name: 'CanteenPage', params: { canteenUrlComponent: $store.getters.getCanteenUrlComponent(canteen) } }"
    outlined
    class="my-4 text-left d-flex flex-column dsfr canteen-card"
  >
    <v-row class="pa-0 ma-0">
      <v-col cols="4" class="pa-0 card-image-wrap" v-if="!dense">
        <img
          :src="canteen.leadImage ? canteen.leadImage.image : '/static/images/canteen-default-image.jpg'"
          class="lead-image"
        />
      </v-col>
      <v-col class="pa-8 d-flex flex-column justify-space-between">
        <div>
          <h2 class="fr-h5 mb-1 primary--text">
            {{ canteen.name }}
          </h2>
          <ProductionTypeTag :canteen="canteen" :position="!dense ? 'top-left' : ''" />
          <CanteenIndicators :useCategories="true" :canteen="canteen" :singleLine="true" :dense="true" class="my-2" />
        </div>
        <p v-if="year" class="my-2 fr-text-sm">
          En {{ year }} :
          <span class="ma-0" v-if="hasPercentages">
            <span class="ma-0 mr-3" v-if="bioPercent">
              <span class="font-weight-black mr-1">{{ bioPercent }} %</span>
              bio
            </span>
            <span class="ma-0" v-if="sustainablePercent">
              <span class="font-weight-black mr-1">{{ sustainablePercent }} %</span>
              de qualité et durables
            </span>
          </span>
        </p>
        <div v-if="year" class="d-flex my-2">
          <img
            v-for="badge in orderedBadges"
            :key="badge.key"
            :src="`/static/images/badges/${badge.key}${badgeIsEarned(badge) ? '' : '-disabled'}.svg`"
            :width="dense ? '35px' : '50px'"
            :height="dense ? '35px' : '50px'"
            :class="dense ? 'mr-2' : 'mr-4'"
            :alt="badgeTitle(badge)"
            :title="badgeTitle(badge)"
          />
        </div>
        <p v-else class="my-2 fr-text-sm">Pas de données renseignées</p>
        <v-card-actions class="px-4 py-0">
          <v-spacer></v-spacer>
          <v-icon color="primary">$arrow-right-line</v-icon>
        </v-card-actions>
      </v-col>
    </v-row>
  </v-card>
</template>

<script>
import CanteenIndicators from "@/components/CanteenIndicators"
import ProductionTypeTag from "@/components/ProductionTypeTag"
import { getSustainableTotal, toPercentage } from "@/utils"
import badges from "@/badges"

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
    ProductionTypeTag,
  },
  computed: {
    year() {
      return this.canteen.badges.year
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
    approDiagnostic() {
      return this.canteen?.approDiagnostic
    },
    bioPercent() {
      return toPercentage(this.approDiagnostic?.percentageValueBioHt)
    },
    sustainablePercent() {
      if (!this.approDiagnostic) return
      return toPercentage(getSustainableTotal(this.approDiagnostic))
    },
    hasPercentages() {
      return this.bioPercent || this.sustainablePercent
    },
    dense() {
      return this.$vuetify.breakpoint.xs
    },
  },
  methods: {
    badgeTitle(badge) {
      return `${badge.title}${this.badgeIsEarned(badge) ? "" : " (à faire)"}`
    },
    badgeIsEarned(badge) {
      return this.canteen?.badges[badge.key]
    },
  },
}
</script>

<style scoped>
.canteen-card {
  min-height: 256px;
}
.canteen-card img.lead-image {
  opacity: 50%;
  max-height: 100%;
  max-width: 100%;
  height: 100%;
  width: 100%;
  object-fit: cover;
  position: absolute;
}
.canteen-card:hover img.lead-image,
.canteen-card:focus img.lead-image {
  opacity: 100%;
}
.card-image-wrap {
  position: relative;
}
</style>
