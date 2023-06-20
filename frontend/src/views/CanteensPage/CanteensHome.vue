<template>
  <div>
    <BreadcrumbsNav />
    <v-card elevation="0" class="text-center text-md-left mb-6 mt-3">
      <v-row v-if="$vuetify.breakpoint.smAndDown">
        <v-col cols="12">
          <v-img max-height="90px" contain src="/static/images/doodles-dsfr/primary/LovingDoodle.png"></v-img>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="2" v-if="$vuetify.breakpoint.mdAndUp">
          <div class="d-flex fill-height align-center">
            <v-img contain src="/static/images/doodles-dsfr/primary/LovingDoodle.png"></v-img>
          </div>
        </v-col>
        <v-col cols="12" md="10">
          <v-spacer></v-spacer>
          <v-card-title class="pr-0">
            <h1 class="font-weight-black text-h5 text-sm-h4 mb-4" style="width: 100%">
              Nos cantines
            </h1>
          </v-card-title>
          <v-card-subtitle>
            <p class="mb-1">
              Découvrez les initiatives prises par nos cantines pour une alimentation saine, de qualité, et plus durable
            </p>
            <p>
              Consulter
              <router-link :to="{ name: 'PublicCanteenStatisticsPage' }">
                les statistiques de votre collectivité (régions et départements)
              </router-link>
            </p>
          </v-card-subtitle>

          <v-spacer></v-spacer>
        </v-col>
      </v-row>
    </v-card>
    <v-sheet class="px-6" elevation="0">
      <v-row>
        <v-col cols="12" md="7" class="pt-0">
          <form role="search" class="d-block d-sm-flex align-end" onsubmit="return false">
            <DsfrSearchField
              hide-details="auto"
              ref="search"
              v-model="searchTerm"
              placeholder="Recherche par nom de l'établissement"
              :searchAction="search"
              :clearAction="clearSearch"
              class="mb-2 flex-grow-1"
            />
          </form>
        </v-col>
      </v-row>
    </v-sheet>

    <div class="d-flex align-center mt-4 pl-0 pl-md-6">
      <v-badge :value="hasActiveFilter" color="#CE614A" dot overlap offset-x="-2">
        <h2 class="text-body-1 font-weight-black" style="background-color: #fff; width: max-content">
          Filtres
        </h2>
      </v-badge>
      <v-btn text color="primary" small @click="showFilters = !showFilters" class="ml-1 py-4 py-sm-0">
        <v-icon small>mdi-filter-outline</v-icon>
        <span v-if="showFilters">Cacher les filtres</span>
        <span v-else>Afficher les filtres</span>
      </v-btn>

      <v-btn text color="primary" small @click="clearFilters" v-if="hasActiveFilter">
        <v-icon small>mdi-filter-off-outline</v-icon>
        Enlever tous les filtres
      </v-btn>
      <v-divider v-if="!showFilters"></v-divider>
    </div>
    <v-expand-transition>
      <v-sheet class="pa-6 text-left mt-2 ml-6" v-show="showFilters" rounded :outlined="showFilters">
        <v-row>
          <v-col cols="12" sm="6" md="4">
            <label
              for="select-region"
              :class="{
                'text-body-2': true,
                'active-filter-label': !!filters.region.value,
              }"
            >
              Région
            </label>
            <DsfrAutocomplete
              v-model="filters.region.value"
              :items="regions"
              clearable
              hide-details
              id="select-region"
              placeholder="Toutes les régions"
              class="mt-1"
              auto-select-first
              :filter="locationFilter"
            />
          </v-col>
          <v-col cols="12" sm="6" md="4">
            <label
              for="select-department"
              :class="{
                'text-body-2': true,
                'active-filter-label': !!filters.department.value,
              }"
            >
              Département
            </label>
            <DsfrAutocomplete
              v-model="filters.department.value"
              :items="departments"
              clearable
              hide-details
              id="select-department"
              placeholder="Tous les départements"
              class="mt-1"
              auto-select-first
              :filter="locationFilter"
            />
          </v-col>
          <v-col cols="12" sm="6" md="4">
            <label
              for="select-sector"
              :class="{
                'text-body-2': true,
                'active-filter-label': filters.sectors.value && !!filters.sectors.value.length,
              }"
            >
              Secteur d'activité
            </label>
            <DsfrSelect
              v-model="filters.sectors.value"
              multiple
              :items="sectors"
              clearable
              hide-details
              id="select-sector"
              placeholder="Tous les secteurs"
              class="mt-1"
            />
          </v-col>
        </v-row>
        <v-row class="align-end mt-0">
          <v-col cols="12" sm="8" md="6">
            <label class="text-body-2">
              Dans les assiettes, part de...
            </label>
            <div class="d-flex align-stretch mt-1">
              <v-col class="pa-0 pr-1 d-flex flex-column">
                <label
                  :class="{
                    caption: true,
                    'pl-1': true,
                    'active-filter-label': !!filters.min_portion_bio.value,
                  }"
                  id="value-percentages-bio"
                >
                  bio minimum
                </label>
                <v-spacer></v-spacer>
                <DsfrTextField
                  :value="filters.min_portion_bio.value"
                  ref="min_portion_bio"
                  :rules="[validators.nonNegativeOrEmpty, validators.lteOrEmpty(100)]"
                  @change="onChangeIntegerFilter('min_portion_bio')"
                  hide-details="auto"
                  append-icon="mdi-percent"
                  placeholder="0"
                  aria-describedby="value-percentages-bio"
                />
              </v-col>
              <v-col class="pa-0 pl-1 d-flex flex-column">
                <label
                  :class="{
                    caption: true,
                    'pl-1': true,
                    'active-filter-label': !!filters.min_portion_combined.value,
                  }"
                  id="value-percentages-bio-qualite"
                >
                  bio, qualité et durables min
                </label>
                <v-spacer></v-spacer>
                <DsfrTextField
                  :value="filters.min_portion_combined.value"
                  ref="min_portion_combined"
                  :rules="[validators.nonNegativeOrEmpty, validators.lteOrEmpty(100)]"
                  @change="onChangeIntegerFilter('min_portion_combined')"
                  hide-details="auto"
                  placeholder="0"
                  append-icon="mdi-percent"
                  aria-describedby="value-percentages-bio-qualite"
                />
              </v-col>
            </div>
          </v-col>
          <v-col cols="12" sm="4" md="3">
            <label
              :class="{
                'text-body-2': true,
                'active-filter-label': !!filters.min_daily_meal_count.value || !!filters.max_daily_meal_count.value,
              }"
              id="meal-count"
            >
              Repas par jour
            </label>
            <div class="d-flex">
              <div>
                <label class="caption" for="min-meal-count-field">
                  Min
                </label>
                <DsfrTextField
                  :value="filters.min_daily_meal_count.value"
                  ref="min_daily_meal_count"
                  :rules="[validators.nonNegativeOrEmpty]"
                  @change="onChangeIntegerFilter('min_daily_meal_count')"
                  hide-details="auto"
                  id="min-meal-count-field"
                  aria-describedby="meal-count"
                />
              </div>
              <span class="mx-2 align-self-center">-</span>
              <div>
                <label class="caption" for="max-meal-count-field">
                  Max
                </label>
                <DsfrTextField
                  :value="filters.max_daily_meal_count.value"
                  ref="max_daily_meal_count"
                  :rules="[validators.nonNegativeOrEmpty]"
                  @change="onChangeIntegerFilter('max_daily_meal_count')"
                  hide-details="auto"
                  aria-describedby="meal-count"
                  id="max-meal-count-field"
                />
              </div>
            </div>
          </v-col>
          <v-col cols="12" sm="4" md="3">
            <label
              for="select-management-type"
              :class="{ 'text-body-2': true, 'active-filter-label': !!filters.management_type.value }"
            >
              Mode de gestion
            </label>
            <DsfrSelect
              v-model="filters.management_type.value"
              :items="managementTypes"
              clearable
              hide-details
              id="select-management-type"
              class="mt-1"
              placeholder="Tous les modes"
            />
          </v-col>
          <v-col cols="12" sm="6" md="5">
            <label
              for="select-production-type"
              :class="{ 'text-body-2': true, 'active-filter-label': !!filters.production_type.value }"
            >
              Type d'établissement
            </label>
            <DsfrSelect
              v-model="filters.production_type.value"
              :items="productionTypes"
              clearable
              hide-details
              id="select-production-type"
              class="mt-1"
              placeholder="Tous les cantines"
            />
          </v-col>
          <v-col cols="12" sm="6" md="5">
            <label for="select-badge" :class="{ 'text-body-2': true, 'active-filter-label': !!filters.badge.value }">
              Mesure EGAlim réalisée
            </label>
            <DsfrSelect
              v-model="filters.badge.value"
              :items="badges"
              clearable
              hide-details
              id="select-badge"
              class="mt-1"
              placeholder="Tous les cantines"
            />
          </v-col>
        </v-row>
      </v-sheet>
    </v-expand-transition>
    <div v-if="loading" class="pa-6">
      <v-progress-circular indeterminate></v-progress-circular>
    </div>
    <div v-else-if="visibleCanteens && visibleCanteens.length > 0">
      <p class="mt-3 mb-n4 text-body-2 grey--text" v-if="resultsCountText">
        {{ resultsCountText }}
      </p>
      <v-row class="my-2" align="end">
        <v-col cols="3" v-if="$vuetify.breakpoint.smAndUp"></v-col>
        <v-spacer v-if="$vuetify.breakpoint.smAndUp"></v-spacer>
        <v-col cols="12" sm="6">
          <DsfrPagination v-model="page" :length="Math.ceil(publishedCanteenCount / limit)" :total-visible="7" />
        </v-col>
        <v-spacer></v-spacer>
        <v-col id="ordering" cols="12" sm="3" class="d-flex align-end">
          <DsfrSelect
            v-model="orderBy"
            :items="orderOptions"
            labelClasses="body-2 text-left mb-2"
            hide-details
            label="Trier par"
          />
          <v-btn
            icon
            @click="toggleOrderDirection"
            :title="`Resultats affichés en ordre ${orderDescending ? 'décroissant' : 'croissant'}`"
            plain
          >
            <v-icon v-if="orderDescending">mdi-arrow-down</v-icon>
            <v-icon v-else>
              mdi-arrow-up
            </v-icon>
          </v-btn>
        </v-col>
      </v-row>
      <v-row>
        <v-col v-for="canteen in visibleCanteens" :key="canteen.id" style="height: auto;" cols="12" md="6">
          <PublishedCanteenCard :canteen="canteen" />
        </v-col>
      </v-row>
      <DsfrPagination
        class="my-6"
        v-model="page"
        :length="Math.ceil(publishedCanteenCount / limit)"
        :total-visible="7"
      />
    </div>
    <div v-else class="d-flex flex-column align-center py-10">
      <v-icon large>mdi-inbox-remove</v-icon>
      <p class="text-body-1 grey--text text--darken-1 my-2">Nous n'avons pas trouvé des cantines avec ces paramètres</p>
      <v-btn color="primary" text @click="clearFilters" class="text-decoration-underline" v-if="hasActiveFilter">
        Désactiver tous les filtres
      </v-btn>
    </div>

    <v-divider class="mb-8 mt-12"></v-divider>

    <v-row class="mb-6" style="position: relative">
      <v-col cols="3" v-if="$vuetify.breakpoint.smAndUp">
        <div class="fill-height d-flex flex-column align-center">
          <v-spacer></v-spacer>
          <v-img src="/static/images/doodles-dsfr/primary/SittingDoodle.png" contain></v-img>
          <v-spacer></v-spacer>
        </div>
      </v-col>
      <v-col>
        <h2 class="text-h6 font-weight-black text-left mb-4">
          Vous n'avez pas trouvé un ou plusieurs établissements qui vous intéressent ?
        </h2>
        <p class="body-2 text-left mb-6">
          Dites-nous tout, nous ferons en sorte de leur communiquer votre intérêt pour leurs initiatives en place.
        </p>
        <v-form v-model="formIsValid" ref="form" @submit.prevent>
          <DsfrTextField v-model="fromEmail" label="Votre email" :rules="[validators.email]" validate-on-blur />
          <DsfrTextField v-model="name" label="Prénom et nom (facultatif)" />
          <DsfrTextarea v-model="message" label="Message" :rules="[validators.required]" />
        </v-form>
        <v-row class="pa-2">
          <v-spacer></v-spacer>
          <v-btn x-large color="primary" @click="sendEmail">
            <v-icon class="mr-2">mdi-send</v-icon>
            Envoyer
          </v-btn>
        </v-row>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import PublishedCanteenCard from "./PublishedCanteenCard"
