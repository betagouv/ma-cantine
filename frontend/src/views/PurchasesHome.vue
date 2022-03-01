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
          Ajouter un produit
        </v-btn>
      </div>
      <v-spacer></v-spacer>

      <v-img
        src="/static/images/doodles/primary/ChartDoodle.png"
        v-if="$vuetify.breakpoint.smAndUp"
        class="mx-auto rounded-0"
        contain
        max-width="150"
      ></v-img>
    </div>
    <v-card outlined class="my-4" v-if="visiblePurchases">
      <div class="d-flex pa-2">
        <v-text-field
          v-model="searchTerm"
          append-icon="mdi-magnify"
          label="Chercher par produit ou fournisseur"
          style="max-width: 450px;"
          outlined
          dense
          hide-details
          clearable
          @click:clear="clearSearch"
          @keyup.enter="search"
        ></v-text-field>
        <v-btn outlined color="primary" class="mx-4" height="40px" @click="search">
          <v-icon>mdi-magnify</v-icon>
          Chercher
        </v-btn>
      </div>

      <div class="d-flex align-center mb-2">
        <v-badge :value="hasActiveFilter" color="secondary" dot overlap>
          <v-btn text color="primary" small @click="showFilters = !showFilters" class="ml-1">
            <v-icon small>mdi-filter-outline</v-icon>
            <span v-if="showFilters">Cacher les &nbsp;</span>
            <span v-else>Afficher les &nbsp;</span>
            filtres
          </v-btn>
        </v-badge>
        <v-divider v-if="hasActiveFilter" style="max-width: 20px;"></v-divider>
        <v-btn text color="primary" small @click="clearFilters" v-if="hasActiveFilter">
          <v-icon small>mdi-filter-off-outline</v-icon>
          Enlever tous les filtres
        </v-btn>

        <v-divider></v-divider>
      </div>
      <v-expand-transition>
        <div v-show="showFilters" class="pa-2">
          <v-row>
            <v-col cols="12" sm="6" md="4">
              <v-select
                v-model="appliedFilters.category"
                :items="categories"
                label="Catégorie"
                hide-details
                dense
                outlined
                clearable
                class="mt-2"
              ></v-select>
            </v-col>
            <v-col cols="12" sm="6">
              <v-select
                v-model="appliedFilters.characteristics"
                :items="characteristics"
                label="Caractéristiques"
                hide-details
                dense
                outlined
                clearable
                multiple
                class="mt-2"
              ></v-select>
            </v-col>
          </v-row>
          <v-row>
            <v-menu
              v-model="startDateMenu"
              :close-on-content-click="true"
              transition="scale-transition"
              offset-y
              min-width="auto"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-col cols="12" sm="6" md="3">
                  <v-text-field
                    :value="appliedFilters.startDate"
                    prepend-icon="mdi-calendar"
                    readonly
                    v-bind="attrs"
                    v-on="on"
                    hide-details
                    outlined
                    dense
                    clearable
                    label="Après"
                    @click:clear="appliedFilters.startDate = null"
                  ></v-text-field>
                </v-col>
              </template>

              <v-date-picker v-model="appliedFilters.startDate" locale="fr-FR"></v-date-picker>
            </v-menu>
            <v-menu
              v-model="endDateMenu"
              :close-on-content-click="true"
              transition="scale-transition"
              offset-y
              min-width="auto"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-col cols="12" sm="6" md="3">
                  <v-text-field
                    :value="appliedFilters.endDate"
                    prepend-icon="mdi-calendar"
                    readonly
                    v-bind="attrs"
                    v-on="on"
                    hide-details
                    outlined
                    dense
                    clearable
                    label="Avant"
                    @click:clear="appliedFilters.endDate = null"
                  ></v-text-field>
                </v-col>
              </template>

              <v-date-picker v-model="appliedFilters.endDate" locale="fr-FR"></v-date-picker>
            </v-menu>
          </v-row>
        </div>
      </v-expand-transition>
      <v-divider></v-divider>
      <v-data-table
        :options.sync="options"
        :loading="loading"
        :server-items-length="purchaseCount || 0"
        :headers="headers"
        :items="processedVisiblePurchases"
        @click:row="onRowClick"
      >
        <template v-slot:[`item.category`]="{ item }">
          <v-chip outlined small :color="getCategoryDisplayValue(item.category).color" dark class="font-weight-bold">
            {{ getCategoryDisplayValue(item.category).text }}
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
import Constants from "@/constants"

