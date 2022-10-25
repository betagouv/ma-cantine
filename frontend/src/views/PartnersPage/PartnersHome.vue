<template>
  <div class="text-left">
    <BreadcrumbsNav :links="[{ to: { name: 'CommunityPage' } }]" />
    <v-row>
      <v-col cols="12" sm="7" md="8">
        <h1 class="font-weight-black text-h5 text-sm-h4 mb-4">
          Améliorer votre offre avec le soutien des partenaires
        </h1>
        <p>
          Ces acteurs de la restauration collective au service des gestionnaires sont prêts pour vous aidez à atteindre
          les objectifs de votre cantine
        </p>
      </v-col>
      <v-col cols="0" sm="5" md="4" v-if="$vuetify.breakpoint.smAndUp" class="py-0 pr-8 d-flex">
        <v-spacer></v-spacer>
        <v-img src="/static/images/peeps-illustration-couple.png" contain max-width="140"></v-img>
      </v-col>
    </v-row>
    <p v-if="$vuetify.breakpoint.mdAndUp" class="font-weight-bold">Vos besoins</p>
    <v-item-group v-if="$vuetify.breakpoint.mdAndUp" multiple v-model="filters.category.value">
      <v-row>
        <v-col v-for="category in categoryItems" cols="4" :key="category.value" class="pa-1">
          <v-item v-slot="{ active, toggle }" :value="category.value">
            <button @click="toggle" style="width: inherit;">
              <v-card :color="active ? 'primary lighten-4' : ''" outlined>
                <v-card-title class="text-body-2">
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
      <v-sheet class="pa-6 text-left mt-2 mx-md-6" v-show="showFilters" rounded :outlined="showFilters">
        <v-row>
          <v-col cols="12" sm="6" v-if="$vuetify.breakpoint.smAndDown">
            <label
              for="select-category"
              :class="{
                'text-body-2': true,
                'active-filter-label': filters.category.value && !!filters.category.value.length,
              }"
            >
              Besoin(s) comblé(s) par le partenaire
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
        </v-row>
        <v-row>
          <v-col cols="12" sm="6">
            <label
              for="select-type"
              :class="{ 'text-body-2': true, 'active-filter-label': filters.type.value && !!filters.type.value.length }"
            >
              Type
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
            <v-checkbox hide-details="auto" class="mt-sm-9" v-model="filters.free.value" label="Gratuit" />
          </v-col>
        </v-row>
      </v-sheet>
    </v-expand-transition>
    <v-row class="mt-3">
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
    </v-row>
    <div v-else class="d-flex flex-column align-center py-6">
      <v-icon large>mdi-inbox-remove</v-icon>
      <p class="text-body-1 grey--text text--darken-1 my-2">
        Nous n'avons pas trouvé des partenaires avec ces paramètres
      </p>
      <v-btn color="primary" text @click="clearFilters" class="text-decoration-underline" v-if="hasActiveFilter">
        Désactiver tous les filtres
      </v-btn>
    </div>
    <v-divider class="mb-8 mt-12"></v-divider>
    <v-row>
      <v-col cols="12">
        <h2 class="text-h6 font-weight-black mb-4">
          Vous n'avez pas trouvé un ou plusieurs partenaires ou prestataires qui vous intéressent ?
        </h2>
        <p class="body-2">
          Dites-nous tout, nous ferons en sorte de vous aider.
        </p>
        <p class="body-2">
          Si vous êtes un acteur de la restauration collective, décrivez-nous votre offre et nous vous ajoutons !
        </p>
        <GeneralContactForm initialInquiryType="other"></GeneralContactForm>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import BreadcrumbsNav from "@/components/BreadcrumbsNav"
import DsfrPagination from "@/components/DsfrPagination"
import DsfrSelect from "@/components/DsfrSelect"
import DsfrCombobox from "@/components/DsfrCombobox"
import PartnerCard from "@/views/PartnersPage/PartnerCard"
import GeneralContactForm from "@/components/GeneralContactForm"
import { getObjectDiff } from "@/utils"
import jsonDepartments from "@/departments.json"

export default {
  name: "PartnersHome",
  components: { BreadcrumbsNav, DsfrPagination, DsfrSelect, DsfrCombobox, PartnerCard, GeneralContactForm },
  data() {
    return {
      limit: 6,
      page: this.$route.query.page,
      types: [],
      visiblePartners: null,
      partnerCount: null,
      filters: {
        free: {
          param: "gratuit",
          value: undefined, // will be set from URL query
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
        type: {
          param: "type",
          value: [],
          default: [],
        },
      },
      showFilters: false,
      categoryItems: [
        {
          value: "plastic",
          text: "Substituer mes plastiques",
          icon: "$recycle-fill",
        },
        {
          value: "asso",
          text: "Donner à une association",
          icon: "$user-heart-fill",
        },
        {
          value: "waste",
          text: "Diagnostiquer mon gaspillage",
          icon: "$delete-fill",
        },
        {
          value: "training",
          text: "Me former ou former mon personnel",
          icon: "$team-fill",
        },
        {
          value: "appro",
          text: "Améliorer ma part de bio / durable",
          icon: "$leaf-fill",
        },
        {
          value: "vege",
          text: "Diversifier mes sources de protéines",
          icon: "mdi-barley",
        },
        {
          value: "suivi",
          text: "Assurer mon suivi d'approvisionnement",
          icon: "$survey-fill",
        },
      ],
      departmentItems: jsonDepartments.map((x) => ({
        text: `${x.departmentCode} - ${x.departmentName}`,
        value: x.departmentCode,
      })),
      typeItems: [],
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
        })
        .catch((e) => {
          this.partnerCount = 0
          this.$store.dispatch("notifyServerError", e)
        })
    },
    populateParameters() {
      Object.values(this.filters).forEach((f) => {
        f.value = this.$route.query[f.param]
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
    setLocations(enabledLocationIds, jsonLocations, locationKeyWord, locationsWord) {
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

      return [...enabledLocations, divider, header, ...disabledLocations]
    },
    setDepartments(enabledDepartmentIds) {
      this.departmentItems = this.setLocations(enabledDepartmentIds, jsonDepartments, "department", "départements")
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
