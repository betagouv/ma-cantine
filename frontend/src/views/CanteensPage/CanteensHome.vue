<template>
  <div>
    <v-card elevation="0" class="text-center text-md-left mb-8 mt-6">
      <v-row v-if="$vuetify.breakpoint.smAndDown">
        <v-col cols="12">
          <v-img max-height="120px" contain src="/static/images/LovingDoodle.png"></v-img>
        </v-col>
      </v-row>
      <v-row>
        <v-spacer></v-spacer>
        <v-col cols="3" v-if="$vuetify.breakpoint.mdAndUp">
          <div class="d-flex fill-height align-center">
            <v-img max-height="140px" contain src="/static/images/LovingDoodle.png"></v-img>
          </div>
        </v-col>
        <v-col cols="12" sm="10" md="7">
          <v-card-title class="pr-0">
            <h1 class="font-weight-black text-h5 text-sm-h4">
              Découvrez les initiatives prises par nos cantines pour une alimentation saine, de qualité, et plus
              durable.
            </h1>
          </v-card-title>
        </v-col>
        <v-spacer></v-spacer>
      </v-row>
    </v-card>
    <div v-if="loading">
      <v-progress-circular indeterminate></v-progress-circular>
    </div>

    <div v-else>
      <v-sheet class="pa-6" rounded outlined>
        <h2 class="text-left text-body-1 font-weight-black mb-8">Recherche</h2>
        <v-row>
          <v-col cols="12" md="7" class="d-flex pt-0">
            <v-text-field
              hide-details="auto"
              ref="search"
              v-model="searchTerm"
              outlined
              placeholder="Recherche par nom de l'établissement"
              clearable
              @click:clear="clearSearch"
              @keyup.enter="search"
            ></v-text-field>
            <v-btn outlined color="primary" large class="ml-4 mt-1" height="48px" @click="search">
              <v-icon>mdi-magnify</v-icon>
              Chercher
            </v-btn>
          </v-col>
        </v-row>

        <h2 class="text-left text-body-1 font-weight-black mt-6 mb-1">Plus de filtres</h2>
        <v-row id="filters">
          <v-col cols="12" sm="6" md="4" class="text-left">
            <label for="select-department" class="text-body-2">Departement</label>
            <v-select
              v-model="chosenDepartment"
              :items="departments"
              clearable
              hide-details
              id="select-department"
              placeholder="Tous les departements"
              class="mt-1"
              outlined
            ></v-select>
          </v-col>
          <v-col cols="12" sm="6" md="4" class="text-left">
            <label for="select-sector" class="text-body-2">Secteur d'activité</label>
            <v-select
              v-model="chosenSectors"
              multiple
              :items="sectors"
              clearable
              hide-details
              id="select-sector"
              placeholder="Tous les secteurs"
              outlined
              class="mt-1"
            ></v-select>
          </v-col>
          <v-col cols="12" sm="6" md="4" class="text-left">
            <label class="text-body-2">Repas par jour</label>
            <div class="d-flex mt-1">
              <v-text-field v-model="minMealCount" type="number" hide-details="auto" outlined label="Min" />
              <span class="mx-4 align-self-center">-</span>
              <v-text-field v-model="maxMealCount" type="number" hide-details="auto" outlined label="Max" />
            </div>
          </v-col>
        </v-row>
      </v-sheet>

      <v-pagination class="my-6" v-model="page" :length="Math.ceil(publishedCanteenCount / limit)"></v-pagination>
      <v-progress-circular class="my-10" indeterminate v-if="!visibleCanteens"></v-progress-circular>
      <v-row v-else>
        <v-col v-for="canteen in visibleCanteens" :key="canteen.id" style="height: auto;" cols="12" md="6">
          <PublishedCanteenCard :canteen="canteen" />
        </v-col>
      </v-row>
      <v-pagination
        class="my-6"
        v-model="page"
        :length="Math.ceil(publishedCanteenCount / limit)"
        v-if="$vuetify.breakpoint.smAndDown"
      ></v-pagination>
    </div>
  </div>
</template>

<script>
import PublishedCanteenCard from "./PublishedCanteenCard"
import jsonDepartments from "@/departments.json"

