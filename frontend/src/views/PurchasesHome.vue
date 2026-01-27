<template>
  <div class="text-left">
    <BreadcrumbsNav />
    <div class="d-flex">
      <div>
        <h1 class="font-weight-black text-h5 text-sm-h4 mb-4" style="width: 100%">
          Mes achats
        </h1>
        <p>
          Une alimentation saine et durable commence par un suivi comptable de vos achats. Des nouvelles fonctionnalités
          arrivent bientôt dans cet espace !
        </p>
        <v-row v-if="hasCanteens" align="center" class="px-3">
          <v-btn color="primary" :to="{ name: 'NewPurchase' }" large class="mr-2 my-3">
            <v-icon>mdi-plus</v-icon>
            Ajouter un produit
          </v-btn>
          <v-btn text color="primary" :to="{ name: 'GestionnaireImport' }" class="px-0 px-md-2 my-3">
            <v-icon class="mr-2">mdi-file-upload-outline</v-icon>
            Créer plusieurs achats depuis un fichier
          </v-btn>
          <v-btn
            text
            color="primary"
            :to="{ name: 'PurchasesSummary' }"
            class="px-0 px-md-2 my-3"
            v-if="$vuetify.breakpoint.xs"
          >
            <v-icon class="mr-2">$pie-chart-2-fill</v-icon>
            Voir la synthèse de mes achats
          </v-btn>
        </v-row>
        <p class="font-weight-bold" v-else>
          Pour commencer à suivre vos achats, veuillez ajouter une cantine.
        </p>
      </div>
      <v-spacer></v-spacer>

      <v-card
        class="dsfr d-flex flex-column justify-center"
        :to="{ name: 'PurchasesSummary' }"
        min-width="300px"
        v-if="purchaseCount && $vuetify.breakpoint.smAndUp"
      >
        <v-card-text class="text-center">
          <v-icon x-large color="primary">
            $pie-chart-2-fill
          </v-icon>
        </v-card-text>
        <v-card-text class="text-center text-body-1 font-weight-bold py-0">
          <p class="mb-0">
            La synthèse de vos achats
          </p>
        </v-card-text>
        <v-card-text class="text-center pt-2">
          <p class="mb-0">
            Cliquez ici pour visualiser les données relatives à vos achats
          </p>
        </v-card-text>
      </v-card>
      <v-img
        src="/static/images/doodles-dsfr/primary/ChartDoodle.png"
        v-else-if="$vuetify.breakpoint.smAndUp"
        class="mx-auto rounded-0"
        contain
        max-width="150"
        :style="purchaseCount === null ? 'visibility: hidden;' : ''"
      ></v-img>
    </div>

    <PurchasesToolExplanation class="my-1" />
    <v-card outlined v-if="hasCanteens && visiblePurchases">
      <v-row class="px-4 mt-2" align="center">
        <v-col cols="12" sm="8" class="py-0">
          <DsfrSearchField
            v-model="searchTerm"
            placeholder="Chercher par produit ou fournisseur"
            hide-details
            clearable
            @clear="clearSearch"
            @search="search"
          />
        </v-col>
        <v-spacer v-if="$vuetify.breakpoint.smAndUp"></v-spacer>
        <v-col class="pb-sm-0">
          <a :href="exportUrl" class="primary--text body-2 mr-sm-4 text-no-wrap" download>
            <v-icon class="mr-1" color="primary">mdi-microsoft-excel</v-icon>
            Exporter mes achats
          </a>
        </v-col>
      </v-row>

      <div class="d-flex align-center mt-2 mt-sm-6 mb-2">
        <v-badge :value="hasActiveFilter" color="#CE614A" dot overlap>
          <v-btn text color="primary" small @click="showFilters = !showFilters" class="ml-1 py-4 py-sm-0">
            <v-icon small>mdi-filter-outline</v-icon>
            <span v-if="showFilters">Cacher les filtres</span>
            <span v-else>Afficher les filtres</span>
          </v-btn>
        </v-badge>
        <v-divider aria-hidden="true" role="presentation" v-if="hasActiveFilter" style="max-width: 20px;"></v-divider>
        <v-btn text color="primary" small @click="clearFilters" v-if="hasActiveFilter">
          <v-icon small>mdi-filter-off-outline</v-icon>
          Enlever tous les filtres
        </v-btn>

        <v-divider aria-hidden="true" role="presentation"></v-divider>
      </div>
      <v-expand-transition>
        <div v-show="showFilters" class="px-4 pb-6 pt-0">
          <v-row v-if="userCanteens.length > 1">
            <v-col cols="12" sm="8">
              <label
                for="filter-canteen"
                :class="{ 'text-body-2': true, 'active-filter-label': appliedFilters.canteen > 0 }"
              >
                Établissement
              </label>
              <DsfrAutocomplete
                id="filter-canteen"
                v-model="appliedFilters.canteen"
                :items="userCanteens"
                item-text="name"
                item-value="id"
                auto-select-first
                hide-details
                clearable
                class="mt-2"
              />
            </v-col>
          </v-row>
          <v-row class="mt-0">
            <v-col cols="12" sm="6" md="5">
              <label
                for="filter-family"
                :class="{ 'text-body-2': true, 'active-filter-label': !!appliedFilters.family }"
              >
                Famille de produit
              </label>
              <DsfrSelect
                v-model="appliedFilters.family"
                id="filter-family"
                :items="productFamilies"
                hide-details
                clearable
                class="mt-2"
              />
            </v-col>
            <v-col cols="12" sm="5">
              <label
                for="filter-characteristics"
                :class="{ 'text-body-2': true, 'active-filter-label': appliedFilters.characteristics.length > 0 }"
              >
                Caractéristiques
              </label>
              <DsfrSelect
                id="filter-characteristics"
                v-model="appliedFilters.characteristics"
                :items="characteristics"
                hide-details
                clearable
                multiple
                class="mt-2"
              />
            </v-col>
          </v-row>
          <v-row class="mt-0">
            <v-menu
              v-model="startDateMenu"
              :close-on-content-click="false"
              transition="scale-transition"
              offset-y
              min-width="auto"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-col cols="12" sm="6" md="3">
                  <label
                    for="filter-startdate"
                    :class="{ 'text-body-2': true, 'active-filter-label': !!appliedFilters.startDate }"
                  >
                    Après
                  </label>
                  <DsfrTextField
                    :value="appliedFilters.startDate"
                    prepend-icon="$calendar-event-fill"
                    readonly
                    v-bind="attrs"
                    v-on="on"
                    hide-details
                    clearable
                    id="filter-startdate"
                    @click:clear="appliedFilters.startDate = null"
                  />
                </v-col>
              </template>

              <v-date-picker
                v-model="appliedFilters.startDate"
                locale="fr-FR"
                @change="startDateMenu = false"
              ></v-date-picker>
            </v-menu>
            <v-menu
              v-model="endDateMenu"
              :close-on-content-click="false"
              transition="scale-transition"
              offset-y
              min-width="auto"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-col cols="12" sm="6" md="3">
                  <label
                    for="filter-enddate"
                    :class="{ 'text-body-2': true, 'active-filter-label': !!appliedFilters.endDate }"
                  >
                    Avant
                  </label>
                  <DsfrTextField
                    :value="appliedFilters.endDate"
                    prepend-icon="$calendar-event-fill"
                    readonly
                    v-bind="attrs"
                    v-on="on"
                    hide-details
                    clearable
                    id="filter-enddate"
                    @click:clear="appliedFilters.endDate = null"
                  />
                </v-col>
              </template>

              <v-date-picker
                v-model="appliedFilters.endDate"
                locale="fr-FR"
                @change="endDateMenu = false"
              ></v-date-picker>
            </v-menu>
          </v-row>
        </div>
      </v-expand-transition>
      <v-divider aria-hidden="true" role="presentation"></v-divider>
      <v-data-table
        :options.sync="options"
        :loading="loading"
        :server-items-length="purchaseCount || 0"
        :headers="headers"
        :items="processedVisiblePurchases"
        @click:row="onRowClick"
        v-model="selectedPurchases"
        show-select
      >
        <template v-slot:[`item.description`]="{ item }">
          <router-link :to="{ name: 'PurchasePage', params: { id: item.id } }">
            {{ item.description || "[sans description]" }}
            <span class="d-sr-only">, {{ item.date }}</span>
          </router-link>
        </template>
        <template v-slot:[`item.family`]="{ item }">
          <v-chip outlined small :color="getProductFamilyDisplayValue(item.family).color" dark class="font-weight-bold">
            {{ capitalise(getProductFamilyDisplayValue(item.family).shortText) }}
          </v-chip>
        </template>
        <template v-slot:[`item.characteristics`]="{ item }">
          {{ getProductCharacteristicsDisplayValue(item.characteristics) }}
        </template>
        <template v-slot:[`item.priceHt`]="{ item }">
          {{ item.priceHt.toLocaleString("fr-FR", { style: "currency", currency: "EUR" }) }}
        </template>
        <template v-slot:[`item.hasAttachment`]="{ item }">
          <v-icon small color="grey" v-if="item.hasAttachment" aria-label="Facture attachée" :aria-hidden="false">
            mdi-paperclip
          </v-icon>
        </template>
        <template v-slot:[`item.actions`]="{ item }">
          <div class="d-flex justify-center">
            <v-icon @click.stop="duplicate(item)" color="primary" :title="duplicatePurchaseInstruction(item)">
              $file-add-line
            </v-icon>
          </div>
        </template>

        <template v-slot:[`no-data`]>
          <div class="mx-10 my-10">
            Cliquer sur le bouton "Ajouter une ligne" pour rentrer vos achats.
          </div>
        </template>
      </v-data-table>
      <v-expand-transition>
        <div v-show="selectedPurchases.length" class="px-4 pb-4 mt-n10">
          <v-btn @click="deleteSelectedPurchases" color="red darken-2" class="white--text">
            <v-icon class="mr-1" small>mdi-delete-forever</v-icon>
            Supprimer {{ selectedPurchases.length }} {{ selectedPurchases.length > 1 ? "achats" : "achat" }}
          </v-btn>
        </div>
      </v-expand-transition>
    </v-card>
    <v-row v-else-if="visiblePurchases" class="mt-4">
      <v-col cols="12" sm="6" md="4" height="100%" class="d-flex flex-column">
        <v-card
          class="dsfr d-flex flex-column align-center justify-center"
          outlined
          min-height="220"
          height="80%"
          :to="{ name: 'GestionnaireCantineRestaurantAjouter' }"
        >
          <v-icon size="100" class="primary--text">mdi-plus</v-icon>
          <v-card-text class="font-weight-bold pt-0 text-center primary--text">
            <p class="mb-0">
              Ajouter une cantine
            </p>
          </v-card-text>
        </v-card>
        <v-spacer></v-spacer>
        <div class="d-flex mt-4 mb-2 align-center px-2">
          <v-divider aria-hidden="true" role="presentation"></v-divider>
          <p class="mx-2 my-0 caption">ou</p>
          <v-divider aria-hidden="true" role="presentation"></v-divider>
        </div>
        <v-spacer></v-spacer>
        <v-btn text color="primary" :to="{ name: 'GestionnaireImportCantines' }">
          <v-icon class="mr-2">mdi-file-upload-outline</v-icon>
          Créer plusieurs cantines depuis un fichier
        </v-btn>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import { formatDate, getObjectDiff, normaliseText, capitalise } from "@/utils"
