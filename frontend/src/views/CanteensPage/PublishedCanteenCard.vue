<template>
  <div>
    <v-card outlined class="text-left d-flex flex-column dsfr expanded-link canteen-card">
      <v-row class="pa-0 ma-0">
        <v-col cols="4" class="pa-0 card-image-wrap" v-if="showImage">
          <img
            :src="canteen.leadImage ? canteen.leadImage.image : '/static/images/canteen-default-image.jpg'"
            class="lead-image"
            alt=""
          />
        </v-col>
        <v-col class="pa-8 d-flex flex-column justify-space-between">
          <div>
            <h3 class="fr-h5 mb-1">
              <router-link
                :to="{
                  name: 'CanteenPage',
                  params: { canteenUrlComponent: $store.getters.getCanteenUrlComponent(canteen) },
                }"
              >
                {{ canteen.name }}
              </router-link>
            </h3>
            <ProductionTypeTag :canteen="canteen" :position="showImage ? 'top-left' : ''" />
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
  </div>
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
    noImage: {
      type: Boolean,
      default: false,
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
      return toPercentage(this.approDiagnostic?.percentageValueBio)
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
    showImage() {
      return !this.dense && !this.noImage
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
  height: 100%;
}
.canteen-card img.lead-image {
  opacity: 0.5;
  max-height: 100%;
  max-width: 100%;
  height: 100%;
  width: 100%;
  object-fit: cover;
  position: absolute;
}
.canteen-card:hover img.lead-image,
.canteen-card:focus-within img.lead-image {
  opacity: 1;
}
.card-image-wrap {
  position: relative;
}
</style>
