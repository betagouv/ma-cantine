<template>
  <div class="text-left grey--text text--darken-4">
    <BreadcrumbsNav />
    <h1 class="text-h4 font-weight-black black--text mb-6">Application de la loi EGalim sur mon territoire</h1>

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

    <v-row v-if="diagnosticsLoading" justify="center" class="py-15">
      <v-progress-circular indeterminate></v-progress-circular>
    </v-row>
    <div v-else class="pt-8">
      <h2 class="text-h5 font-weight-bold">Concernant les cantines inscrites sur la plateforme</h2>
      <p v-if="locationText" class="text-body-2 mt-4 grey--text text--darken-2">
        <v-icon>mdi-map-marker</v-icon>
        {{ locationText }}
      </p>
      <p v-if="sectorsText" class="text-body-2 mt-4 grey--text text--darken-2">
        <v-icon>mdi-office-building</v-icon>
        {{ sectorsText }}
      </p>
      <v-row>
        <v-col cols="12" sm="6">
          <v-card class="fill-height text-center py-4 d-flex flex-column justify-center" outlined>
            <v-card-text>
              <p class="mb-0">
                <span class="text-h5 font-weight-black">{{ statistics.canteenCount }}</span>
                <span class="text-body-2">
                  cantines inscrites
                </span>
              </p>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="12" sm="6">
          <GraphComponent
            graphId="sector-chart"
            :label="sectorCategoryChartTitle.join(' ')"
            :options="sectorCategoryChartOptions"
            :series="sectorCategorySeries"
            type="bar"
            height="auto"
            width="100%"
          >
            <template v-slot:description>
              <p>Nombre de cantines par catégorie de secteur</p>
              <ol>
                <li v-for="(label, idx) in sectorCategoryLabels" :key="`sector-${idx}`">
                  {{ label }} : {{ sectorCategorySeries[0].data[idx] }} cantines
                </li>
              </ol>
            </template>
          </GraphComponent>
        </v-col>
      </v-row>

      <v-row class="mt-10 mb-2 px-3 align-center">
        <h2 class="text-h5 font-weight-bold">À propos des objectifs EGalim</h2>
        <div>
          <label for="select-year" class="d-sr-only">
            Année
          </label>
          <DsfrSelect
            v-model="year"
            :items="yearsList"
            hide-details
            id="select-year"
            class="ml-2"
            item-text="text"
            item-value="key"
            style="max-width: 24em"
          />
        </div>
      </v-row>
      <p v-if="locationText" class="text-body-2 mt-4 grey--text text--darken-2">
        <v-icon>mdi-map-marker</v-icon>
        {{ locationText }}
      </p>
      <p v-if="sectorsText" class="text-body-2 mt-4 grey--text text--darken-2">
        <v-icon>mdi-office-building</v-icon>
        {{ sectorsText }}
      </p>
      <v-row>
        <v-col cols="12" sm="4">
          <v-card class="fill-height text-center py-4 d-flex flex-column justify-center" outlined>
            <v-card-text>
              <p class="mb-0">
                <span class="text-h5 font-weight-black">{{ statistics.canteenCount }}</span>
                <span class="text-body-2">
                  cantines inscrites
                </span>
              </p>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="12" sm="4">
          <v-card class="fill-height text-center py-4 d-flex flex-column justify-center" outlined>
            <v-card-text>
              <p class="mb-0">
                <span class="text-h5 font-weight-black">{{ statistics.teledeclarationsCount }}</span>
                <span class="text-body-2">
                  bilans télédéclarés
                </span>
              </p>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="12" sm="4">
          <v-card class="fill-height text-center pt-4 pb-2 px-3 d-flex flex-column" outlined>
            <v-img max-width="30" contain src="/static/images/badges/appro.svg" class="mx-auto" alt=""></v-img>
            <v-card-text class="grey--text text--darken-2 px-1">
              <p class="mb-0">
                <span class="text-h5 font-weight-black" style="line-height: inherit;">
                  {{ statistics.approPercent }} %
                </span>
                <span class="text-body-2">
                  ont réussi l'objectif d'approvisionnement EGalim
                </span>
              </p>
            </v-card-text>
            <v-card-actions class="px-1">
              <router-link :to="{ name: 'KeyMeasurePage', params: { id: approMeasure.id } }" class="text-body-2">
                La mesure
              </router-link>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
      <div v-if="statistics.teledeclarationsCount === 0">
        <p class="mt-8 caption">
          Aucune cantine n'a renseigné des données relatives à la loi EGalim pour l'année {{ year }}.
        </p>
      </div>
      <div v-else-if="year === yearLast">
        <DsfrCallout class="my-6">
          <p class="mb-0">
            Les données {{ yearLast }} récoltées durant la campagne {{ yearLast + 1 }} seront disponibles d'ici la fin
            d'année (dès lors que le rapport statistique sera validé par le parlement).
          </p>
        </DsfrCallout>
      </div>
      <div v-else>
        <p class="mt-4">Parmi les {{ statistics.teledeclarationsCount }} bilans télédéclarés&nbsp;:</p>
        <v-row class="px-2">
          <v-col class="px-1" cols="12" sm="6">
            <v-card class="fill-height text-center py-4 d-flex flex-column justify-center" outlined>
              <v-card-text>
                <p class="mb-0">
                  <span class="text-h5 font-weight-black">{{ statistics.bioPercent }} %</span>
                  <span class="text-body-2">
                    bio moyen
                  </span>
                </p>
              </v-card-text>
              <div class="mt-2">
                <v-img contain src="/static/images/quality-labels/logo_bio_eurofeuille.png" alt="" max-height="35" />
              </div>
            </v-card>
          </v-col>
          <v-col class="pl-1 pr-0" cols="12" sm="6">
            <v-card class="fill-height text-center py-4 d-flex flex-column justify-center" outlined>
              <v-card-text>
                <p class="mb-0">
                  <span class="text-h5 font-weight-black">{{ statistics.sustainablePercent }} %</span>
                  <span class="text-body-2">
                    durables et de qualité (hors bio) moyen
                  </span>
                </p>
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
        <!-- chiffres faux (requêtes à revoir), on cache en attendant
        <h3 class="text-h6 font-weight-bold mt-10 mb-2">
          Ces cantines ont aussi réalisé les mesures suivantes en {{ year }}
        </h3>
        <p>Parmi les {{ statistics.teledeclarationsCount }} bilans télédéclarés &nbsp;:</p>
        <v-row>
          <v-col cols="12" sm="6" md="5" v-for="measure in otherMeasures" :key="measure.id" class="mb-4">
            <BadgeCard :measure="measure" :percentageAchieved="statistics[measure.badgeId + 'Percent']" />
          </v-col>
        </v-row>
        <BadgesExplanation />
        -->
      </div>
    </div>
  </div>
