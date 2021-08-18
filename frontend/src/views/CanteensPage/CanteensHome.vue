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

    <v-sheet class="px-6" elevation="0">
      <v-row>
        <v-col cols="12" md="7" class="pt-0">
          <form role="search" class="d-block d-sm-flex" onsubmit="return false">
            <v-text-field
              hide-details="auto"
              ref="search"
              v-model="searchTerm"
              outlined
              label="Recherche par nom de l'établissement"
              clearable
              @click:clear="clearSearch"
              @keyup.enter="search"
            ></v-text-field>
            <v-btn outlined color="primary" large class="ml-4 mt-1" height="48px" @click="search">
              <v-icon>mdi-magnify</v-icon>
              Chercher
            </v-btn>
          </form>
        </v-col>
      </v-row>
    </v-sheet>

    <v-sheet class="pa-6 mt-8" rounded outlined>
      <h2 class="text-left text-body-1 font-weight-black mb-2">
        Filtres
        <v-btn
          color="primary"
          v-if="hasActiveFilter"
          plain
          text
          @click="clearFilters"
          :ripple="false"
          height="30"
          class="pa-1 mt-n2"
        >
          <v-icon small class="mt-1 mr-1">mdi-close</v-icon>
          <span class="text-decoration-underline">Désactiver tous les filtres</span>
        </v-btn>
      </h2>
      <v-row id="filters">
        <v-col cols="12" sm="6" md="4" class="text-left">
          <label
            for="select-department"
            :class="{
              'text-body-2': true,
              'active-filter-label': !!appliedFilters.chosenDepartment,
            }"
          >
            Département
          </label>
          <v-select
            v-model="appliedFilters.chosenDepartment"
            :items="departments"
            clearable
            hide-details
            id="select-department"
            placeholder="Tous les départements"
            class="mt-1"
            outlined
          ></v-select>
        </v-col>
        <v-col cols="12" sm="6" md="4" class="text-left">
          <label
            for="select-sector"
            :class="{ 'text-body-2': true, 'active-filter-label': !!appliedFilters.chosenSectors.length }"
          >
            Secteur d'activité
          </label>
          <v-select
            v-model="appliedFilters.chosenSectors"
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
          <label
            :class="{
              'text-body-2': true,
              'active-filter-label': !!appliedFilters.minMealCount || !!appliedFilters.maxMealCount,
            }"
            id="meal-count"
          >
            Repas par jour
          </label>
          <div class="d-flex mt-1">
            <v-text-field
              :value="appliedFilters.minMealCount"
              ref="minMealCount"
              :rules="[validators.nonNegativeOrEmpty]"
              @change="onChangeMealCount('minMealCount')"
              hide-details="auto"
              outlined
              label="Min"
              aria-describedby="meal-count"
            />
            <span class="mx-4 align-self-center">-</span>
            <v-text-field
              :value="appliedFilters.maxMealCount"
              ref="maxMealCount"
              :rules="[validators.nonNegativeOrEmpty]"
              @change="onChangeMealCount('maxMealCount')"
              hide-details="auto"
              outlined
              label="Max"
              aria-describedby="meal-count"
            />
          </div>
        </v-col>
      </v-row>
    </v-sheet>
    <div v-if="loading" class="pa-6">
      <v-progress-circular indeterminate></v-progress-circular>
    </div>
    <div v-else-if="visibleCanteens && visibleCanteens.length > 0">
      <v-pagination class="my-6" v-model="page" :length="Math.ceil(publishedCanteenCount / limit)"></v-pagination>
      <v-row>
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
    <div v-else class="d-flex flex-column align-center py-10">
      <v-icon large>mdi-inbox-remove</v-icon>
      <p class="text-body-1 grey--text text--darken-1 my-2">Nous n'avons pas trouvé des cantines avec ces paramètres</p>
      <v-btn color="primary" text @click="clearFilters" class="text-decoration-underline" v-if="hasActiveFilter">
        Désactiver tous les filtres
      </v-btn>
    </div>
  </div>
</template>

<script>
import PublishedCanteenCard from "./PublishedCanteenCard"
import jsonDepartments from "@/departments.json"
import { getObjectDiff } from "@/utils"
import validators from "@/validators"

