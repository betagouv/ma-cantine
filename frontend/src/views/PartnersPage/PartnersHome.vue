<template>
  <div class="text-left">
    <BreadcrumbsNav />
    <v-row>
      <v-col cols="12" sm="7" md="8">
        <h1 class="font-weight-black text-h5 text-sm-h4 mb-4">
          Nos Partenaires
        </h1>
        <p>
          Les acteurs de la restauration collective au service des gestionnaires
        </p>
      </v-col>
      <v-col cols="0" sm="5" md="4" v-if="$vuetify.breakpoint.smAndUp" class="py-0 pr-8 d-flex">
        <v-spacer></v-spacer>
        <v-img src="/static/images/peeps-illustration-couple.png" contain max-width="140"></v-img>
      </v-col>
    </v-row>
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
          <v-col cols="12" sm="6">
            <label
              for="select-category"
              :class="{ 'text-body-2': true, 'active-filter-label': !!filters.category.value }"
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
            <DsfrSelect
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
            <label for="select-type" :class="{ 'text-body-2': true, 'active-filter-label': !!filters.type.value }">
              Type
            </label>
            <DsfrSelect
              v-model="filters.type.value"
              multiple
              :items="typeItems"
              clearable
              hide-details
              id="select-type"
              placeholder="Tous les besoins"
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
        <DsfrPagination v-model="page" :length="Math.ceil(partnerCount / limit)" :total-visible="7" />
      </v-col>
      <v-spacer></v-spacer>
    </v-row>
    <v-row>
      <v-col v-for="partner in visiblePartners" :key="partner.id" style="height: auto;" cols="12" sm="6" md="4">
        <PartnerCard :partner="partner" />
      </v-col>
    </v-row>
  </div>
</template>

<script>
import BreadcrumbsNav from "@/components/BreadcrumbsNav"
import DsfrPagination from "@/components/DsfrPagination"
import DsfrSelect from "@/components/DsfrSelect"
import PartnerCard from "@/views/PartnersPage/PartnerCard"
import { getObjectDiff } from "@/utils"
import jsonDepartments from "@/departments.json"

export default {
  name: "PartnersHome",
  components: { BreadcrumbsNav, DsfrPagination, DsfrSelect, PartnerCard },
  data() {
    return {
      limit: 6,
      page: null,
      types: [],
      visiblePartners: null,
      partnerCount: null,
      filters: {
        free: {
          frenchKey: "gratuit",
          value: undefined, // will be set from URL query
        },
        category: {
          frenchKey: "besoin",
          value: undefined,
        },
        department: {
          frenchKey: "departement",
          value: [],
          default: [],
        },
        type: {
          frenchKey: "type",
          value: undefined,
        },
      },
      showFilters: false,
      categoryItems: [
        {
          value: "appro",
          text: "Améliorer ma part de bio / durable",
        },
        {
          value: "plastic",
          text: "Substituer mes plastiques",
        },
        {
          value: "asso",
          text: "Donner à une association",
        },
        {
          value: "waste",
          text: "Diagnostiquer mon gaspillage",
        },
        {
          value: "training",
          text: "Me former ou former mon personnel",
        },
        {
          value: "help",
          text: "Trouver des aides / conseils sanitaires",
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
        if (f.value) query[f.frenchKey] = f.value
      })
      return query
    },
    hasActiveFilter() {
      return Object.values(this.filters).some((f) => !!f.value && f.value.length)
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
        })
        .catch((e) => {
          this.partnerCount = 0
          this.$store.dispatch("notifyServerError", e)
        })
    },
    populateParameters() {
      Object.values(this.filters).forEach((f) => {
        f.value = this.$route.query[f.frenchKey]
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
      } else this.fetchCurrentPage()
    },
    clearFilters() {
      Object.entries(this.filters).forEach(([key, f]) => {
        this.filters[key].value = f.default
      })
    },
  },
  watch: {
    page() {
      // TODO: fix bug which results in redirect to page 1 on refresh/load of page 2+
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
    this.populateParameters()
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
</style>
