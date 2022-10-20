<template>
  <div>
    <div class="pa-4">
      <v-row class="mb-4" align="center">
        <p class="mb-0" style="height: fit-content">
          Parmi vos {{ canteenCount }} cantines, {{ unteledeclaredCount }} cantines ne sont pas télédéclarées.
        </p>
        <v-btn color="primary" class="ml-2">Télédéclarer {{ unteledeclaredCount }} cantines</v-btn>
      </v-row>
      <v-row align="center">
        <p class="mb-0" style="height: fit-content">
          Parmi vos {{ canteenCount }} cantines, {{ unteledeclaredCount }} cantines ne sont pas publiées.
        </p>
        <v-btn color="primary" outlined class="ml-2">Publier {{ unteledeclaredCount }} cantines</v-btn>
      </v-row>
    </div>
    <div class="mt-4">
      <h2>Mes cantines en {{ year }}</h2>
      <v-data-table
        v-if="visibleCanteens"
        :options.sync="options"
        :server-items-length="canteenCount || 0"
        :items="visibleCanteens"
        :headers="headers"
        dense
        :items-per-page="limit"
        :footer-props="{
          disableItemsPerPage: true,
        }"
      >
        <template v-slot:[`item.productionType`]="{ item }">
          {{ typeDisplay[item.productionType] }}
        </template>
        <template v-slot:[`item.action`]="{ item }">
          <div v-if="item.action === 'NOTHING'" class="px-3">
            <v-icon small class="mr-2" color="green">$checkbox-circle-fill</v-icon>
            <span class="caption">Rien à faire !</span>
          </div>
          <v-btn small outlined color="primary" :to="actionLink(item)" v-else>
            <v-icon small class="mr-2" color="primary">{{ actions[item.action].icon }}</v-icon>
            {{ actions[item.action].display }}
            <span class="d-sr-only">{{ item.userCanView ? "" : "de" }} {{ item.name }}</span>
          </v-btn>
        </template>
      </v-data-table>
    </div>
  </div>
</template>

<script>
export default {
  name: "AnnualCanteenSummaryTable",
  data() {
    const year = 2021
    return {
      limit: 15,
      page: null,
      canteenCount: null,
      visibleCanteens: null,
      searchTerm: null,
      inProgress: false,
      year,
      unteledeclaredCount: 7,
      options: {
        sortBy: [],
        sortDesc: [],
        page: 1,
      },
      headers: [
        { text: "Nom", value: "name" },
        { text: "Type", value: "productionType" },
        { text: "Action", value: "action" },
      ],
      typeDisplay: {
        site: "Cuisine sur site",
        site_cooked_elsewhere: "Cantine satellite",
        central: "Cuisine centrale",
        central_serving: "Centrale avec service sur place",
      },
      actions: {
        CREATE: {
          display: "Créer le diagnostic " + year,
          icon: "$add-circle-fill",
        },
        COMPLETE: {
          display: "Completer le diagnostic " + year,
          icon: "$edit-box-fill",
        },
        TELEDECLARE: {
          display: "Télédéclarer",
          icon: "$send-plane-fill",
        },
        PUBLISH: {
          display: "Publier",
          icon: "mdi-bullhorn",
        },
        NOTHING: {
          display: "Rien à faire !",
          icon: "$checkbox-circle-fill",
        },
      },
    }
  },
  computed: {
    showPagination() {
      return this.canteenCount && this.canteenCount > this.limit
    },
    showSearch() {
      return this.showPagination || this.searchTerm
    },
    offset() {
      return (this.page - 1) * this.limit
    },
    query() {
      let query = {}
      if (this.page) query.page = String(this.page)
      if (this.searchTerm) query.recherche = this.searchTerm
      return query
    },
  },
  methods: {
    populateInitialParameters() {
      this.page = this.$route.query.cantinePage ? parseInt(this.$route.query.cantinePage) : 1
    },
    fetchCurrentPage() {
      let queryParam = `limit=${this.limit}&offset=${this.offset}`
      if (this.searchTerm) queryParam += `&search=${this.searchTerm}`
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
          this.visibleCanteens.forEach((canteen) => {
            if (!canteen.diagnostics || canteen.diagnostics.length === 0) {
              canteen.action = "CREATE"
            } else {
              const thisYearDiag = canteen.diagnostics.find((d) => d.year === this.year)
              if (!thisYearDiag) {
                canteen.action = "CREATE"
              } else if (thisYearDiag.teledeclaration && thisYearDiag.teledeclaration.status === "SUBMITTED") {
                if (canteen.publicationStatus === "draft") {
                  canteen.action = "NOTHING"
                } else {
                  canteen.action = "PUBLISH"
                }
              } else if (thisYearDiag.valueTotalHt) {
                canteen.action = "TELEDECLARE"
              } else {
                canteen.action = "COMPLETE"
              }
            }
          })
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
    actionLink(canteen) {
      return {
        name: "CanteenModification",
        params: { canteenUrlComponent: this.$store.getters.getCanteenUrlComponent(canteen) },
      }
    },
    addWatchers() {
      // this.$watch("appliedFilters", this.onAppliedFiltersChange, { deep: true })
      this.$watch("options", this.onOptionsChange, { deep: true })
      this.$watch("$route", this.onRouteChange)
    },
    onOptionsChange() {
      // this.$router.push({ query: this.getUrlQueryParams() }).catch(() => {})
      const replace = Object.keys(this.$route.query).length === 0
      const page = { query: { ...this.$route.query, ...{ cantinePage: this.options.page } } }
      // The empty catch is the suggested error management here : https://github.com/vuejs/vue-router/issues/2872#issuecomment-519073998
      if (replace) this.$router.replace(page).catch(() => {})
      else this.$router.push(page).catch(() => {})
    },
    onRouteChange() {
      this.populateInitialParameters()
      this.fetchCurrentPage()
    },
  },
  mounted() {
    this.populateInitialParameters()
    return this.fetchCurrentPage().then(this.addWatchers)
  },
}
</script>
