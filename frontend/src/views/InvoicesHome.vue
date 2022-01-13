<template>
  <div class="text-left">
    <div class="d-flex">
      <div>
        <h1 class="font-weight-black text-h5 text-sm-h4 my-4" style="width: 100%">
          Mes Achats
        </h1>
        <p>
          Une alimentation saine et durable commence par un suivi comptable de vos achats
        </p>
        <v-btn class="primary" :to="{ name: 'NewPurchase' }" large>
          <v-icon>mdi-plus</v-icon>
          Ajouter une ligne
        </v-btn>
      </div>
      <v-spacer></v-spacer>

      <v-img
        src="/static/images/ChartDoodle.png"
        v-if="$vuetify.breakpoint.smAndUp"
        class="mx-auto rounded-0"
        contain
        max-width="150"
      ></v-img>
    </div>
    <v-card outlined class="my-4" v-if="visiblePurchases">
      <!-- eslint-disable-next-line -->
      <v-data-table hide-default-footer :headers="headers" :items="processedVisiblePurchases" @click:row="onRowClick">
        <template v-slot:[`item.category`]="{ item }">
          <v-chip small :color="getDisplayValue(item.category).color" dark>
            {{ getDisplayValue(item.category).text }}
          </v-chip>
        </template>
        <template v-slot:[`item.priceHt`]="{ item }">{{ item.priceHt }} €</template>

        <template v-slot:[`no-data`]>
          <div class="mx-10 my-10">
            Cliquer sur le bouton "Ajouter une ligne" pour rentrer vos achats.
          </div>
        </template>
      </v-data-table>
    </v-card>
    <v-row>
      <v-spacer></v-spacer>
      <v-col cols="12" sm="6">
        <v-pagination
          v-if="page && purchaseCount"
          v-model="page"
          :length="Math.ceil(purchaseCount / limit)"
          :total-visible="7"
        ></v-pagination>
      </v-col>
      <v-spacer></v-spacer>
    </v-row>
  </div>
</template>

<script>
export default {
  name: "InvoicesHome",
  data() {
    return {
      search: "",
      visiblePurchases: null,
      purchaseCount: null,
      page: null,
      limit: 10,
      headers: [
        {
          text: "Date",
          align: "start",
          filterable: false,
          value: "date",
          sortable: false,
        },
        { text: "Fournisseur", value: "provider", sortable: false },
        { text: "Catégorie", value: "category", sortable: false },
        { text: "Cantine", value: "canteen.name", sortable: false },
        { text: "Prix HT", value: "priceHt", sortable: false },
      ],
    }
  },
  computed: {
    loading() {
      return this.purchaseCount === null
    },
    offset() {
      return (this.page - 1) * this.limit
    },
    processedVisiblePurchases() {
      const canteens = this.$store.state.userCanteenPreviews
      return this.visiblePurchases.map((x) => Object.assign(x, { canteen: canteens.find((y) => y.id === x.canteen) }))
    },
  },
  methods: {
    getDisplayValue(category) {
      switch (category) {
        case "VIANDES_VOLAILLES":
          return { text: "Viandes / volailles", color: "deep-orange darken-1" }
        case "FRUITS_ET_LEGUMES":
          return { text: "Fruits et légumes", color: "green darken-1" }
        case "PRODUITS_DE_LA_MER":
          return { text: "Pêche", color: "light-blue darken-1" }
        case "PRODUITS_LAITIERS":
          return { text: "Produits laitiers", color: "lime darken-2" }
        case "PRODUITS_CEREALIERS":
          return { text: "Produits transformés", color: "deep-purple darken-1" }
        default:
          return { text: "Autre", color: "blue-grey darken-1" }
      }
    },
    onRowClick(purchase) {
      this.$router.push({ name: "InvoicePage", params: { id: purchase.id } })
    },
    fetchCurrentPage() {
      let queryParam = `limit=${this.limit}&offset=${this.offset}`
      return fetch(`/api/v1/purchases/?${queryParam}`)
        .then((response) => {
          if (response.status < 200 || response.status >= 400) throw new Error(`Error encountered : ${response}`)
          return response.json()
        })
        .then((response) => {
          this.purchaseCount = response.count
          this.visiblePurchases = response.results
        })
        .catch(() => {
          this.publishedCanteenCount = 0
          this.$store.dispatch("notifyServerError")
        })
    },
  },
  watch: {
    page(newPage) {
      // The empty catch is the suggested error management here : https://github.com/vuejs/vue-router/issues/2872#issuecomment-519073998
      this.$router.push({ query: { page: newPage } }).catch(() => {})
      if (!this.visiblePurchases) this.fetchCurrentPage()
    },
    $route(newRoute) {
      this.page = newRoute.query.page ? parseInt(newRoute.query.page) : 1
      this.fetchCurrentPage()
    },
  },
  mounted() {
    this.page = this.$route.query.page ? parseInt(this.$route.query.page) : 1
  },
}
</script>

<style scoped>
.v-data-table >>> tbody tr:not(.v-data-table__empty-wrapper) {
  cursor: pointer;
}
</style>
