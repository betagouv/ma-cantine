<template>
  <div class="text-left">
    <div
      v-if="
        diagnostic &&
          diagnostic.percentageValueTotalHt &&
          (diagnostic.percentageValueBioHt || diagnostic.percentageValueSustainableHt)
      "
    >
      <h2 class="font-weight-black text-h6 grey--text text--darken-4 my-4">
        Que mange-t-on dans les assiettes en {{ publicationYear }} ?
      </h2>

      <v-card outlined elevation="0" color="primary lighten-5" class="d-flex mb-6" v-if="usesCentralKitchenDiagnostics">
        <v-icon class="ml-4" color="primary">$information-fill</v-icon>

        <v-card-text>
          La cantine « {{ canteen.name }} » sert des repas cuisinés dans une cuisine centrale. Les valeurs ci-dessous
          sont celles du lieu de production des repas.
        </v-card-text>
      </v-card>

      <h3 class="font-weight-black text-body-1 grey--text text--darken-4 my-4">
        Total
      </h3>
      <v-row>
        <v-col cols="12" sm="6" md="4" v-if="toPercentage(diagnostic.percentageValueBioHt)">
          <v-card class="fill-height text-center py-4 d-flex flex-column justify-center" outlined>
            <p class="ma-0">
              <span class="grey--text text-h5 font-weight-black text--darken-2 mr-1">
                {{ toPercentage(diagnostic.percentageValueBioHt) }} %
              </span>
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
        <v-col cols="12" sm="6" md="4" v-if="toPercentage(sustainableTotal)">
          <v-card class="fill-height text-center py-4 d-flex flex-column justify-center" outlined>
            <p class="ma-0">
              <span class="grey--text text-h5 font-weight-black text--darken-2 mr-1">
                {{ toPercentage(sustainableTotal) }} %
              </span>
              <span class="caption grey--text text--darken-2">
                durables et de qualité (hors bio)
              </span>
            </p>
            <div class="d-flex mt-2 justify-center flex-wrap">
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
      <div v-if="diagnostic.diagnosticType === 'COMPLETE'">
        <h3 class="font-weight-black text-body-1 grey--text text--darken-4 mt-4">
          Catégories EGAlim par famille de produit
        </h3>
        <FamiliesGraph :diagnostic="diagnostic" :height="$vuetify.breakpoint.xs ? '440px' : '380px'" />
      </div>
      <div v-else>
        <h3 class="font-weight-black text-body-1 grey--text text--darken-4 mb-4 mt-8">
          Par famille de produit
        </h3>
        <v-row>
          <v-col cols="12" sm="4" md="4" v-if="toPercentage(diagnostic.percentageValueMeatPoultryEgalimHt)">
            <v-card class="fill-height text-center py-4 d-flex flex-column justify-center" outlined>
              <p class="ma-0">
                <span class="grey--text text-h5 font-weight-black text--darken-2 mr-1">
                  {{ toPercentage(diagnostic.percentageValueMeatPoultryEgalimHt) }} %
                </span>
                <span class="caption grey--text text--darken-2">
                  viandes et volailles EGAlim
                </span>
              </p>
              <div class="mt-2">
                <v-icon size="30" color="brown">
                  mdi-food-steak
                </v-icon>
                <v-icon size="30" color="brown">
                  mdi-food-drumstick
                </v-icon>
                <v-icon size="30" color="green">
                  $checkbox-circle-fill
                </v-icon>
              </div>
            </v-card>
          </v-col>
          <v-col cols="12" sm="4" md="4" v-if="toPercentage(diagnostic.percentageValueMeatPoultryFranceHt)">
            <v-card class="fill-height text-center py-4 d-flex flex-column justify-center" outlined>
              <p class="ma-0">
                <span class="grey--text text-h5 font-weight-black text--darken-2 mr-1">
                  {{ toPercentage(diagnostic.percentageValueMeatPoultryFranceHt) }} %
                </span>
                <span class="caption grey--text text--darken-2">
                  viandes et volailles provenance France
                </span>
              </p>
              <div class="mt-2">
                <v-icon size="30" color="brown">
                  mdi-food-steak
                </v-icon>
                <v-icon size="30" color="brown">
                  mdi-food-drumstick
                </v-icon>
                <v-icon size="30" color="indigo">
                  $france-line
                </v-icon>
              </div>
            </v-card>
          </v-col>
          <v-col cols="12" sm="4" md="4" v-if="toPercentage(diagnostic.percentageValueFishEgalimHt)">
            <v-card class="fill-height text-center py-4 d-flex flex-column justify-center" outlined>
              <p class="ma-0">
                <span class="grey--text text-h5 font-weight-black text--darken-2 mr-1">
                  {{ toPercentage(diagnostic.percentageValueFishEgalimHt) }} %
                </span>
                <span class="caption grey--text text--darken-2">
                  produits aquatiques EGAlim
                </span>
              </p>
              <div class="mt-2">
                <v-icon size="30" color="blue">
                  mdi-fish
                </v-icon>
                <v-icon size="30" color="green">
                  $checkbox-circle-fill
                </v-icon>
              </div>
            </v-card>
          </v-col>
        </v-row>
      </div>
    </div>

    <h2 class="font-weight-black text-h6 grey--text text--darken-4 mt-8 mb-n4" v-if="Object.keys(earnedBadges).length">
      Nos démarches
    </h2>
    <v-row class="my-6">
      <div v-for="(badge, key) in earnedBadges" :key="key">
        <v-col cols="12" v-if="badge.earned">
          <v-card class="fill-height" elevation="0">
            <div class="d-flex align-start">
              <v-img width="40" max-width="40" contain :src="`/static/images/badges/${key}.svg`" alt=""></v-img>
              <div>
                <v-card-title class="py-0 text-body-2 font-weight-bold">{{ badge.title }}</v-card-title>
                <v-card-subtitle
                  class="pt-4"
                  v-text="badge.subtitle"
                  v-if="key !== 'appro' || applicableRules.qualityThreshold === 50"
                ></v-card-subtitle>
                <div v-else>
                  <v-card-subtitle class="pt-0">
                    Ce qui est servi dans les assiettes est au moins à {{ applicableRules.qualityThreshold }} % de
                    produits durables et de qualité, dont {{ applicableRules.bioThreshold }} % bio, en respectant
                    <a href="https://ma-cantine.agriculture.gouv.fr/blog/16">les seuils d'Outre-mer</a>
                  </v-card-subtitle>
                </div>
              </div>
            </div>
          </v-card>
        </v-col>
      </div>
    </v-row>

    <div v-if="canteen && canteen.publicationComments">
      <h2 class="font-weight-black text-h6 grey--text text--darken-4 mb-2">
        Un petit mot du gestionnaire
      </h2>
      <p class="body-2">
        {{ canteen.publicationComments }}
      </p>
    </div>

    <div v-if="canteen && shouldDisplayGraph">
      <h2 class="font-weight-black text-h6 grey--text text--darken-4 mt-12 mb-2">
        Évolution des produits dans nos assiettes sur les années
      </h2>
      <div>
        <MultiYearSummaryStatistics
          :diagnostics="graphDiagnostics"
          headingId="appro-heading"
          height="260"
          :width="$vuetify.breakpoint.mdAndUp ? '650px' : '100%'"
          :applicableRules="applicableRules"
        />
      </div>
    </div>

    <div v-if="diagnostic && diagnostic.communicationSupportUrl">
      <h2 class="font-weight-black text-h6 grey--text text--darken-4 mt-8 mb-2">
        Information des usagers et des convives
      </h2>
      <p class="body-2">
        Cette cantine communique aux usagers sur
        <a :href="diagnostic.communicationSupportUrl">{{ diagnostic.communicationSupportUrl }}</a>
        .
      </p>
    </div>

    <div v-if="canteen && canteen.images && canteen.images.length > 0">
      <h2 class="font-weight-black text-h6 grey--text text--darken-4 mt-8 mb-0">
        Galerie
      </h2>
      <p class="body-2">
        Cliquez sur une image pour l'agrandir
      </p>
      <div>
        <ImageGallery :images="canteen.images" />
      </div>
    </div>
  </div>
