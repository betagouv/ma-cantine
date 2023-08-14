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
    ></v-data-table>
  </div>
</template>

<script>
import jsonDepartments from "@/departments.json"

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
        pagination: {
          itemsLength: 0,
        },
      },
      headers: [
        {
          text: "SIRET",
          align: "start",
          filterable: false,
          value: "siret",
          sortable: false,
        },
        { text: "Nom", value: "name", sortable: true },
        { text: "Ville", value: "city", sortable: true },
        { text: "Couverts moyen par jour", value: "dailyMealCount", sortable: false },
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
      let queryParam = `limit=${this.limit}&offset=${this.offset}`
      return fetch(`/api/v1/electedCanteens/?${queryParam}`)
        .then((response) => {
          if (response.status < 200 || response.status >= 400) throw new Error(`Error encountered : ${response}`)
          return response.json()
        })
        .then((response) => {
          this.visibleCanteens = response.results
          this.canteenCount = this.footerProps.pagination.itemsLength = response.count
        })
        .catch((e) => {
          this.publishedCanteenCount = 0
          this.visibleCanteens = []
          this.$store.dispatch("notifyServerError", e)
        })
        .finally(() => (this.loading = false))
    },
  },
  mounted() {
    this.fetchCurrentPage()
  },
}
</script>
