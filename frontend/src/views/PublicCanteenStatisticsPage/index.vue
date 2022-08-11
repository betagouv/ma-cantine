<template>
  <div class="text-left grey--text text--darken-4">
    <BreadcrumbsNav :links="[{ to: { name: 'CanteensHome' } }]" />
    <h1 class="text-h4 font-weight-black black--text mb-6">Découvrir les démarches chez vous</h1>

    <v-card outlined>
      <v-card-text>
        <v-form class="my-4">
          <v-row>
            <v-col class="py-0" cols="12" sm="6" md="4">
              <label for="select-region" class="text-body-2">
                Région
              </label>
              <v-autocomplete
                v-model="chosenRegion"
                :items="regions"
                clearable
                hide-details
                id="select-region"
                placeholder="Toutes les régions"
                class="mt-1"
                outlined
                dense
                auto-select-first
                :filter="locationFilter"
                no-data-text="Pas de résultats"
              ></v-autocomplete>
            </v-col>
            <v-col class="py-2 py-sm-0" cols="12" sm="6" md="4">
              <label for="select-department" class="text-body-2">
                Département
              </label>
              <v-autocomplete
                v-model="chosenDepartment"
                :items="departments"
                clearable
                hide-details
                id="select-department"
                placeholder="Tous les départements"
                class="mt-1"
                outlined
                dense
                auto-select-first
                :filter="locationFilter"
                no-data-text="Pas de résultats"
              ></v-autocomplete>
            </v-col>
            <v-col class="py-2 py-sm-0" cols="12" sm="6" md="4">
              <label for="select-sector" class="text-body-2">
                Secteur d'activité
              </label>
              <v-select
                v-model="chosenSectors"
                multiple
                :items="sectorsList"
                item-text="name"
                item-value="id"
                clearable
                hide-details
                id="select-sector"
                placeholder="Tous les secteurs"
                outlined
                class="mt-1"
                dense
              ></v-select>
            </v-col>
          </v-row>
          <v-row class="mt-8">
            <v-col cols="12" sm="6" md="4">
              <v-btn x-large color="primary" @click="updateRoute">
                Afficher les statistiques
              </v-btn>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
    </v-card>
    <div v-if="locationText" class="py-8">
      <h2 class="text-h5 font-weight-bold">Les statistiques pour {{ locationText }}</h2>
      <p v-if="sectorsText" class="text-body-2 mt-4 grey--text text--darken-2">
        <v-icon aria-hidden="false" role="img" aria-label="Secteurs">mdi-office-building</v-icon>
        {{ sectorsText }}
      </p>
      <v-row :class="{ 'flex-column': $vuetify.breakpoint.smAndDown, 'mt-8': true }">
        <v-col cols="12" md="6" class="pr-0">
          <div id="published-canteen-text" class="mb-5">
            <p class="mb-0">
              Au total, nous avons
              <span class="text-h5 font-weight-bold">{{ statistics.canteenCount }}</span>
              cantine{{ statistics.canteenCount == 1 ? "" : "s" }} sur {{ statsLevelDisplay }}.
            </p>
            <p>
              <span class="text-h5 font-weight-bold">{{ statistics.publishedCanteenCount }}</span>
              cantine{{
                statistics.publishedCanteenCount == 1
                  ? " a publié ses données (répertoriée dans"
                  : "s ont publié leurs données (répertoriées dans"
              }}
              <!-- eslint-disable-next-line prettier/prettier-->
              <router-link :to="{ name: 'CanteensHome' }">nos cantines</router-link>).
            </p>
          </div>
          <VueApexCharts
            :options="publishedChartOptions"
            :series="publishedSeries"
            type="pie"
            height="auto"
            v-if="$vuetify.breakpoint.mdAndUp"
            width="62%"
            role="img"
            aria-describedby="published-canteen-text"
          />
        </v-col>
        <v-col cols="12" sm="8" md="6" class="pl-0">
          <VueApexCharts
            :options="sectorChartOptions"
            :series="sectorSeries"
            type="bar"
            height="auto"
            width="100%"
            role="img"
            :aria-label="sectorChartTitle"
            aria-describedby="sector-chart-description"
          />
          <p id="sector-chart-description" class="d-none">{{ sectorChartDescription }}</p>
        </v-col>
      </v-row>
      <h3 class="text-h6 font-weight-bold mt-10 mb-8">Qualité de produits en {{ year }}</h3>
      <v-row class="px-2">
        <v-col class="pl-0 pr-1" cols="12" sm="6" md="5">
          <v-card class="fill-height text-center pt-4 pb-2 px-3 d-flex flex-column" outlined>
            <v-img max-width="30" contain src="/static/images/badges/appro.svg" class="mx-auto" alt=""></v-img>
            <v-card-text class="grey--text text--darken-2 px-1">
              <span class="text-h5 font-weight-black" style="line-height: inherit;">
                {{ statistics.approPercent }} %
              </span>
              <span class="text-body-2">
                ont réalisé la mesure
                <span class="font-weight-black">« {{ approMeasure.shortTitle.toLowerCase() }} »</span>
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
        <v-col class="pl-1 pr-0" cols="12" sm="6" md="4">
          <v-card class="fill-height text-center py-4 d-flex flex-column justify-center" outlined>
            <v-card-text>
              <span class="text-h5 font-weight-black">{{ statistics.sustainablePercent }} %</span>
              <span class="text-body-2">
                durables et de qualité moyen
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
      <h3 class="text-h6 font-weight-bold mt-10 mb-8">
        Ces cantines ont aussi réalisé les mesures suivantes en {{ year }}
      </h3>
      <v-row class="justify-space-between mt-8 mb-8 px-2">
        <BadgeCard
          v-for="measure in otherMeasures"
          :key="measure.id"
          :measure="measure"
          :percentageAchieved="statistics[measure.badgeId + 'Percent']"
          class="mb-4"
        />
      </v-row>
    </div>
    <v-row v-else justify="center" class="py-15">
      <v-progress-circular indeterminate></v-progress-circular>
    </v-row>
  </div>