</template>

<script>
// import BadgeCard from "./BadgeCard"
// import BadgesExplanation from "./BadgesExplanation"
import labels from "@/data/quality-labels.json"
import keyMeasures from "@/data/key-measures.json"
import jsonDepartments from "@/departments.json"
import jsonRegions from "@/regions.json"
import jsonEpcis from "@/epcis.json"
import { lastYear, normaliseText, sectorsSelectList, capitalise, getObjectDiff } from "@/utils"
import BreadcrumbsNav from "@/components/BreadcrumbsNav"
import DsfrAutocomplete from "@/components/DsfrAutocomplete"
import DsfrSelect from "@/components/DsfrSelect"
import GraphComponent from "@/components/GraphComponent"
import DsfrCallout from "@/components/DsfrCallout"

const yearLast = lastYear()
const yearsList = Array.from(new Array(yearLast - 2020 + 1), (x, i) => i + 2020).map((year) => ({
  key: year,
  text: `données ${year} (télédéclarées en ${year + 1})`,
}))

export default {
  name: "PublicCanteenStatisticsPage",
  components: {
    // BadgeCard,
    // BadgesExplanation,
    BreadcrumbsNav,
    DsfrAutocomplete,
    DsfrSelect,
    GraphComponent,
    DsfrCallout,
  },
  data() {
    return {
      year: yearLast, // init
      yearLast: yearLast,
      yearsList: yearsList,
      labels,
      approMeasure: keyMeasures.find((measure) => measure.badgeId === "appro"),
      otherMeasures: keyMeasures.filter((measure) => measure.badgeId !== "appro"),
      chosenDepartments: [],
      chosenRegions: [],
      chosenSectors: [],
      chosenEpcis: [],
      locationText: null,
      statistics: {},
      loadedDepartmentIds: [],
      loadedRegionIds: [],
      sectorCategoryChartTitle: [
        "Nombre de cantines par catégorie de secteur.",
        "Une cantine peut avoir plusieurs catégories.",
      ],
      defaultLocationText: null,
      epcis: jsonEpcis,
      diagnosticsLoading: true,
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
            fontSize: this.$vuetify.breakpoint.xs ? "12px" : "14px",
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
            })
            this.chosenEpcis = []
            this.locationText = this.createLocationText()
          } else {
            this.locationText = newLocationText
          }
          this.diagnosticsLoading = false
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
        locationText = `${this.chosenEpcis.length} EPCIs : ${names.join(", ")}`
      } else if (this.chosenEpcis.length === 1) {
        locationText = `« ${jsonEpcis.find((epci) => epci.code === this.chosenEpcis[0]).nom} »`
      } else if (this.chosenDepartments.length > 1) {
        let names = []
        this.chosenDepartments.forEach((d) => {
          names.push(jsonDepartments.find((department) => department.departmentCode === d).departmentName)
        })
        locationText = `${this.chosenDepartments.length} départements : ${names.join(", ")}`
      } else if (this.chosenDepartments.length === 1) {
        locationText = `« ${
          jsonDepartments.find((department) => department.departmentCode === this.chosenDepartments[0]).departmentName
        } »`
      } else if (this.chosenRegions.length > 1) {
        let names = []
        this.chosenRegions.forEach((d) => {
          names.push(jsonRegions.find((region) => region.regionCode === d).regionName)
        })
        locationText = `${this.chosenRegions.length} régions : ${names.join(", ")}`
      } else if (this.chosenRegions.length === 1) {
        locationText = `« ${jsonRegions.find((region) => region.regionCode === this.chosenRegions[0]).regionName} »`
      } else {
        locationText = this.defaultLocationText
      }
      return locationText
    },
    updateStatistics() {
      this.diagnosticsLoading = true
      let query = `year=${this.year}`
      if (this.chosenEpcis.length) {
        this.chosenEpcis.forEach((e) => {
          query += `&epci=${e}`
        })
      } else if (this.chosenDepartments.length) {
        this.chosenDepartments.forEach((d) => {
          query += `&department=${d}`
        })
      } else if (this.chosenRegions.length) {
        this.chosenRegions.forEach((r) => {
          query += `&region=${r}`
        })
      }
      if (this.chosenSectors.length) {
        query += `&sectors=${this.chosenSectors.join("&sectors=")}`
      }
      let newLocationText = this.createLocationText()
      this.loadStatistics(newLocationText, query)
    },
    updateRoute() {
      let query = {}
      if (this.year) {
        query.year = this.year
      }
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
      this.year = +this.$route.query.year || lastYear()
      this.chosenRegions = this.$route.query.region || []
      if (!Array.isArray(this.chosenRegions)) this.chosenRegions = [this.chosenRegions]
      this.chosenDepartments = this.$route.query.department || []
      if (!Array.isArray(this.chosenDepartments)) this.chosenDepartments = [this.chosenDepartments]
      this.chosenEpcis = this.$route.query.epcis || []
      if (!Array.isArray(this.chosenEpcis)) this.chosenEpcis = [this.chosenEpcis]
      this.chosenSectors = this.$route.query.sectors?.split(",").map((s) => parseInt(s, 10)) || []
    },
    updateDocumentTitle() {
      let title = `Sur mon territoire - ${this.$store.state.pageTitleSuffix}`
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
      const changedParams = Object.keys(getObjectDiff(newRoute.query, oldRoute.query))
      if (changedParams.length === 1 && changedParams[0] === "year") {
        this.updateStatistics()
      } else {
        this.locationText = "" // refresh whole page, not just year stats
        this.updateStatistics()
      }
      this.updateDocumentTitle()
    },
    year() {
      this.updateRoute()
    },
  },
}
</script>
