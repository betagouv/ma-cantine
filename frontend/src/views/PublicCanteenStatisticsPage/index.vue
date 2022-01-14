<template>
  <div class="text-left grey--text text--darken-4">
    <h1 class="text-h4 font-weight-black black--text mt-3 mb-6">Découvrir les démarches chez vous</h1>
    <!-- Add image? -->
    <!-- Add some introductory text? -->
    <v-form class="my-4">
      <v-row>
        <v-col cols="12" sm="6" md="4">
          <label for="select-region" class="text-body-2">
            Région
          </label>
          <!-- required? -->
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
      <h2 class="text--darken-5 text-h4 mb-2">Les statistiques pour {{ locationText }}</h2>
      <v-row>
        <v-col cols="7">
          <p class="pt-6">
            Aujourd'hui, il y a
            <span class="text-h5 font-weight-bold">{{ statistics.canteensRegistered }}</span>
            cantines dans {{ locationText }} sur ce site.
          </p>
          <p>
            <span class="text-h5 font-weight-bold">{{ statistics.canteensPublished }}</span>
            cantines ont publié leurs données, accessible par
            <router-link :to="{ name: 'CanteensHome' }">nos cantines</router-link>
            .
          </p>
        </v-col>
        <v-spacer></v-spacer>
        <v-col cols="4">
          <VueApexCharts :options="chartOptions" :series="chartSeries" type="pie" height="auto" width="100%" />
        </v-col>
      </v-row>
      <h3 class="text-h5 mt-10 mb-8 text--darken-5">Qualité de produits en {{ year }}</h3>
      <v-row>
        <v-col cols="12" sm="6" md="5" class="pl-0">
          <v-card class="fill-height text-center pt-4 pb-2 px-4 d-flex flex-column" outlined>
            <v-img max-width="30" contain src="/static/images/badges/appro.svg" class="mx-auto" alt=""></v-img>
            <v-card-text class="grey--text text--darken-2">
              <v-row class="align-end">
                <span class="text-h5 font-weight-black mr-1" style="line-height: inherit;">
                  {{ statistics.approPercent }} %
                </span>
                <span class="text-body-2">
                  ont réalisé la mesure
                  <span class="font-weight-black">« {{ approMeasure.shortTitle.toLowerCase() }} »</span>
                </span>
              </v-row>
            </v-card-text>
            <v-card-actions class="px-1">
              <router-link :to="{ name: 'KeyMeasurePage', params: { id: approMeasure.id } }" class="text-body-2">
                La mesure
              </router-link>
            </v-card-actions>
          </v-card>
        </v-col>
        <!-- TODO: this was copied from CanteenPublication. Consider making a component -->
        <v-col cols="12" sm="6" md="3">
          <v-card class="fill-height text-center py-4 d-flex flex-column justify-center" outlined>
            <v-card-text>
              <span class="text-h5 font-weight-black mr-1">{{ statistics.bioPercent }} %</span>
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
              <span class="text-h5 font-weight-black mr-1">{{ statistics.sustainablePercent }} %</span>
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
      <v-row class="justify-space-between mb-8">
        <BadgeCard
          v-for="measure in otherMeasures"
          :key="measure.id"
          :measure="measure"
          :percentageAchieved="statistics[measure.badgeId + 'Percent']"
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
      regions: this.formatLocations(jsonRegions, "region"),
      chosenDepartment: null,
      chosenRegion: null,
      locationText: null,
      statistics: {
        canteensRegistered: 341,
        canteensPublished: 240,
        // appro values
        bioPercent: 14,
        sustainablePercent: 35,
        // % canteens achieved each badge
        // Should canteens have to be published for the count?
        approPercent: 67,
        wastePercent: 12,
        diversificationPercent: 26,
        plasticPercent: 89,
        infoPercent: 34,
      },
      chartOptions: {
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
    }
  },
  computed: {
    departments() {
      let departments = jsonDepartments
      if (this.chosenRegion) {
        departments = departments.filter((department) => department.regionCode === this.chosenRegion)
      }
      return this.formatLocations(departments, "department")
    },
    chartSeries() {
      return [this.statistics.canteensPublished, this.statistics.canteensRegistered - this.statistics.canteensPublished]
    },
  },
  methods: {
    formatLocations(locations, locationKeyWord) {
      return locations.map((x) => ({
        text: `${x[`${locationKeyWord}Code`]} - ${x[`${locationKeyWord}Name`]}`,
        value: x[`${locationKeyWord}Code`],
      }))
    },
    submit() {
      this.locationText = ""
      if (this.chosenDepartment) {
        this.locationText = jsonDepartments.find(
          (department) => department.departmentCode === this.chosenDepartment
        ).departmentName
      } else if (this.chosenRegion) {
        this.locationText = jsonRegions.find((region) => region.regionCode === this.chosenRegion).regionName
      } else {
        this.locationText = null
      }
      // return stats by region/department and year from backend
      // should probably move badge into a canteen attribute rather than calculating it on front
    },
  },
}
</script>
