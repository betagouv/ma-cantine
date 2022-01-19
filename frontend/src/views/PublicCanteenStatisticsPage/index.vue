<template>
  <div class="text-left grey--text text--darken-4">
    <h1 class="text-h4 font-weight-black black--text mt-3 mb-6">Découvrir les démarches chez vous</h1>
    <!-- Add some introductory text? -->
    <v-form class="my-4 pb-8">
      <v-row>
        <v-col cols="12" sm="6" md="4">
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
          ></v-autocomplete>
        </v-col>
        <v-col cols="12" sm="6" md="4">
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
          ></v-autocomplete>
        </v-col>
        <v-col cols="12" sm="6" md="4" class="d-flex align-end">
          <v-btn x-large color="primary" @click="submit">
            <!-- More descriptive text? -->
            Rechercher
          </v-btn>
        </v-col>
      </v-row>
    </v-form>
    <div v-if="locationText" class="py-8">
      <h2 class="text--darken-5 text-h4 mb-8">Les statistiques pour {{ locationText }}</h2>
      <v-row :class="{ 'flex-column': $vuetify.breakpoint.smAndDown }">
        <v-col cols="12" md="6" class="pr-0">
          <div id="published-canteen-text" class="mb-5">
            <p>
              Aujourd'hui, il y a
              <span class="text-h5 font-weight-bold">{{ statistics.canteenCount }}</span>
              cantine{{ statistics.canteenCount == 1 ? "" : "s" }} dans {{ locationText }} sur ce site.
            </p>
            <p>
              <span class="text-h5 font-weight-bold">{{ statistics.publishedCanteenCount }}</span>
              cantine{{ statistics.publishedCanteenCount == 1 ? " a publié ses" : "s ont publié leurs" }} données,
              accessible par
              <router-link :to="{ name: 'CanteensHome' }">nos cantines</router-link>
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
      <h3 class="text-h5 mt-10 mb-8 text--darken-5">Qualité de produits en {{ year }}</h3>
      <v-row>
        <v-col cols="12" sm="6" md="5">
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
                <!-- TODO: more specific link text? -->
                La mesure
              </router-link>
            </v-card-actions>
          </v-card>
        </v-col>
        <!-- TODO: this was copied from CanteenPublication. Consider making a component -->
        <v-col cols="12" sm="6" md="3">
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
        <v-col cols="12" sm="6" md="4">
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
      <h3 class="text-h5 mt-10 mb-8">Ces cantines ont aussi réalisé les mesures suivantes en {{ year }}</h3>
      <v-row class="justify-space-between mb-8 px-4">
        <BadgeCard
          v-for="measure in otherMeasures"
          :key="measure.id"
          :measure="measure"
          :percentageAchieved="statistics[measure.badgeId + 'Percent']"
          class="mb-4"
        />
      </v-row>
    </div>
  </div>
</template>

<script>
import BadgeCard from "./BadgeCard"
import VueApexCharts from "vue-apexcharts"
import labels from "@/data/quality-labels.json"
import keyMeasures from "@/data/key-measures.json"
import jsonDepartments from "@/departments.json"
import jsonRegions from "@/regions.json"
import { normaliseText } from "@/utils"

export default {
  name: "PublicCanteenStatisticsPage",
  components: {
    BadgeCard,
    VueApexCharts,
  },
  data() {
    return {
      year: 2021,
      region: undefined,
      department: undefined,
      labels,
      approMeasure: keyMeasures.find((measure) => measure.badgeId === "appro"),
      otherMeasures: keyMeasures.filter((measure) => measure.badgeId !== "appro"),
      chosenDepartment: null,
      chosenRegion: null,
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
    }
  },
  mounted() {
    this.loadLocations()
    this.loadStatistics("ma cantine", `year=${this.year}`)
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
    sectorLabels() {
      return this.sectors.map((sector) => sector.name)
    },
    sectorSeries() {
      return [
        {
          data: this.sectors.map((sector) => this.statistics.sectors[sector.id.toString()]),
          color: "#55a57e",
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
      const headerText = `Nous n'avons pas encore d'établissements dans ces ${locationsWord} :`
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
    submit() {
      let query = `year=${this.year}`
      this.locationText = ""
      let newLocationText
      if (this.chosenDepartment) {
        newLocationText = jsonDepartments.find((department) => department.departmentCode === this.chosenDepartment)
          .departmentName
        query += `&department=${this.chosenDepartment}`
      } else if (this.chosenRegion) {
        newLocationText = jsonRegions.find((region) => region.regionCode === this.chosenRegion).regionName
        query += `&region=${this.chosenRegion}`
      } else {
        newLocationText = null
        this.statistics = {}
      }
      if (newLocationText) {
        this.loadStatistics(newLocationText, query)
        // should probably move badge into a canteen attribute rather than calculating it on front
      }
    },
  },
  watch: {
    chosenRegion(newRegion) {
      if (this.chosenDepartment) {
        let depInfo = jsonDepartments.find((department) => department.departmentCode === this.chosenDepartment)
        if (depInfo.regionCode !== newRegion) {
          this.chosenDepartment = null
        }
      }
    },
  },
}
</script>