import jsonDepartments from "@/departments.json"
import jsonRegions from "@/regions.json"
import { getObjectDiff, normaliseText, sectorsSelectList } from "@/utils"
import validators from "@/validators"
import Constants from "@/constants"
import badges from "@/badges"
import BreadcrumbsNav from "@/components/BreadcrumbsNav"
import DsfrTextField from "@/components/DsfrTextField"
import DsfrAutocomplete from "@/components/DsfrAutocomplete"
import DsfrSelect from "@/components/DsfrSelect"
import DsfrTextarea from "@/components/DsfrTextarea"
import DsfrPagination from "@/components/DsfrPagination"
import DsfrSearchField from "@/components/DsfrSearchField"

const DEFAULT_ORDER = "creation"

export default {
  components: {
    PublishedCanteenCard,
    BreadcrumbsNav,
    DsfrTextField,
    DsfrAutocomplete,
    DsfrSelect,
    DsfrTextarea,
    DsfrPagination,
    DsfrSearchField,
  },
  data() {
    const user = this.$store.state.loggedUser
    return {
      limit: 6,
      departments: [],
      regions: [],
      sectors: [],
      visibleCanteens: null,
      publishedCanteenCount: null,
      page: null,
      searchTerm: null,
      filters: {
        department: {
          param: "departement",
          value: null,
          default: null,
        },
        region: {
          param: "region",
          value: null,
          default: null,
        },
        management_type: {
          param: "modeDeGestion",
          value: null,
          default: null,
        },
        production_type: {
          param: "typeEtablissement",
          value: null,
          default: null,
        },
        sectors: {
          param: "secteurs",
          value: [],
          default: [],
          transformToFrontend(values) {
            return Array.isArray(values) ? values.map((v) => +v) : +values
          },
        },
        min_daily_meal_count: {
          param: "minRepasJour",
          value: null,
          default: null,
        },
        max_daily_meal_count: {
          param: "maxRepasJour",
          value: null,
          default: null,
        },
        min_portion_bio: {
          param: "minBio",
          value: null,
          default: null,
          transformToBackend(value) {
            return value / 100
          },
        },
        min_portion_combined: {
          param: "minQualite",
          value: null,
          default: null,
          transformToBackend(value) {
            return value / 100
          },
        },
        badge: {
          param: "badge",
          value: null,
          default: null,
        },
      },
      orderBy: null,
      orderOptions: [
        {
          text: "Date de création",
          value: "creation",
          query: "creation_date",
        },
        {
          text: "Date de modification",
          value: "modification",
          query: "modification_date",
        },
        {
          text: "Repas par jour",
          value: "repas",
          query: "daily_meal_count",
        },
        {
          text: "Nom de la cantine",
          value: "nom",
          query: "name",
        },
      ],
      orderDescending: true,
      fromEmail: user ? user.email : "",
      name: user ? `${user.firstName} ${user.lastName}` : "",
      message: "",
      formIsValid: true,
      managementTypes: Constants.ManagementTypes,
      productionTypes: Constants.ProductionTypes,
      showFilters: false,
      badges: [
        Object.entries(badges).map(([key, value]) => {
          return { value: key, text: value.title }
        })[0], // for now only the appro measure is available as a filter
      ],
    }
  },
  computed: {
    loading() {
      return this.publishedCanteenCount === null
    },
    offset() {
      return (this.page - 1) * this.limit
    },
    query() {
      let query = {}
      if (this.page) query.page = String(this.page)
      Object.values(this.filters).forEach((f) => {
        if (f.value) query[f.param] = f.value
      })
      if (this.order) query.trier = this.order.display
      return query
    },
    hasActiveFilter() {
      return Object.values(this.filters).some((f) => !!f.value && f.value.length)
    },
    validators() {
      return validators
    },
    resultsCountText() {
      if (!this.hasActiveFilter || !this.publishedCanteenCount) return null

      if (this.publishedCanteenCount === 1) return "Un établissement correspond à votre recherche"
      else return `${this.publishedCanteenCount} établissements correspondent à votre recherche`
    },
    order() {
      if (!this.orderBy) return null
      const chosenOption = this.orderOptions.find((opt) => opt.value === this.orderBy)
      return {
        query: `${this.orderDescending ? "-" : ""}${chosenOption?.query || DEFAULT_ORDER}`,
        display: `${chosenOption?.value || DEFAULT_ORDER}${this.orderDescending ? "Dec" : "Cro"}`,
      }
    },
  },
  methods: {
    fetchCurrentPage() {
      let queryParam = `limit=${this.limit}&offset=${this.offset}`
      Object.entries(this.filters).forEach(([key, f]) => {
        if (Array.isArray(f.value)) {
          f.value.forEach((v) => {
            queryParam += `&${key}=${v}`
          })
        } else if (f.value) queryParam += `&${key}=${f.transformToBackend ? f.transformToBackend(f.value) : f.value}`
      })
      if (this.order) queryParam += `&ordering=${this.order.query}`

      return fetch(`/api/v1/publishedCanteens/?${queryParam}`)
        .then((response) => {
          if (response.status < 200 || response.status >= 400) throw new Error(`Error encountered : ${response}`)
          return response.json()
        })
        .then((response) => {
          this.publishedCanteenCount = response.count
          this.visibleCanteens = response.results
          this.setDepartments(response.departments)
          this.setRegions(response.regions)
          this.setSectors(response.sectors)
          this.setManagementTypes(response.managementTypes)
          this.setProductionTypes(response.productionTypes)
        })
        .catch((e) => {
          this.publishedCanteenCount = 0
          this.$store.dispatch("notifyServerError", e)
        })
    },
    clearSearch() {
      this.searchTerm = ""
      this.search()
    },
    search() {
      const override = this.searchTerm ? { page: 1, recherche: this.searchTerm } : { page: 1 }
      const query = Object.assign(this.query, override)
      this.$router.push({ query }).catch(() => {})
    },
    updateOrder() {
      const override = this.order ? { page: this.page, trier: this.order.display } : { page: this.page }
      const query = Object.assign(this.query, override)
      this.$router.push({ query }).catch(() => {})
    },
    clearFilters() {
      Object.entries(this.filters).forEach(([key, f]) => {
        this.filters[key].value = f.default
      })
    },
    changePage() {
      const override = this.page ? { page: this.page } : { page: 1 }
      const query = Object.assign(this.query, override)
      this.updateRouter(query)
    },
    applyFilter() {
      const changedKeys = Object.keys(getObjectDiff(this.query, this.$route.query))
      const shouldNavigate = changedKeys.length > 0
      if (shouldNavigate) {
        this.page = 1
        this.updateRouter(Object.assign(this.query, { page: 1 }))
      } else this.fetchCurrentPage()
    },
    populateParameters() {
      this.searchTerm = this.$route.query.recherche || null
      Object.values(this.filters).forEach((f) => {
        f.value = this.$route.query[f.param]
        if (f.transformToFrontend) f.value = f.transformToFrontend(f.value)
      })
      this.page = this.$route.query.page ? parseInt(this.$route.query.page) : 1
      this.orderBy = this.$route.query.trier?.slice(0, -3) || DEFAULT_ORDER
      this.orderDescending = this.$route.query.trier?.slice(-3) === "Dec"
      this.fetchCurrentPage()
    },
    onChangeIntegerFilter(ref) {
      if (this.$refs[ref].validate()) this.filters[ref].value = parseInt(this.$refs[ref].lazyValue) || null
    },
    updateRouter(query) {
      if (this.$route.query.page) {
        this.$router.push({ query }).catch(() => {})
      } else {
        this.$router.replace({ query }).catch(() => {})
      }
    },
    sendEmail() {
      this.$refs.form.validate()
      if (!this.formIsValid) {
        this.$store.dispatch("notifyRequiredFieldsError")
        return
      }

      const payload = {
        from: this.fromEmail,
        name: this.name,
        message: this.message,
      }

      this.$store
        .dispatch("sendCanteenNotFoundEmail", payload)
        .then(() => {
          this.message = ""
          this.$refs.form.resetValidation()
          this.$store.dispatch("notify", {
            status: "success",
            message: `Votre message a bien été envoyé.`,
          })

          if (this.$matomo) {
            this.$matomo.trackEvent("message", "send", "canteen-not-found-email")
          }
          window.scrollTo(0, 0)
        })
        .catch((e) => this.$store.dispatch("notifyServerError", e))
    },
    setLocations(enabledLocationIds, jsonLocations, locationKeyWord, locationsWord) {
      const enabledLocations = jsonLocations
        .filter((x) => enabledLocationIds.indexOf(x[`${locationKeyWord}Code`]) > -1)
        .map((x) => ({
          text: `${x[`${locationKeyWord}Code`]} - ${x[`${locationKeyWord}Name`]}`,
          value: x[`${locationKeyWord}Code`],
        }))
      const headerText =
        this.hasActiveFilter || this.searchTerm
          ? `Ces ${locationsWord} ne contiennent pas d'établissements correspondant à votre recherche :`
          : `Nous n'avons pas encore d'établissements dans ces ${locationsWord} :`
      const header = { header: headerText }

      const divider = { divider: true }

      const disabledLocations = jsonLocations
        .filter((x) => enabledLocationIds.indexOf(x[`${locationKeyWord}Code`]) === -1)
        .map((x) => ({
          text: `${x[`${locationKeyWord}Code`]} - ${x[`${locationKeyWord}Name`]}`,
          value: x[`${locationKeyWord}Code`],
          disabled: true,
        }))

      return [...enabledLocations, divider, header, ...disabledLocations]
    },
    setDepartments(enabledDepartmentIds) {
      this.departments = this.setLocations(enabledDepartmentIds, jsonDepartments, "department", "départements")
    },
    setRegions(enabledRegionIds) {
      this.regions = this.setLocations(enabledRegionIds, jsonRegions, "region", "régions")
    },
    locationFilter(item, queryText, itemText) {
      return (
        Object.prototype.hasOwnProperty.call(item, "divider") ||
        Object.prototype.hasOwnProperty.call(item, "header") ||
        normaliseText(itemText).indexOf(normaliseText(queryText)) > -1
      )
    },
    setSectors(enabledSectorIds) {
      this.sectors = sectorsSelectList(this.$store.state.sectors).map((x) => {
        return x.header
          ? { header: x.header }
          : {
              text: x.name,
              value: x.id,
              disabled: enabledSectorIds.indexOf(x.id) === -1,
            }
      })
    },
    setManagementTypes(enabledManagementTypes) {
      this.managementTypes = Constants.ManagementTypes.map((x) =>
        Object.assign(x, {
          disabled: enabledManagementTypes.indexOf(x.value) === -1,
        })
      )
    },
    setProductionTypes(enabledProductionTypes) {
      const whitelistedProductionTypes = []
      const [centralQuery, siteQuery] = Constants.ProductionTypes.map((x) => x.value)
      if (enabledProductionTypes.indexOf("site") > -1 || enabledProductionTypes.indexOf("site_cooked_elsewhere") > -1) {
        whitelistedProductionTypes.push(siteQuery)
      }
      if (enabledProductionTypes.indexOf("central") > -1 || enabledProductionTypes.indexOf("central_serving") > -1) {
        whitelistedProductionTypes.push(centralQuery)
      }
      this.productionTypes = Constants.ProductionTypes.map((x) =>
        Object.assign(x, {
          disabled: whitelistedProductionTypes.indexOf(x.value) === -1,
        })
      )
    },
    toggleOrderDirection() {
      this.orderDescending = !this.orderDescending
      this.page = 1 // reset page to 1 when changing order direction
    },
  },
  watch: {
    filters: {
      handler() {
        this.applyFilter()
      },
      deep: true,
    },
    page() {
      this.changePage()
    },
    orderBy() {
      this.updateOrder()
    },
    orderDescending() {
      this.updateOrder()
    },
    $route() {
      this.populateParameters()
    },
  },
  mounted() {
    this.populateParameters()
    if (this.hasActiveFilter) this.showFilters = true
  },
}
</script>

<style scoped>
.v-btn--plain:not(.v-btn--active):not(.v-btn--loading):not(:focus):not(:hover) >>> .v-btn__content {
  opacity: 1;
}
.active-filter-label {
  font-weight: bold;
}
.active-filter-label::before {
  content: "⚫︎";
  color: #ce614a;
}
div >>> .v-list-item--disabled .theme--light.v-icon {
  color: rgba(0, 0, 0, 0.22);
}
#ordering >>> .v-select__selection {
  font-size: 12px;
}
</style>