export default {
  data() {
    return {
      limit: 6,
      departments: jsonDepartments.map((x) => ({
        text: `${x.departmentCode} - ${x.departmentName}`,
        value: x.departmentCode,
      })),
      visibleCanteens: null,
      publishedCanteenCount: null,
      page: null,
      searchTerm: null,
      appliedFilters: {
        chosenDepartment: null,
        chosenSectors: [],
        minMealCount: null,
        maxMealCount: null,
      },
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
      if (this.page) query.page = String(this.page)
      if (this.searchTerm) query.recherche = this.searchTerm
      if (this.appliedFilters.chosenDepartment) query.departement = this.appliedFilters.chosenDepartment
      if (this.appliedFilters.chosenSectors && this.appliedFilters.chosenSectors.length > 0)
        query.secteurs = this.appliedFilters.chosenSectors.join("+")
      if (this.appliedFilters.minMealCount) query.minRepasJour = String(this.appliedFilters.minMealCount)
      if (this.appliedFilters.maxMealCount) query.maxRepasJour = String(this.appliedFilters.maxMealCount)
      return query
    },
    sectors() {
      return this.$store.state.sectors
        .map((x) => ({ text: x.name, value: x.id }))
        .sort((a, b) => (a.text > b.text ? 1 : -1))
    },
    hasActiveFilter() {
      return (
        this.appliedFilters.chosenDepartment !== null ||
        this.appliedFilters.chosenSectors.length > 0 ||
        this.appliedFilters.minMealCount !== null ||
        this.appliedFilters.maxMealCount !== null
      )
    },
    validators() {
      return validators
    },
  },
  methods: {
    fetchCurrentPage() {
      let queryParam = `limit=${this.limit}&offset=${this.offset}`
      if (this.searchTerm) queryParam += `&search=${this.searchTerm}`
      if (this.appliedFilters.chosenDepartment) queryParam += `&department=${this.appliedFilters.chosenDepartment}`
      if (this.appliedFilters.minMealCount) queryParam += `&min_daily_meal_count=${this.appliedFilters.minMealCount}`
      if (this.appliedFilters.maxMealCount) queryParam += `&max_daily_meal_count=${this.appliedFilters.maxMealCount}`

      for (let i = 0; i < this.appliedFilters.chosenSectors.length; i++)
        queryParam += `&sectors=${this.appliedFilters.chosenSectors[i]}`

      return fetch(`/api/v1/publishedCanteens/?${queryParam}`)
        .then((response) => {
          if (response.status < 200 || response.status >= 400) throw new Error(`Error encountered : ${response}`)
          return response.json()
        })
        .then((response) => {
          this.publishedCanteenCount = response.count
          this.visibleCanteens = response.results
        })
        .catch(() => {
          this.publishedCanteenCount = 0
          this.$store.dispatch("notifyServerError")
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
    clearFilters() {
      this.appliedFilters = {
        chosenDepartment: null,
        chosenSectors: [],
        minMealCount: null,
        maxMealCount: null,
      }
    },
    changePage() {
      const override = this.page ? { page: this.page } : { page: 1 }
      const query = Object.assign(this.query, override)
      this.$router.push({ query }).catch(() => {})
    },
    applyFilter() {
      const changedKeys = Object.keys(getObjectDiff(this.query, this.$route.query))
      const shouldNavigate = changedKeys.length > 0
      if (shouldNavigate) this.$router.push({ query: Object.assign(this.query, { page: 1 }) }).catch(() => {})
      else this.fetchCurrentPage()
    },
    populateParameters() {
      this.page = this.$route.query.page ? parseInt(this.$route.query.page) : 1
      this.searchTerm = this.$route.query.recherche || null
      this.appliedFilters = {
        chosenDepartment: this.$route.query.departement || null,
        chosenSectors: this.$route.query.secteurs?.split?.("+").map((x) => parseInt(x)) || [],
        minMealCount: parseInt(this.$route.query.minRepasJour) || null,
        maxMealCount: parseInt(this.$route.query.maxRepasJour) || null,
      }
    },
    onChangeMealCount(ref) {
      if (this.$refs[ref].validate()) this.appliedFilters[ref] = parseInt(this.$refs[ref].lazyValue) || null
    },
  },
  watch: {
    appliedFilters: {
      handler() {
        this.applyFilter()
      },
      deep: true,
    },
    page() {
      this.changePage()
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

<style scoped>
.v-btn--plain:not(.v-btn--active):not(.v-btn--loading):not(:focus):not(:hover) >>> .v-btn__content {
  opacity: 1;
}
.active-filter-label {
  font-weight: bold;
}
.active-filter-label::before {
  content: "⚫︎";
  color: #0c7f46;
}
</style>
