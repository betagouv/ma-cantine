<template>
  <div>
    <v-sheet class="px-3 mt-6 mb-6" elevation="0" v-if="showFilters">
      <v-row>
        <v-col cols="12" md="7" class="pa-0 pr-md-8">
          <form role="search" class="d-block d-sm-flex align-end" onsubmit="return false">
            <DsfrSearchField
              hide-details="auto"
              ref="search"
              v-model="searchTerm"
              placeholder="Recherche par nom, SIRET de l'établissement ou SIREN de l'unité légale"
              clearable
              @clear="clearSearch"
              @search="search"
              class="mb-2 flex-grow-1"
            />
          </form>
        </v-col>
        <v-col cols="12" md="4" class="pa-0">
          <DsfrNativeSelect
            v-model="filterProductionType"
            :items="productionTypeOptions"
            label="Filtrer par type de production"
            labelClasses="d-sr-only"
            title="Filtrer par type de production"
          />
        </v-col>
      </v-row>
    </v-sheet>
    <DsfrPagination class="mb-6" v-model="page" :length="Math.ceil(canteenCount / limit)" v-if="showPagination" />
    <v-sheet fluid height="200" v-if="inProgress">
      <v-progress-circular indeterminate style="left: 50%; top: 50%"></v-progress-circular>
    </v-sheet>
    <v-row v-if="visibleCanteens.length === 0">
      <v-col cols="12">
        <p>Aucune cantine trouvée pour la recherche : {{ searchTerm }}</p>
      </v-col>
    </v-row>
    <v-row v-else>
      <v-col cols="12" sm="6" md="4" height="100%" v-for="canteen in visibleCanteens" :key="`canteen-${canteen.id}`">
        <CanteenCard :canteen="canteen" class="fill-height" />
      </v-col>
      <v-col cols="12" sm="6" md="4" height="100%" class="d-flex flex-column">
        <v-card
          class="d-flex flex-column align-center justify-center dsfr"
          outlined
          min-height="220"
          height="80%"
          :to="{ name: 'GestionnaireCantineAjouter' }"
        >
          <v-icon size="100" class="primary--text">mdi-plus</v-icon>
          <v-card-text class="font-weight-bold pt-0 text-center primary--text text-body-1">
            Ajouter une cantine
          </v-card-text>
        </v-card>
        <v-spacer></v-spacer>
        <div class="d-flex mt-4 mb-2 align-center px-2">
          <v-divider aria-hidden="true" role="presentation"></v-divider>
          <p class="mx-2 my-0 caption">ou</p>
          <v-divider aria-hidden="true" role="presentation"></v-divider>
        </div>
        <v-spacer></v-spacer>
        <v-btn text color="primary" :to="{ name: 'GestionnaireImportCantines' }">
          <v-icon class="mr-2">mdi-file-upload-outline</v-icon>
          Créer plusieurs cantines depuis un fichier
        </v-btn>
      </v-col>
    </v-row>
    <DsfrPagination class="my-6" v-model="page" :length="Math.ceil(canteenCount / limit)" v-if="showPagination" />
  </div>
</template>

<script>
import CanteenCard from "./CanteenCard"
import DsfrPagination from "@/components/DsfrPagination"
import DsfrSearchField from "@/components/DsfrSearchField"
import DsfrNativeSelect from "@/components/DsfrNativeSelect"
import Constants from "@/constants"
import { lastYear } from "@/utils"

export default {
  name: "CanteensPagination",
  components: { CanteenCard, DsfrPagination, DsfrSearchField, DsfrNativeSelect },
  data() {
    return {
      limit: 5,
      page: null,
      canteenCount: null,
      visibleCanteens: null,
      searchTerm: null,
      filterProductionType: "all",
      inProgress: false,
      productionTypeOptions: [{ text: "Toutes les cantines", value: "all" }].concat(Constants.ProductionTypes),
    }
  },
  computed: {
    offset() {
      return (this.page - 1) * this.limit
    },
    query() {
      let query = {}
      if (this.page) query.cantinePage = String(this.page)
      if (this.searchTerm) query.recherche = this.searchTerm
      if (this.filterProductionType !== "all") query.typeEtablissement = this.filterProductionType
      return query
    },
    showFilters() {
      return (
        this.canteenCount > this.limit ||
        this.searchTerm ||
        this.filterProductionType !== "all" ||
        this.$route.query.recherche
      )
    },
    showPagination() {
      return this.canteenCount > this.limit
    },
  },
  methods: {
    populateInitialParameters() {
      this.page = this.$route.query.cantinePage ? parseInt(this.$route.query.cantinePage) : 1
      if (this.$route.query.typeEtablissement === "central") {
        this.filterProductionType = "central"
      } else if (this.$route.query.typeEtablissement) {
        this.filterProductionType = this.$route.query.typeEtablissement
      } else {
        this.filterProductionType = "all"
      }
      this.searchTerm = this.$route.query.recherche || null
    },
    fetchCurrentPage() {
      let queryParam = `ordering=action&limit=${this.limit}&offset=${this.offset}`
      if (this.searchTerm) queryParam += `&search=${this.searchTerm}`
      if (this.filterProductionType !== "all") queryParam += `&production_type=${this.filterProductionType}`
      this.inProgress = true

      return fetch(`/api/v1/actionableCanteens/${lastYear()}?${queryParam}`)
        .then((response) => {
          if (response.status < 200 || response.status >= 400) throw new Error(`Error encountered : ${response}`)
          return response.json()
        })
        .then((response) => {
          this.canteenCount = response.count
          this.visibleCanteens = response.results
          this.$emit("canteen-count", this.canteenCount)
        })
        .catch((e) => {
          this.publishedCanteenCount = 0
          this.$store.dispatch("notifyServerError", e)
        })
        .finally(() => {
          this.inProgress = false
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
    applyProductionType() {
      this.$nextTick(() => {
        this.page = 1
        this.$router.push({ query: this.query }).catch(() => {})
      })
    },
  },
  watch: {
    page(newPage) {
      const replace = Object.keys(this.$route.query).length === 0
      const page = { query: { ...this.$route.query, ...{ cantinePage: newPage } } }
      // The empty catch is the suggested error management here : https://github.com/vuejs/vue-router/issues/2872#issuecomment-519073998
      if (replace) this.$router.replace(page).catch(() => {})
      else this.$router.push(page).catch(() => {})
    },
    $route() {
      this.populateInitialParameters()
      this.$nextTick(this.fetchCurrentPage)
    },
    filterProductionType() {
      this.applyProductionType()
    },
  },
  mounted() {
    this.populateInitialParameters()
    if (Object.keys(this.$route.query).length > 0) this.fetchCurrentPage()
  },
}
</script>
