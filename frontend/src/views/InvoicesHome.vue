<template>
  <div class="text-left">
    <div class="d-flex">
      <div>
        <h1 class="font-weight-black text-h5 text-sm-h4 my-4" style="width: 100%">
          Mes achats
        </h1>
        <p>
          Une alimentation saine et durable commence par un suivi comptable de vos achats. Des nouvelles fonctionnalités
          arrivent bientôt dans cet espace !
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
      <v-data-table
        :options.sync="options"
        :loading="loading"
        :server-items-length="purchaseCount || 0"
        :headers="headers"
        :items="processedVisiblePurchases"
        @click:row="onRowClick"
      >
        <template v-slot:[`item.category`]="{ item }">
          <v-chip outlined small :color="getDisplayValue(item.category).color" dark class="font-weight-bold">
            {{ getDisplayValue(item.category).text }}
          </v-chip>
        </template>
        <template v-slot:[`item.priceHt`]="{ item }">{{ item.priceHt }} €</template>
        <template v-slot:[`item.hasAttachment`]="{ item }">
          <v-icon small color="grey" v-if="item.hasAttachment" aria-label="Has invoice file" :aria-hidden="false">
            mdi-paperclip
          </v-icon>
        </template>

        <template v-slot:[`no-data`]>
          <div class="mx-10 my-10">
            Cliquer sur le bouton "Ajouter une ligne" pour rentrer vos achats.
          </div>
        </template>
      </v-data-table>
    </v-card>
  </div>
</template>

<script>
import { formatDate } from "@/utils"

export default {
  name: "InvoicesHome",
  data() {
    return {
      search: "",
      loading: false,
      visiblePurchases: null,
      purchaseCount: null,
      limit: 10,
      options: {
        sortBy: [],
        sortDesc: [],
        page: null,
      },
      headers: [
        {
          text: "Date",
          align: "start",
          filterable: false,
          value: "date",
          sortable: true,
        },
        { text: "Fournisseur", value: "provider", sortable: true },
        { text: "Catégorie", value: "category", sortable: false },
        { text: "Cantine", value: "canteen__name", sortable: true },
        { text: "Prix HT", value: "priceHt", sortable: true },
        { text: "", value: "hasAttachment", sortable: false },
      ],
    }
  },
  computed: {
    offset() {
      return (this.options.page - 1) * this.limit
    },
    processedVisiblePurchases() {
      const canteens = this.$store.state.userCanteenPreviews
      return this.visiblePurchases.map((x) => {
        const canteen = canteens.find((y) => y.id === x.canteen)
        const date = x.date ? formatDate(x.date) : null
        const hasAttachment = !!x.invoiceFile
        return Object.assign(x, { canteen__name: canteen?.name, date, hasAttachment })
      })
    },
  },
  methods: {
    getDisplayValue(category) {
      const categoryHash = {
        VIANDES_VOLAILLES: { text: "Viandes, volailles", color: "red darken-4" },
        PRODUITS_DE_LA_MER: { text: "Produits de la mer", color: "pink darken-4" },
        FRUITS_ET_LEGUMES: {
          text: this.$vuetify.breakpoint.smAndUp
            ? "Fruits, légumes, légumineuses et oléagineux"
            : "Fruits, légumes, ...",
          color: "purple darken-4",
        },
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
      this.loading = true
      return fetch(`/api/v1/purchases/?${this.getApiQueryParams()}`)
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
        .finally(() => {
          this.loading = false
        })
    },
    getApiQueryParams() {
      let apiQueryParams = `limit=${this.limit}&offset=${this.offset}`
      const orderingItems = this.getOrderingItems()
      if (orderingItems.length > 0) apiQueryParams += `&ordering=${orderingItems.join(",")}`
      return apiQueryParams
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
      if (!this.$route.query["trier-par"]) {
        this.$set(this, "options", { page })
        return
      }
      let sortBy = []
      let sortDesc = []
      this.$route.query["trier-par"].split(",").forEach((element) => {
        const isDesc = element[0] === "-"
        sortBy.push(isDesc ? element.slice(1) : element)
        sortDesc.push(isDesc)
      })
      this.$set(this, "options", { sortBy, sortDesc, page })
    },
  },
  watch: {
    options() {
      const replace = Object.keys(this.$route.query).length === 0
      if (replace) this.$router.replace({ query: this.getUrlQueryParams() }).catch(() => {})
      else this.$router.push({ query: this.getUrlQueryParams() }).catch(() => {})
      if (!this.visiblePurchases && !this.loading) this.fetchCurrentPage()
    },
    $route() {
      this.populateParametersFromRoute()
      this.fetchCurrentPage()
    },
  },
  mounted() {
    this.populateParametersFromRoute()
  },
}
</script>

<style scoped>
.v-data-table >>> tbody tr:not(.v-data-table__empty-wrapper),
.v-data-table >>> .v-chip {
  cursor: pointer;
}

/* Hides items-per-row */
.v-data-table >>> .v-data-footer__select {
  visibility: hidden;
}
</style>