export default {
  name: "PurchasesHome",
  data() {
    return {
      searchTerm: null,
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
        { text: "Produit", value: "description", sortable: true },
        { text: "Catégorie", value: "category", sortable: false },
        { text: "Cantine", value: "canteen__name", sortable: true },
        { text: "Prix HT", value: "priceHt", sortable: true },
        { text: "", value: "hasAttachment", sortable: false },
      ],
      categories: [],
      characteristics: [],
      showFilters: false,
      startDateMenu: false,
      endDateMenu: false,
      appliedFilters: {
        category: null,
        characteristics: [],
        startDate: null,
        endDate: null,
      },
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
    hasActiveFilter() {
      return (
        this.appliedFilters.category !== null ||
        this.appliedFilters.characteristics.length !== 0 ||
        this.appliedFilters.startDate !== null ||
        this.appliedFilters.endDate !== null
      )
    },
    // TODO: format choice lists to have explanation of inactive choices
  },
  methods: {
    getCategoryDisplayValue(category) {
      if (Object.prototype.hasOwnProperty.call(Constants.Categories, category)) return Constants.Categories[category]
      return { text: "", color: "" }
    },
    getCharacteristicDisplayValue(characteristic) {
      if (Object.prototype.hasOwnProperty.call(Constants.Characteristics, characteristic))
        return Constants.Characteristics[characteristic]
      return { text: "" }
    },
    onRowClick(purchase) {
      this.$router.push({ name: "PurchasePage", params: { id: purchase.id } })
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
          this.categories = response.categories
            .map((c) => {
              const displayValue = this.getCategoryDisplayValue(c)
              return displayValue.text ? { text: displayValue.text, value: c } : null
            })
            .filter((x) => !!x)
          this.characteristics = response.characteristics
            .map((c) => {
              const displayValue = this.getCategoryDisplayValue(c)
              return displayValue.text ? { text: displayValue.text, value: c } : null
            })
            .filter((x) => !!x)
          this.canteens = response.canteens.map((c) => ({ text: c, value: c }))
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
      if (this.searchTerm) apiQueryParams += `&search=${this.searchTerm}`
      if (this.appliedFilters.category) apiQueryParams += `&category=${this.appliedFilters.category}`
      if (this.appliedFilters.startDate) apiQueryParams += `&date_after=${this.appliedFilters.startDate}`
      if (this.appliedFilters.endDate) apiQueryParams += `&date_before=${this.appliedFilters.endDate}`
      if (this.appliedFilters.characteristics.length > 0)
        apiQueryParams += `&characteristics=${this.appliedFilters.characteristics.join(",")}`
      return apiQueryParams
    },
    getUrlQueryParams() {
      let urlQueryParams = { page: this.options.page }
      const orderingItems = this.getOrderingItems()
      if (orderingItems.length > 0) urlQueryParams["trier-par"] = orderingItems.join(",")
      if (this.searchTerm) urlQueryParams["recherche"] = this.searchTerm
      if (this.appliedFilters.category)
        urlQueryParams["categorie"] = this.getCategoryDisplayValue(this.appliedFilters.category).text
      if (this.appliedFilters.startDate) urlQueryParams["après"] = this.appliedFilters.startDate
      if (this.appliedFilters.endDate) urlQueryParams["avant"] = this.appliedFilters.endDate
      if (this.appliedFilters.characteristics.length > 0)
        urlQueryParams["caracteristiques"] = this.appliedFilters.characteristics
          .map((c) => this.getCharacteristicDisplayValue(c).text)
          .join(",")
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
      this.searchTerm = this.$route.query.recherche || null
      let sortBy = []
      let sortDesc = []

      this.$route.query["trier-par"] &&
        this.$route.query["trier-par"].split(",").forEach((element) => {
          const isDesc = element[0] === "-"
          sortBy.push(isDesc ? element.slice(1) : element)
          sortDesc.push(isDesc)
        })
      this.$set(this, "options", { sortBy, sortDesc, page })
      this.$set(this, "appliedFilters", {
        startDate: this.$route.query.après || null,
        endDate: this.$route.query.avant || null,
        characteristics: [],
        category: null,
      })
      // TODO: populate characteristics, transforming human-readable text to API-friendly text
      // TODO: populate category
    },
    clearSearch() {
      this.searchTerm = ""
      this.search()
    },
    search() {
      if (this.searchTerm && this.options.page !== 1) this.options.page = 1
      else this.$router.push({ query: this.getUrlQueryParams() }).catch(() => {})
    },
    applyFilters() {
      if (this.options.page !== 1) this.options.page = 1
      else this.$router.push({ query: this.getUrlQueryParams() }).catch(() => {})
    },
    clearFilters() {
      this.$set(this, "appliedFilters", {
        startDate: null,
        endDate: null,
        characteristics: [],
        category: null,
      })
    },
  },
  watch: {
    appliedFilters: {
      handler() {
        this.applyFilters()
      },
      deep: true,
    },
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
    if (this.hasActiveFilter) this.showFilters = true
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
