<template>
  <div>
    <v-sheet class="px-3 mt-6 mb-6" elevation="0">
      <v-row>
        <v-col cols="12" md="7" class="pa-0 pr-md-8">
          <form role="search" class="d-block d-sm-flex align-end" onsubmit="return false">
            <DsfrSearchField
              hide-details="auto"
              ref="search"
              v-model="searchTerm"
              placeholder="Recherche par nom de l'établissement"
              clearable
              :clearAction="clearSearch"
              :searchAction="search"
              class="mb-2 flex-grow-1"
            />
          </form>
        </v-col>
        <v-col cols="12" md="4" class="pa-0">
          <DsfrSelect
            @change="applyProductionType"
            height="40"
            v-model="filterProductionType"
            :items="productionTypeOptions"
          />
        </v-col>
      </v-row>
    </v-sheet>
    <DsfrPagination class="mb-6" v-model="page" :length="Math.ceil(canteenCount / limit)" />
    <v-sheet fluid height="200" v-if="inProgress">
      <v-progress-circular indeterminate style="left: 50%; top: 50%"></v-progress-circular>
    </v-sheet>
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
          :to="{ name: 'NewCanteen' }"
        >
          <v-icon size="100" class="primary--text">mdi-plus</v-icon>
          <v-card-text class="font-weight-bold pt-0 text-center primary--text">
            Ajouter une cantine
          </v-card-text>
        </v-card>
        <v-spacer></v-spacer>
        <div class="d-flex mt-4 mb-2 align-center px-2">
          <v-divider></v-divider>
          <p class="mx-2 my-0 caption">ou</p>
          <v-divider></v-divider>
        </div>
        <v-spacer></v-spacer>
        <v-btn text color="primary" :to="{ name: 'DiagnosticsImporter' }">
          <v-icon class="mr-2">mdi-file-upload-outline</v-icon>
          Créer plusieurs cantines depuis un fichier
        </v-btn>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import CanteenCard from "./CanteenCard"
import DsfrPagination from "@/components/DsfrPagination"
import DsfrSearchField from "@/components/DsfrSearchField"
import DsfrSelect from "@/components/DsfrSelect"

export default {
  name: "CanteensPagination",
  components: { CanteenCard, DsfrPagination, DsfrSearchField, DsfrSelect },
  data() {
    return {
      limit: 5,
      page: null,
      canteenCount: null,
      visibleCanteens: null,
      searchTerm: null,
      filterProductionType: "all",
      productionTypeQuery: null,
      inProgress: false,
      productionTypeOptions: [
        { text: "Toutes les cantines", value: "all" },
        { text: "Cuisines centrales", value: "central" },
        { text: "Cantines satellites et autogérées", value: "satellites" },
      ],
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
      if (this.productionTypeQuery)
        if (this.productionTypeQuery.indexOf("central") !== -1) query.typeEtablissement = "central"
        else query.typeEtablissement = "satellite_site"
      return query
    },
  },
  methods: {
    populateInitialParameters() {
      this.page = this.$route.query.cantinePage ? parseInt(this.$route.query.cantinePage) : 1
      if (this.$route.query.typeEtablissement === "central") {
        this.filterProductionType = "central"
      } else if (this.$route.query.typeEtablissement === "satellite_site") {
        this.filterProductionType = "satellites"
      } else {
        this.filterProductionType = "all"
      }
    },
    fetchCurrentPage() {
      let queryParam = `limit=${this.limit}&offset=${this.offset}`
      if (this.searchTerm) queryParam += `&search=${this.searchTerm}`
      if (this.productionTypeQuery)
        for (let i = 0; i < this.productionTypeQuery.length; i++)
          queryParam += `&production_type=${this.productionTypeQuery[i]}`
      this.searchTerm = this.$route.query.recherche || null
      this.inProgress = true

      return fetch(`/api/v1/canteens/?${queryParam}`)
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
    populateProductionType() {
      if (this.filterProductionType === "central") this.productionTypeQuery = ["central", "central_serving"]
      else if (this.filterProductionType === "satellites") this.productionTypeQuery = ["site", "site_cooked_elsewhere"]
      else this.productionTypeQuery = null
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
    filterProductionType() {
      this.populateProductionType()
    },
    $route() {
      this.populateInitialParameters()
      this.$nextTick(this.fetchCurrentPage)
    },
  },
  mounted() {
    this.populateInitialParameters()
    if (Object.keys(this.$route.query).length > 0) {
      this.populateProductionType()
      this.fetchCurrentPage()
    }
  },
}
</script>