import Constants from "@/constants"
import DsfrTextField from "@/components/DsfrTextField"
import BreadcrumbsNav from "@/components/BreadcrumbsNav"
import DsfrSelect from "@/components/DsfrSelect"
import DsfrSearchField from "@/components/DsfrSearchField"
import DsfrAutocomplete from "@/components/DsfrAutocomplete"
import PurchasesToolExplanation from "@/components/PurchasesToolExplanation"

export default {
  name: "PurchasesHome",
  components: {
    DsfrTextField,
    BreadcrumbsNav,
    DsfrSelect,
    DsfrSearchField,
    DsfrAutocomplete,
    PurchasesToolExplanation,
  },
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
        page: 1,
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
        { text: "Famille", value: "family", sortable: true },
        { text: "Caratéristiques", value: "characteristics", sortable: false },
        { text: "Cantine", value: "canteen__name", sortable: true },
        { text: "Prix HT", value: "priceHt", sortable: true, align: "end" },
        { text: "", value: "hasAttachment", sortable: false },
        { text: "Dupliquer", value: "actions", sortable: false },
      ],
      productFamilies: [],
      characteristics: [],
      showFilters: false,
      startDateMenu: false,
      endDateMenu: false,
      appliedFilters: {
        family: null,
        canteen: null,
        characteristics: [],
        startDate: null,
        endDate: null,
      },
      selectedPurchases: [],
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
    exportUrl() {
      return `/api/v1/export-achats.xlsx?${this.getApiQueryParams(false)}`
    },
    hasActiveFilter() {
      return (
        this.appliedFilters.family !== null ||
        this.appliedFilters.characteristics.length !== 0 ||
        this.appliedFilters.startDate !== null ||
        this.appliedFilters.endDate !== null ||
        this.appliedFilters.canteen !== null
      )
    },
    hasCanteens() {
      return !!this.$store.state.userCanteenPreviews && this.$store.state.userCanteenPreviews.length > 0
    },
    // TODO: format choice lists to have explanation of inactive choices
    userCanteens() {
      const canteens = this.$store.state.userCanteenPreviews
      return canteens.sort((a, b) => {
        return normaliseText(a.name) > normaliseText(b.name) ? 1 : 0
      })
    },
  },
  methods: {
    getProductFamilyDisplayValue(family) {
      if (Object.prototype.hasOwnProperty.call(Constants.ProductFamilies, family))
        return Constants.ProductFamilies[family]
      return { text: "", shortText: "", color: "" }
    },
    getProductCharacteristicsDisplayValue(characteristics) {
      const priorityOrder = Object.keys(Constants.Characteristics)
      characteristics = characteristics.filter((c) => priorityOrder.indexOf(c) > -1)
      characteristics.sort((a, b) => {
        return priorityOrder.indexOf(a) - priorityOrder.indexOf(b)
      })
      const displayCount = 3
      const remaining = characteristics.length - displayCount
      characteristics.splice(displayCount)
      let str = characteristics.map((c) => this.getCharacteristicDisplayValue(c).text).join(", ")
      if (remaining > 0) str += ` et ${remaining} autre${remaining > 1 ? "s" : ""}`
      return str
    },
    getCharacteristicDisplayValue(characteristic) {
      if (Object.prototype.hasOwnProperty.call(Constants.Characteristics, characteristic))
        return Constants.Characteristics[characteristic]
      return { text: "" }
    },
    getChoiceValueFromText(choices, displayText) {
      const entry = Object.entries(choices).find((c) => c[1].text === displayText)
      return entry ? entry[0] : null
    },
    onRowClick(purchase) {
      const purchaseIndex = this.selectedPurchases.findIndex((p) => p.id === purchase.id)
      if (purchaseIndex === -1) this.selectedPurchases.push(purchase)
      else this.selectedPurchases.splice(purchaseIndex, 1)
    },
    // the following requires that purchases are SoftDeletionObjects
    // in 2nd PR: if too many purchase objects in soft deleted state, make weekly bot to clear out purchases that have been deleted for > 1 week (or whatever time period)
    deleteSelectedPurchases() {
      const selectedCount = this.selectedPurchases.length
      if (!selectedCount) return
      const ids = this.selectedPurchases.map((p) => p.id)
      this.$store
        .dispatch("deletePurchases", { ids })
        .then(() => {
          const title =
            selectedCount === 1 ? "L'achat a bien été supprimé" : `${selectedCount} achats ont bien été supprimés`
          this.$store.dispatch("notify", {
            title,
            status: "success",
            undoMessage: "Restaurer achats",
            undoAction: this.recoverDeletedPurchases(ids),
          })
          this.selectedPurchases = []
          this.fetchCurrentPage()
        })
        .catch((e) => {
          this.$store.dispatch("notifyServerError", e)
        })
    },
    recoverDeletedPurchases(ids) {
      return () => {
        this.$store
          .dispatch("restorePurchases", ids)
          .then((response) => {
            const title =
              response.count === 1 ? "L'achat a bien été restauré" : `${response.count} achats ont bien été restaurés`
            this.$store.dispatch("notify", {
              title,
              status: "success",
            })
            this.selectedPurchases = []
            this.fetchCurrentPage()
          })
          .catch((e) => {
            this.$store.dispatch("notifyServerError", e)
          })
      }
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
          this.productFamilies = response.families
            .map((c) => {
              const displayValue = this.getProductFamilyDisplayValue(c)
              return displayValue.text ? { text: displayValue.text, value: c } : null
            })
            .filter((x) => !!x)
          this.characteristics = response.characteristics
            .map((c) => {
              const displayValue = this.getCharacteristicDisplayValue(c)
              return displayValue.text ? { text: displayValue.text, value: c } : null
            })
            .filter((x) => !!x)
          this.canteens = response.canteens.map((c) => ({ text: c, value: c }))
        })
        .catch((e) => {
          this.$store.dispatch("notifyServerError", e)
        })
        .finally(() => {
          this.loading = false
        })
    },
    getApiQueryParams(includePagination = true) {
      let apiQueryParams = includePagination ? `limit=${this.limit}&offset=${this.offset}` : ""
      const orderingItems = this.getOrderingItems()
      if (orderingItems.length > 0) apiQueryParams += `&ordering=${orderingItems.join(",")}`
      if (this.searchTerm) apiQueryParams += `&search=${this.searchTerm}`
      if (this.appliedFilters.family) apiQueryParams += `&family=${this.appliedFilters.family}`
      if (this.appliedFilters.startDate) apiQueryParams += `&date_after=${this.appliedFilters.startDate}`
      if (this.appliedFilters.endDate) apiQueryParams += `&date_before=${this.appliedFilters.endDate}`
      if (this.appliedFilters.canteen) apiQueryParams += `&canteen__id=${this.appliedFilters.canteen}`
      if (this.appliedFilters.characteristics.length > 0)
        apiQueryParams += `&characteristics=${this.appliedFilters.characteristics.join("&characteristics=")}`
      return apiQueryParams
    },
    getUrlQueryParams() {
      let urlQueryParams = { page: this.options.page }
      const orderingItems = this.getOrderingItems()
      if (orderingItems.length > 0) urlQueryParams["trier-par"] = orderingItems.join(",")
      if (this.searchTerm) urlQueryParams["recherche"] = this.searchTerm
      if (this.appliedFilters.family)
        urlQueryParams["famille"] = this.getProductFamilyDisplayValue(this.appliedFilters.family).text
      if (this.appliedFilters.startDate) urlQueryParams["après"] = this.appliedFilters.startDate
      if (this.appliedFilters.endDate) urlQueryParams["avant"] = this.appliedFilters.endDate
      if (this.appliedFilters.canteen) urlQueryParams["cantine"] = this.appliedFilters.canteen
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

      const newOptions = { sortBy, sortDesc, page }
      const optionChanges = this.options ? getObjectDiff(this.options, newOptions) : newOptions
      if (Object.keys(optionChanges).length > 0) this.$set(this, "options", newOptions)

      let characteristics = []
      const queryCharacteristics = (this.$route.query.caracteristiques || "").split(",")
      queryCharacteristics.forEach((displayCharacteristic) => {
        const value = this.getChoiceValueFromText(Constants.Characteristics, displayCharacteristic)
        if (value) characteristics.push(value)
      })

      const filters = {
        startDate: this.$route.query.après || null,
        endDate: this.$route.query.avant || null,
        characteristics,
        family: this.getChoiceValueFromText(Constants.ProductFamilies, this.$route.query.famille),
        canteen: Number(this.$route.query.cantine) || null,
      }
      const filterChanges = this.appliedFilters ? getObjectDiff(this.appliedFilters, filters) : filters
      if (Object.keys(filterChanges).length > 0) this.$set(this, "appliedFilters", filters)
    },
    clearSearch() {
      this.searchTerm = ""
      this.search()
    },
    search() {
      if (this.searchTerm && this.options.page !== 1) this.options.page = 1
      else this.$router.push({ query: this.getUrlQueryParams() }).catch(() => {})
    },
    clearFilters() {
      this.$set(this, "appliedFilters", {
        startDate: null,
        endDate: null,
        characteristics: [],
        family: null,
        canteen: null,
      })
    },
    onAppliedFiltersChange() {
      if (this.options.page !== 1) {
        this.options.page = 1
      } else {
        this.$router.push({ query: this.getUrlQueryParams() }).catch(() => {})
      }
    },
    onOptionsChange() {
      this.$router.push({ query: this.getUrlQueryParams() }).catch(() => {})
    },
    onRouteChange() {
      this.populateParametersFromRoute()
      this.fetchCurrentPage()
    },
    addWatchers() {
      this.$watch("appliedFilters", this.onAppliedFiltersChange, { deep: true })
      this.$watch("options", this.onOptionsChange, { deep: true })
      this.$watch("$route", this.onRouteChange)
    },
    capitalise: capitalise,
    duplicate(purchase) {
      this.$router.push({ name: "PurchasePage", params: { id: purchase.id }, query: { dupliquer: true } })
    },
    duplicatePurchaseInstruction(purchase) {
      const readableDate = purchase.date.toLocaleString("fr-FR", {
        month: "long",
        day: "numeric",
        year: "numeric",
      })
      return `Dupliquer l'achat « ${purchase.description || "sans description"} » du ${readableDate}`
    },
  },
  beforeMount() {
    if (!this.$route.query["page"]) this.$router.replace({ query: { page: 1 } })
  },
  mounted() {
    this.populateParametersFromRoute()
    if (this.hasActiveFilter) this.showFilters = true
    return this.fetchCurrentPage().then(this.addWatchers)
  },
}
</script>

<style scoped>
.v-data-table >>> tbody tr:not(.v-data-table__empty-wrapper),
.v-data-table >>> .v-chip {
  cursor: pointer;
}

/* Hides rows-per-page */
.v-data-table >>> .v-data-footer__select {
  visibility: hidden;
}
.active-filter-label {
  font-weight: bold;
}
.active-filter-label::before {
  content: "⚫︎";
  color: #ce614a;
}
</style>
