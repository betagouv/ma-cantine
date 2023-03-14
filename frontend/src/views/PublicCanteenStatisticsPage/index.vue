<template>
  <div class="text-left grey--text text--darken-4">
    <BreadcrumbsNav :links="[{ to: { name: 'CanteensHome' } }]" />
    <h1 class="text-h4 font-weight-black black--text mb-6">Découvrir les démarches chez vous</h1>

    <v-card outlined>
      <v-card-text>
        <v-form class="mb-2">
          <v-row>
            <v-col class="py-0 mt-4" cols="12" sm="6">
              <label for="select-region" class="text-body-2">
                Région
              </label>
              <DsfrAutocomplete
                v-model="chosenRegions"
                :items="regions"
                clearable
                multiple
                hide-details
                id="select-region"
                placeholder="Toutes les régions"
                class="mt-1"
                auto-select-first
                :filter="locationFilter"
                no-data-text="Pas de résultats"
              />
            </v-col>
            <v-col class="py-2 py-sm-0 mt-4" cols="12" sm="6">
              <label for="select-department" class="text-body-2">
                Département
              </label>
              <DsfrAutocomplete
                v-model="chosenDepartments"
                :items="departments"
                clearable
                multiple
                hide-details
                id="select-department"
                placeholder="Tous les départements"
                class="mt-1"
                auto-select-first
                :filter="locationFilter"
                no-data-text="Pas de résultats"
              />
            </v-col>
            <v-col class="py-2 py-sm-0 mt-4" cols="12" sm="6">
              <label for="select-epci" class="text-body-2">
                EPCI
              </label>
              <DsfrAutocomplete
                v-model="chosenEpcis"
                :items="epcis"
                clearable
                multiple
                hide-details
                id="select-epci"
                placeholder="Tous les EPCIs"
                class="mt-1"
                auto-select-first
                no-data-text="Pas de résultats"
                item-text="nom"
                item-value="code"
              />
            </v-col>
            <v-col class="py-2 py-sm-0 mt-4" cols="12" sm="6">
              <label for="select-sector" class="text-body-2">
                Secteur d'activité
              </label>
              <DsfrSelect
                v-model="chosenSectors"
                multiple
                :items="sectorsList"
                item-text="name"
                item-value="id"
                clearable
                hide-details
                id="select-sector"
                placeholder="Tous les secteurs"
                class="mt-1"
              />
            </v-col>
          </v-row>
          <v-row class="mt-6">
            <v-col cols="12" sm="6" md="4">
              <v-btn x-large color="primary" @click="updateRoute">
                Filtrer les données
              </v-btn>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
    </v-card>
    <div v-if="locationText" class="py-8">
      <h2 class="text-h5 font-weight-bold">Les chiffres pour {{ locationText }}</h2>
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
            :options="sectorCategoryChartOptions"
            :series="sectorCategorySeries"
            type="bar"
            height="auto"
            width="100%"
            role="img"
            :aria-label="sectorCategoryChartTitle"
            aria-describedby="sector-chart-description"
          />
          <p id="sector-chart-description" class="d-none">{{ sectorChartDescription }}</p>
        </v-col>
      </v-row>
      <div v-if="statistics.diagnosticsCount === 0">
        <p class="mt-8 caption">
          Aucune cantine n'a renseigné des données relatives à la loi EGAlim pour l'année {{ year }}.
        </p>
      </div>
      <div v-else>
        <h3 class="text-h6 font-weight-bold mt-10 mb-2">Qualité de produits en {{ year }}</h3>
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
        <BadgesExplanation />
      </div>
    </div>
    <v-row v-else justify="center" class="py-15">
      <v-progress-circular indeterminate></v-progress-circular>
    </v-row>
  </div>
</template>

<script>
import BadgeCard from "./BadgeCard"
import BadgesExplanation from "./BadgesExplanation"
import VueApexCharts from "vue-apexcharts"
import labels from "@/data/quality-labels.json"
import keyMeasures from "@/data/key-measures.json"
import jsonDepartments from "@/departments.json"
import jsonRegions from "@/regions.json"
import jsonEpcis from "@/epcis.json"
import { lastYear, normaliseText, sectorsSelectList, capitalise } from "@/utils"
import BreadcrumbsNav from "@/components/BreadcrumbsNav"
import DsfrAutocomplete from "@/components/DsfrAutocomplete"
import DsfrSelect from "@/components/DsfrSelect"

