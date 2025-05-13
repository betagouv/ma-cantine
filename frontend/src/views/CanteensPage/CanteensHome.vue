<template>
  <div class="text-left fr-text">
    <BreadcrumbsNav :links="[{ to: { name: 'CanteenSearchLanding' } }]" />
    <div>
      <h1 class="fr-h1 hidden">Les cantines</h1>
      <v-row id="search-and-ordering" align="end">
        <v-col cols="12" md="4">
          <form role="search" onsubmit="return false">
            <h2 class="fr-h5 mb-2">Rechercher</h2>
            <DsfrSearchField
              hide-details="auto"
              ref="search"
              v-model="searchTerm"
              placeholder="Recherche par nom ou SIRET"
              @search="search"
              clearable
              @clear="clearSearch"
            />
          </form>
        </v-col>
        <v-col id="ordering" cols="12" sm="6" md="3" class="d-flex align-end">
          <DsfrNativeSelect v-model="orderBy" :items="orderOptions" hide-details label="Trier par" class="mb-n1" />
          <v-btn
            icon
            @click="toggleOrderDirection"
            :title="`Resultats affichés en ordre ${orderDescending ? 'décroissant' : 'croissant'}`"
            plain
          >
            <v-icon color="primary" v-if="orderDescending">mdi-arrow-down</v-icon>
            <v-icon color="primary" v-else>
              mdi-arrow-up
            </v-icon>
          </v-btn>
        </v-col>
      </v-row>
      <v-row
        id="filters-and-results"
        :class="{ 'pt-4': true, 'min-height': !visibleCanteens || visibleCanteens.length === limit }"
      >
        <v-col id="filters" cols="12" md="4">
          <h3 class="fr-h6 mb-0">
            Filtrer
          </h3>
          <v-form class="mt-4">
            <DsfrAccordion
              :items="[
                { id: 'territory', icon: '$road-map-fill', text: 'Par territoire', titleLevel: 'h4' },
                { id: 'characteristic', icon: '$community-fill', text: 'Par caractéristique', titleLevel: 'h4' },
              ]"
            >
              <template v-slot:title="{ item }">
                <span class="d-flex">
                  <v-icon color="primary" class="mr-2">{{ item.icon }}</v-icon>
                  {{ item.text }}
                </span>
              </template>
              <template v-slot:content="{ item }">
                <div v-if="item.id === 'territory'">
                  <LocationSelect
                    locationType="region"
                    v-model="filters.region.value"
                    :labelClasses="{ 'active-filter-label': !!filters.region.value }"
                    class="mb-4"
                    :selectableOptions="selectableRegions"
                    :unselectableOptionsHeader="unselectableRegionsHeader"
                  />
                  <LocationSelect
                    locationType="department"
                    v-model="filters.department.value"
                    :labelClasses="{ 'active-filter-label': !!filters.department.value }"
                    class="mb-4"
                    :selectableOptions="selectableDepartments"
                    :unselectableOptionsHeader="unselectableDepartmentsHeader"
                  />
                  <label
                    for="select-commune"
                    :class="{
                      'active-filter-label': !!filters.city_insee_code.value,
                    }"
                  >
                    Commune
                  </label>
                  <CityField
                    :inseeCode.sync="filters.city_insee_code.value"
                    clearable
                    hide-details
                    id="select-commune"
                    placeholder="Toutes les communes"
                    class="mt-1 mb-4"
                    @locationUpdate="setLocation"
                  />
                </div>
                <div v-if="item.id === 'characteristic'">
                  <label
                    for="select-sector"
                    :class="{
                      'fr-text': true,
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
                    class="mt-1 mb-4"
                  />
                  <DsfrRadio
                    v-model="filters.management_type.value"
                    :items="managementTypes"
                    :optionsRow="$vuetify.breakpoint.mdAndUp"
                    label="Mode de gestion"
                    :labelClasses="{
                      'fr-text text-left grey--text text--darken-4': true,
                      'active-filter-label': !!filters.management_type.value,
                    }"
                    :hideOptional="true"
                    class="mb-n2"
                  />

                  <DsfrNativeSelect
                    v-model="filters.production_type.value"
                    :items="productionTypes"
                    label="Type d'établissement"
                    :labelClasses="{
                      'mb-1 fr-text text-left': true,
                      'active-filter-label': !!filters.production_type.value,
                    }"
                    class="mb-4"
                  />
                  <fieldset class="mb-4">
                    <legend
                      :class="{
                        'active-filter-label': !!filters.min_portion_bio.value || !!filters.min_portion_combined.value,
                      }"
                    >
                      Dans les assiettes, part minimum de...
                    </legend>
                    <div class="d-flex mt-1">
                      <DsfrTextField
                        label="bio"
                        labelClasses="caption pl-1"
                        :value="filters.min_portion_bio.value"
                        ref="min_portion_bio"
                        :rules="[validators.nonNegativeOrEmpty, validators.lteOrEmpty(100)]"
                        @change="onChangeIntegerFilter('min_portion_bio')"
                        hide-details="auto"
                        append-icon="mdi-percent"
                        placeholder="0"
                        :hideOptional="true"
                        class="mr-2"
                      />
                      <DsfrTextField
                        label="bio, qualité et durable"
                        labelClasses="caption pl-1"
                        :value="filters.min_portion_combined.value"
                        ref="min_portion_combined"
                        :rules="[validators.nonNegativeOrEmpty, validators.lteOrEmpty(100)]"
                        @change="onChangeIntegerFilter('min_portion_combined')"
                        hide-details="auto"
                        placeholder="0"
                        append-icon="mdi-percent"
                        :hideOptional="true"
                        class="ml-2"
                      />
                    </div>
                  </fieldset>
                  <fieldset class="mb-4">
                    <legend
                      :class="{
                        'active-filter-label':
                          !!filters.min_daily_meal_count.value || !!filters.max_daily_meal_count.value,
                      }"
                    >
                      Repas par jour
                    </legend>
                    <div class="d-flex mt-1">
                      <div>
                        <DsfrTextField
                          label="minimum"
                          labelClasses="caption"
                          :value="filters.min_daily_meal_count.value"
                          ref="min_daily_meal_count"
                          :rules="[validators.nonNegativeOrEmpty]"
                          @change="onChangeIntegerFilter('min_daily_meal_count')"
                          hide-details="auto"
                          :hideOptional="true"
                          class="mr-2"
                        />
                      </div>
                      <div>
                        <DsfrTextField
                          label="maximum"
                          labelClasses="caption"
                          :value="filters.max_daily_meal_count.value"
                          ref="max_daily_meal_count"
                          :rules="[validators.nonNegativeOrEmpty]"
                          @change="onChangeIntegerFilter('max_daily_meal_count')"
                          hide-details="auto"
                          :hideOptional="true"
                          class="ml-2"
                        />
                      </div>
                    </div>
                  </fieldset>
                  <DsfrNativeSelect
                    v-model="filters.badge.value"
                    :items="badges"
                    label="Expertise EGalim"
                    :labelClasses="{
                      'mb-1 fr-text text-left': true,
                      'active-filter-label': !!filters.badge.value,
                    }"
                    class="mb-4"
                  />
                </div>
              </template>
            </DsfrAccordion>
          </v-form>
        </v-col>
        <v-col id="results" cols="12" md="8" class="d-flex flex-column">
          <div v-if="loading" class="d-flex align-center">
            <v-progress-circular indeterminate class="align-self-center" />
            <p class="mb-0 ml-4">Patience le chargement de la page peut prendre une dizaine de secondes</p>
          </div>
          <div v-else class="d-flex flex-column" style="height: 100%;">
            <div class="d-flex">
              <ResultCount :count="publishedCanteenCount" class="fr-h6 mb-0" />

              <v-btn text color="primary" small @click="clearFilters" v-if="hasActiveFilter" class="mb-1">
                <v-icon small>mdi-filter-off-outline</v-icon>
                Enlever tous les filtres
              </v-btn>
            </div>
            <DsfrTagGroup
              :tags="filterTags"
              :closeable="true"
              @closeTag="(tag) => removeFilter(tag)"
              class="mt-2 mb-6"
            />
            <div v-if="publishedCanteenCount === 0" class="d-flex flex-column align-center py-10">
              <v-icon large>mdi-inbox-remove</v-icon>
              <p class="text-body-1 grey--text text--darken-1 my-2">
                Nous n'avons pas trouvé des cantines avec ces paramètres
              </p>
              <v-btn
                color="primary"
                text
                @click="clearFilters"
                class="text-decoration-underline"
                v-if="hasActiveFilter"
              >
                Désactiver tous les filtres
              </v-btn>
            </div>
            <v-progress-circular v-else-if="pageLoading" indeterminate class="mt-8 align-self-center" />
            <div v-else>
              <v-spacer />
              <PublishedCanteenCard
                v-for="canteen in visibleCanteens"
                :key="canteen.id"
                :canteen="canteen"
                class="my-4"
              />
              <v-spacer />
            </div>
            <v-spacer />
            <DsfrPagination
              class="my-6"
              v-model="page"
              :length="Math.ceil(publishedCanteenCount / limit)"
              :total-visible="5"
              v-if="publishedCanteenCount"
              @input="scrollTop"
            />
          </div>
        </v-col>
      </v-row>
    </div>

    <v-divider aria-hidden="true" role="presentation" class="mb-8 mt-12"></v-divider>

    <v-row class="mb-6" style="position: relative">
      <v-col cols="3" v-if="$vuetify.breakpoint.smAndUp">
        <div class="fill-height d-flex flex-column align-center">
          <v-spacer></v-spacer>
          <v-img src="/static/images/doodles-dsfr/primary/SittingDoodle.png" contain></v-img>
          <v-spacer></v-spacer>
        </div>
      </v-col>
      <v-col>
        <h2 class="text-h6 font-weight-black mb-4">
          Vous n'avez pas trouvé un ou plusieurs établissements qui vous intéressent ?
        </h2>
        <p class="body-2 mb-6">
          Dites-nous tout, nous ferons en sorte de leur communiquer votre intérêt pour leurs initiatives en place.
        </p>
        <v-form v-model="formIsValid" ref="form" @submit.prevent>
          <DsfrEmail v-model="fromEmail" />
          <DsfrFullName v-model="name" />
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
import { getObjectDiff, sectorsSelectList } from "@/utils"
import validators from "@/validators"
import Constants from "@/constants"
import badges from "@/badges"
import BreadcrumbsNav from "@/components/BreadcrumbsNav"
import DsfrAccordion from "@/components/DsfrAccordion"
import DsfrTextField from "@/components/DsfrTextField"
import DsfrRadio from "@/components/DsfrRadio"
import DsfrSelect from "@/components/DsfrSelect"
import DsfrNativeSelect from "@/components/DsfrNativeSelect"
import DsfrTextarea from "@/components/DsfrTextarea"
import DsfrPagination from "@/components/DsfrPagination"
import DsfrSearchField from "@/components/DsfrSearchField"
import CityField from "@/views/CanteenEditor/CityField"
import DsfrTagGroup from "@/components/DsfrTagGroup"
import DsfrEmail from "@/components/DsfrEmail"
import DsfrFullName from "@/components/DsfrFullName"
import LocationSelect from "@/components/LocationSelect"
import ResultCount from "@/components/ResultCount"