export default {
  data() {
    return {
      limit: 6,
      page: null,
      departments: jsonDepartments.map((x) => ({
        text: `${x.departmentCode} - ${x.departmentName}`,
        value: x.departmentCode,
      })),
      chosenDepartment: null,
      chosenSectors: [],
      minMealCount: null,
      maxMealCount: null,
      searchTerm: null,
      visibleCanteens: null,
      publishedCanteenCount: null,
    }
  },
  components: { PublishedCanteenCard },
  computed: {
    loading() {
      return this.publishedCanteenCount === null
    },
    offset() {
      return (this.page - 1) * this.limit
    },
    query() {
      let query = {}
      if (this.page) query.page = this.page
      if (this.searchTerm) query.recherche = this.searchTerm
      if (this.chosenDepartment) query.departement = this.chosenDepartment
      if (this.chosenSectors && this.chosenSectors.length > 0) query.secteurs = this.chosenSectors.join("+")
      if (this.minMealCount) query.minRepasJour = this.minMealCount
      if (this.maxMealCount) query.maxRepasJour = this.maxMealCount
      return query
    },
    sectors() {
      return this.$store.state.sectors.map((x) => ({ text: x.name, value: x.id }))
    },
  },
  methods: {
    fetchCurrentPage() {
      let queryParam = `limit=${this.limit}&offset=${this.offset}`
      if (this.searchTerm) queryParam += `&search=${this.searchTerm}`
      if (this.chosenDepartment) queryParam += `&department=${this.chosenDepartment}`
      if (this.minMealCount) queryParam += `&min_daily_meal_count=${this.minMealCount}`
      if (this.maxMealCount) queryParam += `&max_daily_meal_count=${this.maxMealCount}`

      for (let i = 0; i < this.chosenSectors.length; i++) queryParam += `&sectors=${this.chosenSectors[i]}`

      return (
        fetch(`/api/v1/publishedCanteens/?${queryParam}`)
          // verifyResponse
          .then((response) => response.json())
          .then((response) => {
            this.publishedCanteenCount = response.count
            this.visibleCanteens = response.results
            // TODO : loading false
          })
          .catch(() => {
            // TODO : Handle error
          })
      )
    },
    clearSearch() {
      this.searchTerm = ""
      this.search()
    },
    search() {
      const override = this.searchTerm ? { page: 1, recherche: this.searchTerm } : { page: 1 }
      const query = Object.assign(this.query, override)
      this.$router.push({ query }).catch(() => {})
      this.fetchCurrentPage()
    },
    applyFilter(filterQueryObject) {
      // The empty catch is the suggested error management here :
      // https://github.com/vuejs/vue-router/issues/2872#issuecomment-519073998
      // We reset to page 1 after applying a filter unless otherwise specified
      const pageCorrectedQuery = Object.assign({ page: 1 }, filterQueryObject)
      const currentQuery = this.$route.query
      const shouldNavigate = Object.keys(pageCorrectedQuery).some(
        (key) => String(pageCorrectedQuery[key]) !== currentQuery[key]
      )
      if (shouldNavigate) this.$router.push({ query: Object.assign(this.query, pageCorrectedQuery) }).catch(() => {})
      else this.fetchCurrentPage()
    },
    populateParameters() {
      this.page = this.$route.query.page ? parseInt(this.$route.query.page) : 1
      this.searchTerm = this.$route.query.recherche || null
      this.chosenDepartment = this.$route.query.departement || null
      this.chosenSectors = this.$route.query.secteurs?.split?.("+").map((x) => parseInt(x)) || []
      this.minMealCount = parseInt(this.$route.query.minRepasJour) || null
      this.maxMealCount = parseInt(this.$route.query.maxRepasJour) || null
    },
  },
  watch: {
    page(newPage) {
      this.applyFilter({ page: newPage })
    },
    chosenSectors(newChosenSectors) {
      const hasSectors = newChosenSectors && newChosenSectors.length > 0
      this.applyFilter(hasSectors ? { secteurs: newChosenSectors.join("+") } : {})
    },
    chosenDepartment(newDepartment) {
      this.applyFilter(newDepartment ? { departement: newDepartment } : {})
    },
    maxMealCount(newMaxMealCount) {
      this.applyFilter(newMaxMealCount ? { maxRepasJour: newMaxMealCount } : {})
    },
    minMealCount(newMinMealCount) {
      this.applyFilter(newMinMealCount ? { minRepasJour: newMinMealCount } : {})
    },
    $route() {
      this.populateParameters()
    },
  },
  mounted() {
    this.populateParameters()
  },
}
</script>