</template>

<script>
import labels from "@/data/quality-labels.json"
import {
  lastYear,
  badges,
  hasDiagnosticApproData,
  latestCreatedDiagnostic,
  applicableDiagnosticRules,
  getSustainableTotal,
} from "@/utils"
import MultiYearSummaryStatistics from "@/components/MultiYearSummaryStatistics"
import FamiliesGraph from "@/components/FamiliesGraph"
import ImageGallery from "@/components/ImageGallery"

export default {
  props: {
    canteen: Object,
  },
  data() {
    return {
      labels,
    }
  },
  components: { MultiYearSummaryStatistics, ImageGallery, FamiliesGraph },
  computed: {
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
    usesCentralKitchenDiagnostics() {
      return (
        this.canteen?.productionType === "site_cooked_elsewhere" && this.canteen?.centralKitchenDiagnostics?.length > 0
      )
    },
    publicationYear() {
      return this.diagnostic?.year
    },
    sustainableTotal() {
      return getSustainableTotal(this.diagnostic)
    },
    earnedBadges() {
      const canteenBadges = badges(this.canteen, this.diagnostic, this.$store.state.sectors)
      let earnedBadges = {}
      Object.keys(canteenBadges).forEach((key) => {
        if (canteenBadges[key].earned) earnedBadges[key] = canteenBadges[key]
      })
      return earnedBadges
    },
    shouldDisplayGraph() {
      if (!this.diagnosticSet || this.diagnosticSet.length === 0) return false
      const completedDiagnostics = this.diagnosticSet.filter(hasDiagnosticApproData)
      if (completedDiagnostics.length === 0) return false
      else if (completedDiagnostics.length === 1) return completedDiagnostics[0].year !== lastYear()
      else return true
    },
    graphDiagnostics() {
      if (!this.diagnosticSet || this.diagnosticSet.length === 0) return null
      const diagnostics = {}
      for (let i = 0; i < this.diagnosticSet.length; i++) {
        const diagnostic = this.diagnosticSet[i]
        diagnostics[diagnostic.year] = diagnostic
      }
      return diagnostics
    },
    applicableRules() {
      return applicableDiagnosticRules(this.canteen)
    },
  },
  methods: {
    toPercentage(value) {
      return Math.round(value * 100)
    },
  },
}
</script>