</template>

<script>
import BadgeCard from "./BadgeCard"
import VueApexCharts from "vue-apexcharts"
import labels from "@/data/quality-labels.json"
import keyMeasures from "@/data/key-measures.json"
import jsonDepartments from "@/departments.json"
import jsonRegions from "@/regions.json"
import { lastYear, normaliseText, sectorsSelectList } from "@/utils"
import BreadcrumbsNav from "@/components/BreadcrumbsNav"

export default {
  name: "PublicCanteenStatisticsPage",
  components: {
    BadgeCard,
    VueApexCharts,
    BreadcrumbsNav,
  },
  data() {
    return {
      year: lastYear(),
      labels,
      approMeasure: keyMeasures.find((measure) => measure.badgeId === "appro"),
      otherMeasures: keyMeasures.filter((measure) => measure.badgeId !== "appro"),
      chosenDepartment: null,
      chosenRegion: null,
      chosenSectors: [],
      locationText: null,
      statistics: {},
      publishedChartOptions: {
        labels: ["Publiée", "Non publiée"],
        colors: ["#55a57e", "#ccc"],
        dataLabels: {
          dropShadow: false,
          style: {
            colors: ["#333"],
            fontSize: "14px",
          },
          offsetX: 30,
        },
      },
      loadedDepartmentIds: [],
      loadedRegionIds: [],
      sectorChartTitle: "Nombre de cantines par secteur",
      defaultLocationText: "l'ensemble de la plateforme",
      statsLevel: "site",
    }
  },
  mounted() {
    this.populateInitialParameters()
    this.loadLocations()
    this.updateStatistics()
  },
  computed: {
    departments() {
      let enabledDepartments = this.loadedDepartmentIds
      let departmentsForRegion = jsonDepartments
      if (this.chosenRegion) {
        departmentsForRegion = jsonDepartments.filter((department) => department.regionCode === this.chosenRegion)
      }
      return this.formatLocations(enabledDepartments, departmentsForRegion, "department", "départements")
    },
    regions() {
      return this.formatLocations(this.loadedRegionIds, jsonRegions, "region", "régions")
    },
    publishedSeries() {
      return [
        this.statistics.publishedCanteenCount,
        this.statistics.canteenCount - this.statistics.publishedCanteenCount,
      ]
    },
    sectors() {
      return this.$store.state.sectors
    },
    sectorsList() {
      return sectorsSelectList(this.sectors)
    },
    sectorLabels() {
      return this.sectors.map((sector) => sector.name)
    },
    sectorSeries() {
      return [
        {
          data: this.sectors.map((sector) => this.statistics.sectors[sector.id.toString()]),
          color: "#55a57e",
          name: "Nombre de cantines",
        },
      ]
    },
    sectorChartOptions() {
      return {
        title: {
          text: this.sectorChartTitle,
          style: {
            fontSize: "14px",
            fontWeight: "normal",
            fontFamily: "Marianne",
            color: "#333",
          },
          offsetX: this.$vuetify.breakpoint.mdAndUp ? 162 : 10,
          offsetY: -5,
          floating: true,
        },
        dataLabels: {
          style: {
            colors: ["#000"],
          },
        },
        chart: {
          type: "bar",
          toolbar: { tools: { download: false } },
          animations: { enabled: false },
        },
        xaxis: {
          categories: this.sectorLabels,
          labels: {
            trim: true,
          },
        },
        plotOptions: {
          bar: {
            horizontal: true,
          },
        },
        legend: {
          show: false,
        },
      }
    },
    sectorChartDescription() {
      let desc = ""
      Object.keys(this.statistics.sectors).forEach((key) => {
        desc += `${this.sectors.find((sector) => sector.id.toString() === key).name}, ${this.statistics.sectors[key]}; `
      })
      return desc
    },
    statsLevelDisplay() {
      return { department: "ce département", region: "cette région", site: "ce site" }[this.statsLevel]
    },
    chosenRegionName() {
      return this.chosenRegion
        ? jsonRegions.find((region) => region.regionCode === this.chosenRegion).regionName || this.chosenRegion
        : null
    },
    sectorsText() {
      let sectorsText = ""
      if (this.$route.query.sectors) {
        const sectors = this.$route.query.sectors
          .split(",")
          .map((sectorId) => {
            return this.sectors.find((x) => x.id === parseInt(sectorId, 10))?.name
          })
          .filter((name) => !!name)
        sectorsText += sectors.join(", ")
      }
      return sectorsText
    },
  },
  methods: {
    loadLocations() {
      fetch(`/api/v1/canteenLocations/`)
        .then((response) => response.json())
        .then((data) => {
          this.loadedRegionIds = data.regions
          this.loadedDepartmentIds = data.departments
        })
    },
    loadStatistics(newLocationText, query) {
      fetch(`/api/v1/canteenStatistics/?${query}`)
        .then((response) => response.json())
        .then((data) => {
          this.statistics = data
          this.locationText = newLocationText
        })
    },
    // this was derived from 'setLocations' in the CanteensHome page, if used again consider a util
    formatLocations(enabledLocationIds, jsonLocations, locationKeyWord, locationsWord) {
      const enabledLocations = jsonLocations
        .filter((x) => enabledLocationIds.indexOf(x[`${locationKeyWord}Code`]) > -1)
        .map((x) => ({
          text: `${x[`${locationKeyWord}Code`]} - ${x[`${locationKeyWord}Name`]}`,
          value: x[`${locationKeyWord}Code`],
        }))

      let headerText =
        this.chosenRegion && locationKeyWord == "department"
          ? `Pour la région « ${this.chosenRegionName} », nous `
          : "Nous "
      headerText += `n'avons pas encore d'établissements dans ces ${locationsWord} :`
      const header = { header: headerText }
      const divider = { divider: true }

      const disabledLocations = jsonLocations
        .filter((x) => enabledLocationIds.indexOf(x[`${locationKeyWord}Code`]) === -1)
        .map((x) => ({
          text: `${x[`${locationKeyWord}Code`]} - ${x[`${locationKeyWord}Name`]}`,
          value: x[`${locationKeyWord}Code`],
          disabled: true,
        }))

      return disabledLocations.length ? [...enabledLocations, divider, header, ...disabledLocations] : enabledLocations
    },
    // taken from the CanteensHome page, if used again consider a util
    locationFilter(item, queryText, itemText) {
      return (
        Object.prototype.hasOwnProperty.call(item, "divider") ||
        Object.prototype.hasOwnProperty.call(item, "header") ||
        normaliseText(itemText).indexOf(normaliseText(queryText)) > -1
      )
    },
    createLocationText() {
      let locationText
      if (this.chosenDepartment) {
        locationText = `« ${
          jsonDepartments.find((department) => department.departmentCode === this.chosenDepartment).departmentName
        } »`
      } else if (this.chosenRegion) {
        locationText = `« ${this.chosenRegionName} »`
      } else {
        locationText = this.defaultLocationText
      }
      return locationText
    },
    updateStatistics() {
      let query = `year=${this.year}`
      this.locationText = ""
      if (this.chosenDepartment) {
        query += `&department=${this.chosenDepartment}`
        this.statsLevel = "department"
      } else if (this.chosenRegion) {
        query += `&region=${this.chosenRegion}`
        this.statsLevel = "region"
      } else {
        this.statsLevel = "site"
      }
      if (this.chosenSectors.length) {
        query += `&sectors=${this.chosenSectors.join("&sectors=")}`
      }
      let newLocationText = this.createLocationText()
      this.loadStatistics(newLocationText, query)
      this.updateRoute()
    },
    updateRoute() {
      let query = {}
      if (this.chosenDepartment) {
        query.department = this.chosenDepartment
      }
      if (this.chosenRegion) {
        query.region = this.chosenRegion
      }
      if (this.chosenSectors.length) {
        query.sectors = this.chosenSectors.join(",")
      }
      // The empty catch is the suggested error management here : https://github.com/vuejs/vue-router/issues/2872#issuecomment-519073998
      this.$router
        .push({ query })
        .then(() => this.updateDocumentTitle())
        .catch(() => {})
    },
    populateInitialParameters() {
      this.chosenDepartment = this.$route.query.department
      this.chosenRegion = this.$route.query.region
      this.chosenSectors = this.$route.query.sectors?.split(",").map((s) => parseInt(s, 10)) || []
    },
    updateDocumentTitle() {
      let title = `Les statistiques dans ma collectivité - ${this.$store.state.pageTitleSuffix}`
      if (this.chosenRegion || this.chosenDepartment) title = `${this.createLocationText()} - ${title}`
      document.title = title
    },
  },
  watch: {
    chosenRegion(newRegion) {
      if (newRegion && this.chosenDepartment) {
        let depInfo = jsonDepartments.find((department) => department.departmentCode === this.chosenDepartment)
        if (depInfo.regionCode !== newRegion) {
          this.chosenDepartment = null
        }
      }
    },
    $route() {
      this.populateInitialParameters()
      this.updateStatistics()
      this.updateDocumentTitle()
    },
  },
}
</script>