export default {
  name: "PublicCanteenStatisticsPage",
  components: {
    BadgeCard,
    BadgesExplanation,
    VueApexCharts,
    BreadcrumbsNav,
    DsfrAutocomplete,
    DsfrSelect,
  },
  data() {
    return {
      year: lastYear(),
      labels,
      approMeasure: keyMeasures.find((measure) => measure.badgeId === "appro"),
      otherMeasures: keyMeasures.filter((measure) => measure.badgeId !== "appro"),
      chosenDepartments: [],
      chosenRegions: [],
      chosenSectors: [],
      chosenEpcis: [],
      locationText: null,
      statistics: {},
      publishedChartOptions: {
        labels: ["Publiée", "Non publiée"],
        colors: ["#6a6af4", "#aaa"],
        dataLabels: {
          dropShadow: false,
          style: {
            colors: ["#000"],
            fontSize: "14px",
          },
          offsetX: 30,
        },
      },
      loadedDepartmentIds: [],
      loadedRegionIds: [],
      sectorCategoryChartTitle: [
        "Nombre de cantines par catégorie de secteur.",
        "Une cantine peut avoir plusieurs catégories.",
      ],
      defaultLocationText: "l'ensemble de la plateforme",
      statsLevel: "site",
      epcis: jsonEpcis,
    }
  },
  mounted() {
    this.populateInitialParameters()
    this.loadLocations()
    this.updateStatistics()
    this.updateDocumentTitle()
  },
  computed: {
    departments() {
      let enabledDepartments = this.loadedDepartmentIds
      let departmentsForRegions = jsonDepartments
      if (this.chosenRegions.length) {
        departmentsForRegions = jsonDepartments.filter(
          (department) => this.chosenRegions.indexOf(department.regionCode) > -1
        )
      }
      return this.formatLocations(enabledDepartments, departmentsForRegions, "department", "départements")
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
    sectorCategories() {
      return this.$store.state.sectorCategories
    },
    sectorCategoryLabels() {
      const categoriesMap = {
        administration: "Administration",
        enterprise: "Entreprise",
        education: "Enseignement",
        health: "Santé",
        social: "Social / Médico-social",
        leisure: "Loisirs",
        autres: "Autres",
      }
      return this.sectorCategories.map((category) => categoriesMap[category] || "Inconnu")
    },
    sectorCategorySeries() {
      return [
        {
          data: this.sectorCategories.map((category) => this.statistics.sectorCategories[category || "inconnu"]),
          color: "#6a6af4",
          name: "Nombre de cantines",
        },
      ]
    },
    sectorCategoryChartOptions() {
      return {
        title: {
          text: this.sectorCategoryChartTitle,
          style: {
            fontSize: "14px",
            fontWeight: "normal",
            fontFamily: "Marianne",
            color: "#333",
          },
          offsetX: this.$vuetify.breakpoint.mdAndUp ? 162 : 10,
          offsetY: -5,
          margin: 20,
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
          categories: this.sectorCategoryLabels,
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
      Object.keys(this.statistics.sectorCategories).forEach((key) => {
        desc += `${this.sectorCategories.find((category) => category === key)}, ${
          this.statistics.sectorCategories[key]
        }; `
      })
      return desc
    },
    statsLevelDisplay() {
      return {
        department: "ce département",
        region: "cette région",
        departments: "ces départements",
        regions: "ces régions",
        site: "ce site",
        epci: "cet EPCI",
      }[this.statsLevel]
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
          if (this.statistics.epciError) {
            this.$store.dispatch("notify", {
              title: "Nous n'avons pas trouvé les infos pour l'EPCI choisi",
              message:
                "Une erreur est survenue, vous pouvez réessayer plus tard ou nous contacter directement à support-egalim@beta.gouv.fr",
              status: "error",
              duration: 7000,
            })
            this.chosenEpcis = []
            this.locationText = this.createLocationText()
          } else {
            this.locationText = newLocationText
          }
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

      let headerText = "Nous "
      if (this.chosenRegions.length && locationKeyWord.startsWith("department")) {
        let regionText = "les régions séléctionnées"
        if (this.chosenRegions.length === 1) {
          regionText = jsonRegions.find((region) => region.regionCode === this.chosenRegions[0]).regionName
          regionText = `la région « ${regionText} »`
        }
        headerText = `Pour ${regionText}, nous `
      }
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
      if (this.chosenEpcis.length > 1) {
        let names = []
        this.chosenEpcis.forEach((d) => {
          names.push(jsonEpcis.find((epci) => epci.code === d).nom)
        })
        locationText = `les ${this.chosenEpcis.length} EPCIs : ${names.join(", ")}`
      } else if (this.chosenEpcis.length === 1) {
        locationText = `« ${jsonEpcis.find((epci) => epci.code === this.chosenEpcis[0]).nom} »`
      } else if (this.chosenDepartments.length > 1) {
        let names = []
        this.chosenDepartments.forEach((d) => {
          names.push(jsonDepartments.find((department) => department.departmentCode === d).departmentName)
        })
        locationText = `les ${this.chosenDepartments.length} départements : ${names.join(", ")}`
      } else if (this.chosenDepartments.length === 1) {
        locationText = `« ${
          jsonDepartments.find((department) => department.departmentCode === this.chosenDepartments[0]).departmentName
        } »`
      } else if (this.chosenRegions.length > 1) {
        let names = []
        this.chosenRegions.forEach((d) => {
          names.push(jsonRegions.find((region) => region.regionCode === d).regionName)
        })
        locationText = `les ${this.chosenRegions.length} régions : ${names.join(", ")}`
      } else if (this.chosenRegions.length === 1) {
        locationText = `« ${jsonRegions.find((region) => region.regionCode === this.chosenRegions[0]).regionName} »`
      } else {
        locationText = this.defaultLocationText
      }
      return locationText
    },
    updateStatistics() {
      let query = `year=${this.year}`
      this.locationText = ""
      if (this.chosenEpcis.length) {
        this.chosenEpcis.forEach((e) => {
          query += `&epci=${e}`
        })
        this.statsLevel = "epci"
      } else if (this.chosenDepartments.length) {
        this.chosenDepartments.forEach((d) => {
          query += `&department=${d}`
        })
        if (this.chosenDepartments.length === 1) {
          this.statsLevel = "department"
        } else {
          this.statsLevel = "departments"
        }
      } else if (this.chosenRegions.length) {
        this.chosenRegions.forEach((r) => {
          query += `&region=${r}`
        })
        if (this.chosenRegions.length === 1) {
          this.statsLevel = "region"
        } else {
          this.statsLevel = "regions"
        }
      } else {
        this.statsLevel = "site"
      }
      if (this.chosenSectors.length) {
        query += `&sectors=${this.chosenSectors.join("&sectors=")}`
      }
      let newLocationText = this.createLocationText()
      this.loadStatistics(newLocationText, query)
    },
    updateRoute() {
      let query = {}
      if (this.chosenRegions) {
        query.region = this.chosenRegions
      }
      if (this.chosenDepartments) {
        query.department = this.chosenDepartments
      }
      if (this.chosenEpcis) {
        query.epcis = this.chosenEpcis
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
      this.chosenRegions = this.$route.query.region || []
      if (!Array.isArray(this.chosenRegions)) this.chosenRegions = [this.chosenRegions]
      this.chosenDepartments = this.$route.query.department || []
      if (!Array.isArray(this.chosenDepartments)) this.chosenDepartments = [this.chosenDepartments]
      this.chosenEpcis = this.$route.query.epcis || []
      if (!Array.isArray(this.chosenEpcis)) this.chosenEpcis = [this.chosenEpcis]
      this.chosenSectors = this.$route.query.sectors?.split(",").map((s) => parseInt(s, 10)) || []
    },
    updateDocumentTitle() {
      let title = `Les cantines dans ma collectivité - ${this.$store.state.pageTitleSuffix}`
      if (this.chosenRegions.length || this.chosenDepartments.length || this.chosenEpcis.length) {
        let locationText = this.createLocationText()
        if (locationText.startsWith("les")) {
          locationText = capitalise(locationText)
        }
        title = `${locationText} - ${title}`
      }
      document.title = title
    },
  },
  watch: {
    chosenRegions(newRegions, oldRegions) {
      // If the regions selection has been narrowed, chosen deps could now fall outside regions chosen.
      // If chosen regions was cleared, all deps are valid, so leave selection alone.
      // If there weren't any regions (and now there are), clear departments.
      // If there are fewer regions than previously, clear department selection.
      if (newRegions.length && (!oldRegions.length || newRegions.length < oldRegions.length)) {
        this.chosenDepartments = []
      }
    },
    $route(newRoute, oldRoute) {
      if (newRoute.fullPath === oldRoute.fullPath) return
      this.populateInitialParameters()
      this.updateStatistics()
      this.updateDocumentTitle()
    },
  },
}
</script>
