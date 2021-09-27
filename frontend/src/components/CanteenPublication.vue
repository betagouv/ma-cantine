<template>
  <div class="text-left">
    <div v-if="diagnostic.valueTotalHt && (diagnostic.valueBioHt || diagnostic.valueSustainableHt)">
      <h2 class="font-weight-black text-h6 grey--text text--darken-4 my-4">
        Que mange-t-on dans les assiettes en {{ publicationYear }} ?
      </h2>
      <v-row>
        <v-col cols="12" sm="6" md="4" v-if="diagnostic.valueBioHt">
          <v-card class="fill-height text-center pa-4 d-flex flex-column justify-center" outlined>
            <p class="ma-0">
              <span class="grey--text text-h5 font-weight-black text--darken-2 mr-1">{{ bioPercent }} %</span>
              <span class="caption grey--text text--darken-2">
                bio
              </span>
            </p>
            <div class="mt-2">
              <v-img
                contain
                src="/static/images/quality-labels/logo_bio_eurofeuille.png"
                alt="Logo Agriculture Biologique"
                title="Logo Agriculture Biologique"
                max-height="35"
              />
            </div>
          </v-card>
        </v-col>
        <v-col cols="12" sm="6" md="4" v-if="diagnostic.valueSustainableHt">
          <v-card class="fill-height text-center pa-4 d-flex flex-column justify-center" outlined>
            <p class="ma-0">
              <span class="grey--text text-h5 font-weight-black text--darken-2 mr-1">{{ sustainablePercent }} %</span>
              <span class="caption grey--text text--darken-2">
                durables et de qualité
              </span>
            </p>
            <div class="d-flex mt-2 justify-center">
              <v-img
                contain
                v-for="label in labels"
                :key="label.title"
                :src="`/static/images/quality-labels/${label.src}`"
                :alt="label.title"
                :title="label.title"
                class="px-1"
                max-height="40"
                max-width="40"
              />
            </div>
          </v-card>
        </v-col>
      </v-row>
    </div>

    <h2 class="font-weight-black text-h6 grey--text text--darken-4 mt-8 mb-n4" v-if="Object.keys(earnedBadges).length">
      Nos démarches
    </h2>
    <v-row class="my-6">
      <v-col cols="12" v-for="(badge, key) in earnedBadges" :key="key">
        <v-card class="fill-height" elevation="0">
          <div class="d-flex align-start">
            <v-img width="30" max-width="35" contain :src="`/static/images/badge-${key}-2.png`"></v-img>
            <div>
              <v-card-title class="py-0 text-body-2 font-weight-bold">{{ badge.title }}</v-card-title>
              <v-card-subtitle class="pt-4" v-text="badge.subtitle"></v-card-subtitle>
            </div>
          </div>
        </v-card>
      </v-col>
    </v-row>

    <PublicationComment :comments="canteen && canteen.publicationComments" />
  </div>
</template>

<script>
import PublicationComment from "./PublicationComment.vue"
import badges from "@/badges.json"
import labels from "@/data/quality-labels.json"

function percentage(part, total) {
  return Math.round((part / total) * 100)
}

export default {
  components: {
    PublicationComment,
  },
  props: {
    canteen: Object,
  },
  data() {
    return {
      labels,
      publicationYear: 2020,
    }
  },
  computed: {
    diagnostic() {
      return this.canteen.diagnostics.find((d) => d.year === this.publicationYear)
    },
    bioPercent() {
      return percentage(this.diagnostic.valueBioHt, this.diagnostic.valueTotalHt)
    },
    sustainablePercent() {
      return percentage(this.diagnostic.valueSustainableHt, this.diagnostic.valueTotalHt)
    },
    earnedBadges() {
      let applicable = {}
      const d = this.diagnostic
      if (this.bioPercent >= 20 && this.bioPercent + this.sustainablePercent >= 50) {
        applicable.appro = badges.appro
      }
      if (
        d.hasWasteDiagnostic &&
        d.wasteActions?.length > 0 &&
        (this.canteen.dailyMealCount <= 3000 || d.hasDonationAgreement)
      ) {
        applicable.waste = badges.waste
      }
      if (
        d.cookingPlasticSubstituted &&
        d.servingPlasticSubstituted &&
        d.plasticBottlesSubstituted &&
        d.plasticTablewareSubstituted
      ) {
        applicable.plastic = badges.plastic
      }
      const sectors = this.$store.state.sectors
      const schoolSectorId = sectors.find((x) => x.name === "Scolaire").id
      if (d.vegetarianWeeklyRecurrence === "DAILY") {
        applicable.diversification = badges.diversification
      } else if (this.canteen.sectors.indexOf(schoolSectorId) > -1) {
        if (d.vegetarianWeeklyRecurrence === "MID" || d.vegetarianWeeklyRecurrence === "HIGH") {
          applicable.diversification = badges.diversification
        }
      }
      if (d.communicatesOnFoodQuality) {
        applicable.info = badges.info
      }
      return applicable
    },
  },
}
</script>
