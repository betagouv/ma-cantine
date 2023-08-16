<template>
  <div class="text-left">
    <h1 class="text-h6 mt-6 mb-2 font-weight-bold">
      Les cantines de mon territoire
    </h1>
    <p>Établissements dans {{ departmentsString }}</p>
    <v-data-table
      :footer-props="footerProps"
      :items="visibleCanteens"
      :options.sync="options"
      :loading="loading"
      :headers="headers"
      :server-items-length="canteenCount || 0"
    >
      <template v-slot:[`item.publicationStatus`]="{ item }">
        <router-link
          v-if="item.publicationStatus === 'published'"
          :to="{ name: 'CanteenPage', params: { canteenUrlComponent: `${item.id}--${item.name}` } }"
        >
          Publiée
        </router-link>
        <span v-else>
          Non publiée
        </span>
      </template>
    </v-data-table>
  </div>
</template>

<script>
import jsonDepartments from "@/departments.json"
import { getObjectDiff } from "@/utils"

export default {
  name: "ElectedCanteens",
  data() {
    return {
      loading: false,
      canteenCount: null,
      visibleCanteens: [],
      limit: 10,
      options: {
        sortBy: [],
        sortDesc: [],
        page: 1,
      },
      footerProps: {
        disableItemsPerPage: true,
        itemsPerPageText: "Cantines per page",
      },
      headers: [
        { text: "SIRET", value: "siret", sortable: true },
        { text: "Nom", value: "name", sortable: true },
        { text: "Ville", value: "city", sortable: true },
        { text: "Couverts moyen par jour", value: "dailyMealCount", sortable: true },
        { text: "Publication", value: "publicationStatus", sortable: false },
      ],
    }
  },
  computed: {
    offset() {
      return (this.options.page - 1) * this.limit
    },
    departmentsString() {
      const userDepartments = this.$store.state.loggedUser.departments
      const departmentsArray = jsonDepartments
        .filter((x) => userDepartments.indexOf(x.departmentCode) > -1)
        .map((x) => `${x.departmentName} (${x.departmentCode})`)
      if (departmentsArray.length < 2) return `le département ${departmentsArray.join("")}`
      return `les départements ${departmentsArray.slice(0, -1).join(", ")} et ${departmentsArray.slice(-1)}`
    },
  },
  methods: {
    fetchCurrentPage() {
      this.loading = true
      return fetch(`/api/v1/electedCanteens/?${this.getApiQueryParams()}`)
        .then((response) => {
          if (response.status < 200 || response.status >= 400) throw new Error(`Error encountered : ${response}`)
          return response.json()
        })
        .then((response) => {
          this.visibleCanteens = response.results
          this.canteenCount = response.count
        })
        .catch((e) => {
          this.publishedCanteenCount = 0
          this.visibleCanteens = []
          this.$store.dispatch("notifyServerError", e)
        })
        .finally(() => (this.loading = false))
    },
    getApiQueryParams(includePagination = true) {
      let apiQueryParams = includePagination ? `limit=${this.limit}&offset=${this.offset}` : ""
      const orderingItems = this.getOrderingItems()
      if (orderingItems.length > 0) apiQueryParams += `&ordering=${orderingItems.join(",")}`
      return apiQueryParams
    },
    addWatchers() {
      this.$watch("options", this.onOptionsChange, { deep: true })
      this.$watch("$route", this.onRouteChange)
    },
    onOptionsChange() {
      this.$router.push({ query: this.getUrlQueryParams() }).catch(() => {})
    },
    onRouteChange() {
      this.populateParametersFromRoute()
      this.fetchCurrentPage()
    },
    getUrlQueryParams() {
      let urlQueryParams = { page: this.options.page }
      const orderingItems = this.getOrderingItems()
      if (orderingItems.length > 0) urlQueryParams["trier-par"] = orderingItems.join(",")
      return urlQueryParams
    },
    getOrderingItems() {
      let orderParams = []
      if (this.options.sortBy && this.options.sortBy.length > 0)
        for (let i = 0; i < this.options.sortBy.length; i++)
          orderParams.push(this.options.sortDesc[i] ? `-${this.options.sortBy[i]}` : this.options.sortBy[i])
      return orderParams
    },
    populateParametersFromRoute() {
      const page = this.$route.query.page ? parseInt(this.$route.query.page) : 1
      let sortBy = []
      let sortDesc = []

      this.$route.query["trier-par"] &&
        this.$route.query["trier-par"].split(",").forEach((element) => {
          const isDesc = element[0] === "-"
          sortBy.push(isDesc ? element.slice(1) : element)
          sortDesc.push(isDesc)
        })

      const newOptions = { sortBy, sortDesc, page }
      const optionChanges = this.options ? getObjectDiff(this.options, newOptions) : newOptions
      if (Object.keys(optionChanges).length > 0) this.$set(this, "options", newOptions)
    },
  },
  beforeMount() {
    if (!this.$route.query["page"]) this.$router.replace({ query: { page: 1 } })
  },
  mounted() {
    this.populateParametersFromRoute()
    this.fetchCurrentPage().then(this.addWatchers)
  },
}
</script>
