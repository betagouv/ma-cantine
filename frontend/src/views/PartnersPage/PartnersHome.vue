<template>
  <div class="text-left">
    <BreadcrumbsNav />
    <v-row>
      <v-col cols="12" sm="7" md="8">
        <h1 class="font-weight-black text-h5 text-sm-h4 mb-4">
          Améliorer votre offre avec le soutien des acteurs de l'éco-système
        </h1>
        <ReferencingInfo />
      </v-col>
      <v-col cols="0" sm="5" md="4" v-if="$vuetify.breakpoint.smAndUp" class="py-0 pr-8 d-flex">
        <v-spacer></v-spacer>
        <v-img src="/static/images/peeps-illustration-couple.png" contain max-width="200"></v-img>
      </v-col>
    </v-row>
    <p v-if="$vuetify.breakpoint.mdAndUp" class="font-weight-bold">Vos besoins</p>
    <v-item-group v-if="$vuetify.breakpoint.mdAndUp" multiple v-model="filters.category.value">
      <v-row>
        <v-col v-for="category in categoryItems" cols="4" :key="category.value" class="pa-1" fill-height>
          <v-item v-slot="{ active, toggle }" :value="category.value">
            <button @click="toggle" style="width: inherit;" class="fill-height">
              <v-card :color="active ? 'primary lighten-4' : ''" outlined class="fill-height">
                <v-card-title class="text-body-2 d-block text-left">
                  <v-icon small class="mr-2" :color="active ? 'primary' : ''">
                    {{ category.icon }}
                  </v-icon>
                  {{ category.text }}
                </v-card-title>
              </v-card>
            </button>
          </v-item>
        </v-col>
      </v-row>
    </v-item-group>
    <div class="d-flex align-center mt-8 pl-0">
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
      <v-sheet class="pa-6 text-left mt-2 ma-0" v-show="showFilters" rounded :outlined="showFilters">
        <v-row>
          <v-col cols="12" sm="6" v-if="$vuetify.breakpoint.smAndDown">
            <label
              for="select-category"
              :class="{
                'text-body-2': true,
                'active-filter-label': filters.category.value && !!filters.category.value.length,
              }"
            >
              Besoin(s) comblé(s) par l'acteur
            </label>
            <DsfrSelect
              v-model="filters.category.value"
              multiple
              :items="categoryItems"
              clearable
              hide-details
              id="select-category"
              placeholder="Tous les besoins"
              class="mt-1"
            />
          </v-col>
          <v-col cols="12" sm="6">
            <label
              for="select-department"
              :class="{
                'text-body-2': true,
                'active-filter-label': filters.department.value && !!filters.department.value.length,
              }"
            >
              Département
            </label>
            <DsfrCombobox
              v-model="filters.department.value"
              multiple
              :items="departmentItems"
              clearable
              hide-details
              id="select-department"
              placeholder="Tous les départements"
              class="mt-1"
            />
          </v-col>
          <v-col cols="12" sm="6">
            <label
              for="select-sector"
              :class="{
                'text-body-2': true,
                'active-filter-label': filters.sectorCategories.value && !!filters.sectorCategories.value.length,
              }"
            >
              Secteur d'activité
            </label>
            <DsfrSelect
              v-model="filters.sectorCategories.value"
              multiple
              :items="sectorCategories"
              clearable
              hide-details
              id="select-sector"
              placeholder="Tous les secteurs"
              class="mt-1"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" sm="6">
            <label
              for="select-type"
              :class="{
                'text-body-2': true,
                'active-filter-label': filters.type.value && !!filters.type.value.length,
              }"
            >
              Type d'acteur
            </label>
            <DsfrSelect
              v-model="filters.type.value"
              multiple
              :items="typeItems"
              clearable
              hide-details
              id="select-type"
              placeholder="Tous les types"
              class="mt-1"
            />
          </v-col>
          <v-col cols="6">
            <label
              for="select-gratuity-option"
              :class="{
                'text-body-2': true,
                'active-filter-label': filters.gratuityOption.value && !!filters.gratuityOption.value.length,
              }"
            >
              Type d'offre
            </label>
            <DsfrSelect
              v-model="filters.gratuityOption.value"
              multiple
              :items="gratuityOptions"
              clearable
              hide-details
              id="select-gratuity-option"
              placeholder="Toutes"
              class="mt-1"
            />
          </v-col>
        </v-row>
      </v-sheet>
    </v-expand-transition>
    <div class="mt-3">
      <v-row v-if="!!partnerCount">
        <v-spacer></v-spacer>
        <v-col cols="12" sm="6">
          <DsfrPagination
            v-model="page"
            :length="Math.ceil(partnerCount / limit)"
            :total-visible="7"
            v-if="!!partnerCount"
          />
        </v-col>
        <v-spacer></v-spacer>
      </v-row>
      <v-row v-if="!!partnerCount">
        <v-col v-for="partner in visiblePartners" :key="partner.id" style="height: auto;" cols="12" sm="6" md="4">
          <PartnerCard :partner="partner" />
        </v-col>
        <v-col style="height: auto;" cols="12" sm="6" md="4">
          <NewPartnerCard />
        </v-col>
      </v-row>
      <v-row v-else>
        <v-col cols="12">
          <div class="d-flex flex-column align-center py-0">
            <p class="text-body-1 grey--text text--darken-1 my-2">
              <v-icon class="mr-1 mt-n1">mdi-inbox-remove</v-icon>
              Nous n'avons pas trouvé des acteurs avec ces paramètres
            </p>
            <v-btn color="primary" text @click="clearFilters" class="text-decoration-underline" v-if="hasActiveFilter">
              Désactiver tous les filtres
            </v-btn>
          </div>
        </v-col>
        <v-col style="height: auto;" cols="12" sm="6" md="4">
          <NewPartnerCard />
        </v-col>
      </v-row>
    </div>
    <v-divider class="mb-8 mt-12"></v-divider>
    <v-row>
      <v-col cols="12">
        <h2 class="text-h6 font-weight-black mb-4">
          Vous n'avez pas trouvé un ou plusieurs acteurs qui vous intéressent ?
        </h2>
        <p class="body-2">
          Dites-nous tout, nous ferons en sorte de vous aider.
        </p>
        <GeneralContactForm initialInquiryType="other"></GeneralContactForm>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import Constants from "@/constants"