const DEFAULT_ORDER = "creation"

export default {
  components: {
    PublishedCanteenCard,
    BreadcrumbsNav,
    DsfrAccordion,
    DsfrTextField,
    DsfrRadio,
    DsfrSelect,
    DsfrNativeSelect,
    DsfrTextarea,
    DsfrPagination,
    DsfrSearchField,
    CityField,
    DsfrTagGroup,
    DsfrEmail,
    DsfrFullName,
    LocationSelect,
    ResultCount,
  },
  data() {
    const sectors = this.$store.state.sectors
    const user = this.$store.state.loggedUser
    return {
      limit: 15,
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
          displayName(value) {
            const department = jsonDepartments.find((d) => d.departmentCode === value)
            return department && `${department.departmentName} (${value})`
          },
        },
        region: {
          param: "region",
          value: null,
          default: null,
          displayName(value) {
            const region = jsonRegions.find((d) => d.regionCode === value)
            return region.regionName
          },
        },
        city_insee_code: {
          param: "commune",
          value: null,
          default: null,
          displayNameComputed: "locationDisplay",
        },
        management_type: {
          param: "modeDeGestion",
          value: null,
          default: null,
          displayName(value) {
            const mt = Constants.ManagementTypes.find((pt) => pt.value === value)?.text || value
            return `Gestion ${mt.toLowerCase()}`
          },
        },
        production_type: {
          param: "typeEtablissement",
          value: null,
          default: null,
          displayName(value) {
            return Constants.ProductionTypes.find((pt) => pt.value === value)?.text
          },
        },
        sectors: {
          param: "secteurs",
          value: [],
          default: [],
          transformToFrontend(values) {
            if (!values) return
            return Array.isArray(values) ? values.map((v) => +v) : [+values]
          },
          displayName(value) {
            value = +value
            return sectors.find((s) => s.id === value)?.name || value
          },
        },
        min_daily_meal_count: {
          param: "minRepasJour",
          value: null,
          default: null,
          displayName(value) {
            return `Repas min : ${value}`
          },
        },
        max_daily_meal_count: {
          param: "maxRepasJour",
          value: null,
          default: null,
          displayName(value) {
            return `Repas max : ${value}`
          },
        },
        min_portion_bio: {
          param: "minBio",
          value: null,
          default: null,
          transformToBackend(value) {
            return value / 100
          },
          displayName(value) {
            return `Bio min : ${value} %`
          },
        },
        min_portion_combined: {
          param: "minQualite",
          value: null,
          default: null,
          transformToBackend(value) {
            return value / 100
          },
          displayName(value) {
            return `EGalim min : ${value} %`
          },
        },
        badge: {
          param: "badge",
          value: null,
          default: null,
          displayName(value) {
            return badges[value]?.title
          },
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
      location: undefined,
      selectableDepartments: undefined,
      selectableRegions: undefined,
    }
  },
  computed: {
    loading() {
      return this.publishedCanteenCount === null
    },
    pageLoading() {
      return this.visibleCanteens === null
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
      if (this.searchTerm) query.recherche = this.searchTerm
      return query
    },
    hasActiveFilter() {
      return Object.values(this.filters).some((f) => !!f.value && f.value.length)
    },
    validators() {
      return validators
    },
    resultsCountText() {
      if (!this.publishedCanteenCount) return null
      else if (!this.hasActiveFilter && !this.searchTerm) return null

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
    filterTags() {
      const activeFilters = Object.entries(this.filters).filter(([, f]) => !!f.value)
      const tags = activeFilters
        .filter(([, f]) => !Array.isArray(f.default))
        .map(([key, filter]) => {
          const text = filter.displayNameComputed
            ? this[filter.displayNameComputed]
            : filter.displayName && filter.displayName(filter.value)
          return {
            id: key,
            key,
            text: text || `${filter.param} : ${filter.value}`,
          }
        })
      const arrayFilters = activeFilters.filter(([, f]) => Array.isArray(f.default))
      arrayFilters.forEach(([key, filter]) => {
        const arrayTags = filter.value.map((fv, idx) => {
          const text = filter.displayName && filter.displayName(fv)
          return {
            id: `${key}[${idx}]`,
            key,
            idx: idx,
            isArray: true,
            text: text || `${filter.param} : ${fv}`,
          }
        })
        tags.push(...arrayTags)
      })
      return tags
    },
    locationDisplay() {
      return this.location?.city
    },
    unselectableDepartmentsHeader() {
      const locationsWord = "départements"
      return this.hasActiveFilter || this.searchTerm
        ? `Ces ${locationsWord} ne contiennent pas d'établissements correspondant à votre recherche :`
        : `Nous n'avons pas encore d'établissements dans ces ${locationsWord} :`
    },
    unselectableRegionsHeader() {
      const locationsWord = "régions"
      return this.hasActiveFilter || this.searchTerm
        ? `Ces ${locationsWord} ne contiennent pas d'établissements correspondant à votre recherche :`
        : `Nous n'avons pas encore d'établissements dans ces ${locationsWord} :`
    },
  },
  methods: {
    fetchCurrentPage() {
      this.visibleCanteens = null // trigger this.pageLoading
      let queryParam = `limit=${this.limit}&offset=${this.offset}`
      if (this.searchTerm) queryParam += `&search=${this.searchTerm}`
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
          if (response.status === 400) {
            return Promise.reject("Bad request")
          } else if (response.status < 200 || response.status > 400) throw new Error(`Error encountered : ${response}`)
          return response.json()
        })
        .then((response) => {
          this.publishedCanteenCount = response.count
          this.visibleCanteens = response.results
          this.selectableDepartments = response.departments
          this.selectableRegions = response.regions
          this.setSectors(response.sectors)
          this.setManagementTypes(response.managementTypes)
          this.setProductionTypes(response.productionTypes)
        })
        .catch((e) => {
          this.publishedCanteenCount = 0
          this.visibleCanteens = 0
          if (e !== "Bad request") this.$store.dispatch("notifyServerError", e)
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
      const override = this.order ? { page: 1, trier: this.order.display } : { page: 1 }
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
      // urls are always strings. Some query params are not strings.
      // Ensure like-for-like comparison by treating the url query params before check
      // https://github.com/betagouv/ma-cantine/issues/2773
      const urlQuery = JSON.parse(JSON.stringify(this.$route.query))
      Object.values(this.filters).forEach((f) => {
        if (f.transformToFrontend && urlQuery[f.param]) {
          urlQuery[f.param] = f.transformToFrontend(this.$route.query[f.param])
        }
      })

      const changedKeys = Object.keys(getObjectDiff(this.query, urlQuery))
      const shouldNavigate = changedKeys.length > 0
      if (shouldNavigate) {
        this.page = 1
        this.updateRouter(Object.assign(this.query, { page: 1 }))
        this.publishedCanteenCount = null // trigger this.loading
      }
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
    removeFilter(filterTag) {
      if (filterTag.isArray) {
        this.filters[filterTag.key].value.splice(filterTag.idx, 1)
      } else {
        this.filters[filterTag.key].value = this.filters[filterTag.id].default
      }
    },
    setLocation(location) {
      this.location = location
    },
    scrollTop() {
      window.scrollTo(0, 0)
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
div >>> .active-filter-label {
  font-weight: bold;
}
div >>> .active-filter-label::before {
  content: "⚫︎";
  color: #ce614a;
}
div >>> .v-list-item--disabled .theme--light.v-icon {
  color: rgba(0, 0, 0, 0.22);
}
#ordering >>> .v-select__selection {
  font-size: 12px;
}
/* TODO: fix min height now that we have filter tags to take into account */
#filters-and-results.min-height {
  min-height: 1050px;
}
h1.hidden {
  clip: rect(1px, 1px, 1px, 1px);
  height: 1px;
  overflow: hidden;
  position: absolute;
  white-space: nowrap;
  width: 1px;
  z-index: -1;
  user-select: none;
}
</style>
