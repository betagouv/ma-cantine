<template>
  <div class="text-left">
    <div class="d-flex">
      <div>
        <h1 class="font-weight-black text-h5 text-sm-h4 my-4" style="width: 100%">
          Mes achats
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
      <v-data-table hide-default-footer :headers="headers" :items="processedVisiblePurchases" @click:row="onRowClick">
        <template v-slot:[`item.category`]="{ item }">
          <v-chip outlined small :color="getDisplayValue(item.category).color" dark class="font-weight-bold">
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
      return this.visiblePurchases.map((x) => {
        const canteen = canteens.find((y) => y.id === x.canteen)
        const date = x.date ? this.getReadableDate(x.date) : null
        return Object.assign(x, { canteen, date })
      })
    },
  },
  methods: {
    getDisplayValue(category) {
      const categoryHash = {
        VIANDES_VOLAILLES: { text: "Viandes, volailles", color: "red darken-4" },
        PRODUITS_DE_LA_MER: { text: "Produits de la mer", color: "pink darken-4" },
        FRUITS_ET_LEGUMES: { text: "Fruits, légumes, légumineuses et oléagineux", color: "purple darken-4" },
        PRODUITS_CEREALIERS: { text: "Produits céréaliers", color: "deep-purple darken-4" },
        ENTREES: { text: "Entrées et plats composés", color: "indigo darken-4" },
        PRODUITS_LAITIERS: { text: "Lait et produits laitiers", color: "blue darken-4" },
        BOISSONS: { text: "Boissons", color: "light-blue darken-4" },
        AIDES: { text: "Aides culinaires et ingrédients divers", color: "cyan darken-4" },
        BEURRE_OEUF_FROMAGE: { text: "Beurre, oeuf, fromage", color: "teal darken-4" },
        PRODUITS_SUCRES: { text: "Produits sucrés", color: "green darken-4" },
        ALIMENTS_INFANTILES: { text: "Aliments infantiles", color: "light-green darken-4" },
        GLACES_SORBETS: { text: "Glaces et sorbets", color: "blue-grey darken-4" },
        AUTRES: { text: "Autres", color: "brown darken-4" },
      }

      if (Object.prototype.hasOwnProperty.call(categoryHash, category)) return categoryHash[category]
      return { text: "", color: "" }
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
    getReadableDate(dateString) {
      const options = {
        year: "numeric",
        month: "short",
        day: "numeric",
      }
      const dateSegments = dateString.split("-")
      const date = new Date(parseInt(dateSegments[0]), parseInt(dateSegments[1]) - 1, parseInt(dateSegments[2]))
      return date.toLocaleString("fr", options)
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
.v-data-table >>> tbody tr:not(.v-data-table__empty-wrapper),
.v-data-table >>> .v-chip {
  cursor: pointer;
}
</style>