import BreadcrumbsNav from "@/components/BreadcrumbsNav"
import DsfrPagination from "@/components/DsfrPagination"
import DsfrSelect from "@/components/DsfrSelect"
import DsfrCombobox from "@/components/DsfrCombobox"
import PartnerCard from "@/views/PartnersPage/PartnerCard"
import NewPartnerCard from "@/views/PartnersPage/NewPartnerCard"
import GeneralContactForm from "@/components/GeneralContactForm"
import ReferencingInfo from "./ReferencingInfo"
import { getObjectDiff, departmentItems } from "@/utils"

export default {
  name: "PartnersHome",
  components: {
    BreadcrumbsNav,
    DsfrPagination,
    DsfrSelect,
    DsfrCombobox,
    PartnerCard,
    NewPartnerCard,
    GeneralContactForm,
    ReferencingInfo,
  },
  data() {
    return {
      limit: 5,
      page: this.$route.query.page,
      types: [],
      visiblePartners: null,
      partnerCount: null,
      filters: {
        gratuityOption: {
          param: "gratuit",
          value: [],
          default: [],
        },
        category: {
          param: "besoin",
          value: [],
          default: [],
        },
        department: {
          param: "departement",
          value: [],
          default: [],
        },
        sectorCategories: {
          param: "secteur",
          value: [],
          default: [],
        },
        type: {
          param: "type",
          value: [],
          default: [],
        },
      },
      showFilters: false,
      categoryItems: [
        {
          value: "appro",
          text: "Améliorer ma part de bio et de produits durables",
          icon: "$leaf-fill",
        },
        {
          value: "suivi",
          text: "Assurer mon suivi d'approvisionnement",
          icon: "$survey-fill",
        },
        {
          value: "waste",
          text: "Diagnostiquer mon gaspillage",
          icon: "$delete-fill",
        },

        {
          value: "asso",
          text: "Donner à une association",
          icon: "$user-heart-fill",
        },
        {
          value: "vege",
          text: "Diversifier mes sources de protéines et atteindre l'équilibre alimentaire des menus",
          icon: "mdi-barley",
        },
        {
          value: "plastic",
          text: "Substituer mes plastiques",
          icon: "$recycle-fill",
        },
        {
          value: "training",
          text: "Me former ou former mon personnel (formation qualifiante)",
          icon: "$team-fill",
        },
        {
          value: "network",
          text: "Me mettre en réseau avec les acteurs du terrain",
          icon: "$user-add-fill",
        },
        {
          value: "financial",
          text: "Obtenir une aide financière / matérielle",
          icon: "$money-euro-box-fill",
        },
      ],
      // Need to create a deep copy to avoid modiifying the array elsewhere in the app
      departmentItems: JSON.parse(JSON.stringify(departmentItems)),
      sectorCategories: [],
      typeItems: [],
      gratuityOptions: [
        {
          value: "free",
          text: "Gratuit",
        },
        {
          value: "paid",
          text: "Payant",
        },
        {
          value: "mix",
          text: "Mixte",
        },
      ],
    }
  },
  computed: {
    loading() {
      return this.partnerCount === null
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
      return query
    },
    hasActiveFilter() {
      const activeMobileFilters = Object.values(this.filters).filter((f) => !!f.value && f.value.length)
      const activeDesktopFilters = activeMobileFilters.filter((f) => f.param !== "besoin")
      const breakpoint = this.$vuetify.breakpoint
      return (
        (breakpoint.smAndDown && activeMobileFilters.length > 0) ||
        (breakpoint.mdAndUp && activeDesktopFilters.length > 0)
      )
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
        } else if (f.value) queryParam += `&${key}=${f.value}`
      })
      return fetch(`/api/v1/partners/?${queryParam}`)
        .then((response) => {
          if (response.status < 200 || response.status >= 400) throw new Error(`Error encountered : ${response}`)
          return response.json()
        })
        .then((response) => {
          this.partnerCount = response.count
          this.visiblePartners = response.results
          this.typeItems = response.types
          this.setDepartments(response.departments)
          this.setSectorCategories(response.sectorCategories)
        })
        .catch((e) => {
          this.partnerCount = 0
          this.$store.dispatch("notifyServerError", e)
        })
    },
    populateParameters() {
      Object.values(this.filters).forEach((f) => {
        f.value = this.$route.query[f.param]
        if (f.transformToFrontend) f.value = f.transformToFrontend(f.value)
      })
      this.page = this.$route.query.page ? parseInt(this.$route.query.page) : 1
      this.fetchCurrentPage()
    },
    changePage() {
      const query = Object.assign(this.query, { page: this.page || 1 })
      this.updateRouter(query)
    },
    updateRouter(query) {
      if (this.$route.query.page) {
        this.$router.push({ query }).catch(() => {})
      } else {
        this.$router.replace({ query }).catch(() => {})
      }
    },
    applyFilter() {
      const changedKeys = Object.keys(getObjectDiff(this.query, this.$route.query))
      const shouldNavigate = changedKeys.length > 0
      if (shouldNavigate) {
        this.page = 1
        this.updateRouter(Object.assign(this.query, { page: 1 }))
      }
    },
    clearFilters() {
      Object.entries(this.filters).forEach(([key, f]) => {
        this.filters[key].value = f.default
      })
    },
    setLocations(enabledLocationIds) {
      const enabledLocations = this.departmentItems.filter((x) => enabledLocationIds.indexOf(x.value) > -1)
      const header = { header: `Nous n'avons pas encore de partenaires dans ces departements :` }
      const divider = { divider: true }

      const disabledLocations = this.departmentItems
        .filter((x) => enabledLocationIds.indexOf(x.value) === -1)
        .map((x) => Object.assign(x, { disabled: true }))

      return [...enabledLocations, divider, header, ...disabledLocations]
    },
    setDepartments(enabledDepartmentIds) {
      this.departmentItems = this.setLocations(enabledDepartmentIds)
    },
    setSectorCategories(enabledSectorCategories) {
      const header = { header: `Nous n'avons pas encore de partenaires dans ces domaines :` }
      const divider = { divider: true }
      const disabledCategories = Object.keys(Constants.SectorCategoryTranslations)
        .filter((x) => !enabledSectorCategories.includes(x) && x !== "inconnu")
        .map((x) => {
          return {
            text: Constants.SectorCategoryTranslations[x],
            value: x,
            disabled: true,
          }
        })
      const enabledCategories = enabledSectorCategories.map((x) => {
        return {
          text: Constants.SectorCategoryTranslations[x],
          value: x,
        }
      })
      this.sectorCategories = [...enabledCategories, divider, header, ...disabledCategories]
    },
  },
  watch: {
    page() {
      this.changePage()
    },
    $route() {
      this.populateParameters()
    },
    filters: {
      handler() {
        this.applyFilter()
      },
      deep: true,
    },
  },
  mounted() {
    if (this.page) {
      this.populateParameters()
    } else {
      // this will cause a redirect to the URL with the good params
      this.page = 1
    }
  },
}
/*
# How the filters work:

## When the user picks a filter

The filters watcher detects a change in the filter object, triggering applyFilter
applyFilter resets the page to 1 and called updateRouter
updateRouter either pushes or replaces with the new query to the $router...
...causing the $route watcher to call populateParameters
populateParameters sets the values of the filters based on the URL query params and then triggers fetching data

## When the user loads a URL with filters

mounted triggers populateParameters
which after setting the query data, triggers fetching data

*/
</script>

<style scoped>
.active-filter-label {
  font-weight: bold;
}
.active-filter-label::before {
  content: "⚫︎";
  color: #ce614a;
}
.v-item-group >>> .v-card--link:focus::before {
  opacity: 0;
}
.v-item-group >>> .v-card {
  user-select: none;
}
</style>
