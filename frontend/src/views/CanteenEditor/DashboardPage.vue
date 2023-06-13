<template>
  <div>
    <h1 class="text-h4 font-weight-black my-6">Où en sommes nous sur les mesures de la loi ?</h1>

    <CanteenDashboard
      :diagnostics="diagnostics"
      :showResources="true"
      :canteen="originalCanteen"
      :singleColumn="true"
    />

    <div class="text-left mt-10">
      <h2>Où sont les autres cantines comme celle-ci ?</h2>
      <p>Pour les cantines dans le département {{ department }}{{ sectorSpecifierText }} :</p>
      <div v-if="!diagnosticsLoading">
        <v-row class="mt-10 mb-2 px-3 align-center">
          <h3 class="text-h6 font-weight-bold">Qualité de produits en {{ year }}</h3>
        </v-row>
        <div v-if="statistics.diagnosticsCount === 0">
          <p class="mt-8 caption">
            Aucune cantine n'a renseigné des données relatives à la loi EGAlim pour l'année {{ year }}.
          </p>
        </div>
        <div v-else>
          <p class="mb-8">Parmi les {{ statistics.diagnosticsCount }} cantines qui ont commencé un diagnostic&nbsp;:</p>
          <v-row class="px-2">
            <v-col class="pl-0 pr-1" cols="12" sm="6" md="4">
              <v-card class="fill-height text-center pt-4 pb-2 px-3 d-flex flex-column" outlined>
                <v-img max-width="30" contain src="/static/images/badges/appro.svg" class="mx-auto" alt=""></v-img>
                <v-card-text class="grey--text text--darken-2 px-1">
                  <span class="text-h5 font-weight-black" style="line-height: inherit;">
                    {{ statistics.approPercent }} %
                  </span>
                  <span class="text-body-2">
                    ont réussi l'objectif d'approvisionnement EGAlim
                  </span>
                </v-card-text>
                <v-card-actions class="px-1">
                  <router-link :to="{ name: 'KeyMeasurePage', params: { id: approMeasure.id } }" class="text-body-2">
                    La mesure
                  </router-link>
                </v-card-actions>
              </v-card>
            </v-col>
            <v-col class="px-1" cols="12" sm="6" md="3">
              <v-card class="fill-height text-center py-4 d-flex flex-column justify-center" outlined>
                <v-card-text>
                  <span class="text-h5 font-weight-black">{{ statistics.bioPercent }} %</span>
                  <span class="text-body-2">
                    bio moyen
                  </span>
                </v-card-text>
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
            <v-col class="pl-1 pr-0" cols="12" sm="6" md="5">
              <v-card class="fill-height text-center py-4 d-flex flex-column justify-center" outlined>
                <v-card-text>
                  <span class="text-h5 font-weight-black">{{ statistics.sustainablePercent }} %</span>
                  <span class="text-body-2">
                    durables et de qualité (hors bio) moyen
                  </span>
                </v-card-text>
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
          <h3 class="text-h6 font-weight-bold mt-10 mb-2">
            Ces cantines ont aussi réalisé les mesures suivantes en {{ year }}
          </h3>
          <p class="mb-8">
            Parmi les mêmes {{ statistics.diagnosticsCount }} cantines qui ont commencé un diagnostic&nbsp;:
          </p>
          <v-row class="my-8">
            <v-col cols="12" sm="6" md="5" v-for="measure in otherMeasures" :key="measure.id" class="mb-4">
              <BadgeCard :measure="measure" :percentageAchieved="statistics[measure.badgeId + 'Percent']" />
            </v-col>
          </v-row>
        </div>
      </div>
      <v-row v-else justify="center" class="py-15">
        <v-progress-circular indeterminate></v-progress-circular>
      </v-row>
      <!-- two links : one to nos cantines pre-filtered and one to stats page pre-filtered -->
    </div>
  </div>
</template>

<script>
import keyMeasures from "@/data/key-measures.json"
import labels from "@/data/quality-labels.json"
import { lastYear } from "@/utils"
import Constants from "@/constants"
import CanteenDashboard from "@/components/CanteenDashboard"
import BadgeCard from "@/views/PublicCanteenStatisticsPage/BadgeCard"

export default {
  components: {
    CanteenDashboard,
    BadgeCard,
  },
  props: ["diagnostics", "originalCanteen"],
  data() {
    return {
      year: lastYear(),
      statistics: {},
      diagnosticsLoading: false,
      approMeasure: keyMeasures.find((measure) => measure.badgeId === "appro"),
      otherMeasures: keyMeasures.filter((measure) => measure.badgeId !== "appro"),
      labels,
    }
  },
  computed: {
    regionalQueryString() {
      let query = `year=${this.year}`
      if (this.department) {
        query += `&department=${this.department}`
      }
      if (this.searchSectors.length) {
        query += `&sectors=${this.searchSectors.join("&sectors=")}`
      }
      return query
    },
    department() {
      return this.originalCanteen.department
    },
    allSectors() {
      return this.$store.state.sectors
    },
    canteenSectorCategories() {
      const canteenSectors = this.originalCanteen.sectors.map((sectorId) =>
        this.allSectors.find((s) => s.id === sectorId)
      )
      const categories = canteenSectors.map((s) => s.category)
      const uniqueCategories = categories.filter((c, idx, self) => c && self.indexOf(c) === idx)
      return uniqueCategories
    },
    searchSectors() {
      return this.allSectors
        .filter((sector) => this.canteenSectorCategories.includes(sector.category))
        .map((sector) => sector.id)
    },
    sectorSpecifierText() {
      if (this.searchSectors.length === 0) return ""
      let string = " et "
      if (this.canteenSectorCategories.length === 1) {
        string += "la catégorie de secteur"
      } else {
        string += "les catégories de secteur"
      }
      const categoriesDisplayString = this.canteenSectorCategories
        .map((c) => Constants.SectorCategoryTranslations[c])
        .join(", ")
      string += " " + categoriesDisplayString
      return string
    },
  },
  methods: {
    loadStatistics() {
      this.diagnosticsLoading = true
      fetch(`/api/v1/canteenStatistics/?${this.regionalQueryString}`)
        .then((response) => response.json())
        .then((data) => {
          this.statistics = data
          this.diagnosticsLoading = false
        })
    },
  },
  created() {
    document.title = `Améliorer - ${this.originalCanteen.name} - ${this.$store.state.pageTitleSuffix}`
  },
  mounted() {
    this.loadStatistics()
  },
}
</script>
