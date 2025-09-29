<template>
  <div>
    <div v-if="loading" class="pa-10 align-center d-flex flex-column">
      <p>
        Merci de patienter, nous compilons les actions concernant vos cantines. Ceci peut prendre quelques secondes.
      </p>
      <v-progress-circular indeterminate></v-progress-circular>
    </div>
    <div v-else>
      <v-row>
        <v-col v-if="showMassDiagnose || diagLoading" cols="12" sm="6" md="4">
          <v-card outlined>
            <v-card-text v-if="diagLoading" class="green--text">
              <v-col cols="1" justify-self="center">
                <v-progress-circular indeterminate></v-progress-circular>
              </v-col>
              <v-col>
                <p>Création de diagnostics en cours...</p>
              </v-col>
            </v-card-text>
            <div v-else-if="showMassDiagnose">
              <v-card-text>
                <p class="mb-0">
                  Vous pouvez créer
                  <span v-if="toDiagnose.length > 1">{{ toDiagnose.length }} diagnostics</span>
                  <span v-else>1 diagnostic</span>
                  depuis les achats renseignés.
                </p>
              </v-card-text>
              <v-card-actions class="pb-4">
                <v-btn class="primary ml-2" @click="massDiagnose">
                  <span v-if="toDiagnose.length > 1">Créer {{ toDiagnose.length }} diagnostics</span>
                  <span v-else>Créer le bilan</span>
                </v-btn>
              </v-card-actions>
            </div>
            <v-alert v-if="diagSuccesses.length" outlined type="success">
              <p v-if="diagSuccesses.length" class="mb-0">
                {{ diagSuccesses.length }} {{ diagSuccesses.length > 1 ? "diagnostics créés" : "diagnostic créé" }}
              </p>
            </v-alert>
          </v-card>
        </v-col>
        <v-col v-if="suggestTeledeclare()" cols="12" sm="6" md="4">
          <v-card outlined v-if="toTeledeclare.length > 1">
            <v-card-text>
              <p class="mb-0">
                Vous pouvez dès à présent effectuer la télédéclaration pour
                <span v-if="toTeledeclare.length > 1">{{ toTeledeclareCount }} cantines.</span>
                <span v-else>une cantine.</span>
              </p>
            </v-card-text>
            <v-card-actions class="pb-4">
              <v-btn class="primary ml-2" @click="showMultipleTeledeclarationPreview = true">
                <span v-if="toTeledeclare.length > 1">
                  Télédeclarer
                  <span v-if="toTeledeclareCount > toTeledeclare.length">
                    les {{ toTeledeclare.length }} premières cantines
                  </span>
                  <span v-else>{{ toTeledeclare.length }} cantines</span>
                </span>
                <span v-else>Télédeclarer la cantine</span>
              </v-btn>
            </v-card-actions>
          </v-card>
          <v-alert v-if="tdSuccesses.length" outlined type="success">
            <p v-if="tdSuccesses.length" class="mb-0">
              {{ tdSuccesses.length }} {{ tdSuccesses.length > 1 ? "cantines télédéclarées" : "cantine télédéclarée" }}
            </p>
          </v-alert>
          <v-alert v-if="tdFailures.length" outlined type="error">
            <p>
              {{ tdFailures.length }}
              {{ tdFailures.length > 1 ? "cantines pas télédéclarées" : "cantine pas télédéclarée" }}
            </p>
            <p>Essayez de télédéclarer les cantines restantes une par une depuis le tableur en dessous.</p>
            <p class="mb-0">Si le problème persiste, contactez-nous.</p>
          </v-alert>
        </v-col>
      </v-row>
      <TeledeclarationPreview
        v-if="toTeledeclare.length"
        :diagnostics="toTeledeclare"
        v-model="showMultipleTeledeclarationPreview"
        @teledeclare="submitTeledeclaration"
        :tdLoading="tdLoading"
        :idx="tdIdx"
      />
      <div class="mt-4">
        <v-data-table
          v-if="visibleCanteens"
          :options.sync="options"
          :server-items-length="canteenCount || 0"
          :items="visibleCanteens"
          :headers="headers"
          dense
          :items-per-page="limit"
          disable-sort
          :page="page"
          :footer-props="{
            disableItemsPerPage: true,
          }"
        >
          <template v-slot:[`item.name`]="{ item }">
            <router-link :to="toCanteen(item)">{{ item.name }}</router-link>
          </template>
          <template v-slot:[`item.siret`]="{ item }">
            <span v-if="item.sirenUniteLegale">SIREN : {{ item.sirenUniteLegale }}</span>
            <span v-else>SIRET : {{ item.siret }}</span>
          </template>
          <template v-slot:[`item.productionType`]="{ item }">
            {{ typeDisplay[item.productionType] }}
          </template>
          <template v-slot:[`item.badge`]="{ item }">
            <DataInfoBadge :canteen-action="item.action" />
          </template>
          <template v-slot:[`item.action`]="{ item }">
            <v-fade-transition>
              <div :key="`${item.id}_${item.action}`">
                <div v-if="getActionDisplay(item.action) === 'edit'">
                  <v-icon small class="mr-2" color="primary">{{ getActionIcon(item.action) }}</v-icon>
                  <span class="caption">
                    {{ getActionText(item.action) }}
                    <router-link :to="toTeledeclaration(item)">en cliquant ici</router-link>
                  </span>
                </div>
                <div v-if="getActionDisplay(item.action) === 'text'">
                  <v-icon v-if="getActionIcon(item.action)" small class="mr-2" color="green">
                    {{ getActionIcon(item.action) }}
                  </v-icon>
                  <span class="caption">{{ getActionText(item.action) }}</span>
                </div>
                <v-btn
                  v-if="getActionDisplay(item.action) === 'button'"
                  small
                  outlined
                  color="primary"
                  :to="actionLink(item)"
                  @click="action(item)"
                >
                  <v-icon small class="mr-2" color="primary">
                    {{ getActionIcon(item.action) }}
                  </v-icon>
                  {{ getActionText(item.action) }}
                  <span class="d-sr-only">{{ item.userCanView ? "" : "de" }} {{ item.name }}</span>
                </v-btn>
              </div>
            </v-fade-transition>
          </template>
        </v-data-table>
      </div>
      <TeledeclarationPreview
        v-if="canteenForTD"
        :diagnostic="diagnosticForTD"
        v-model="showTeledeclarationPreview"
        @teledeclare="submitTeledeclaration"
        :canteen="canteenForTD"
        :tdLoading="tdLoading"
      />
    </div>
  </div>
</template>

<script>
import TeledeclarationPreview from "@/components/TeledeclarationPreview"
import DataInfoBadge from "@/components/DataInfoBadge"
import { lastYear, actionIsTeledeclare } from "@/utils"

export default {
  name: "AnnualActionableCanteensTable",
  components: { TeledeclarationPreview, DataInfoBadge },
  data() {
    const year = lastYear()
    return {
      loading: false,
      limit: 15,
      page: null,
      canteenCount: null,
      visibleCanteens: null,
      searchTerm: null,
      year,
      options: {
        sortBy: [],
        sortDesc: [],
      },
      headers: [
        { text: "Nom", value: "name" },
        { text: "Siret ou Siren", value: "siret" },
        { text: "Type", value: "productionType" },
        { text: "Statut", value: "badge" },
        { text: "Action", value: "action" },
      ],
      typeDisplay: {
        site: "Cuisine sur site",
        site_cooked_elsewhere: "Cantine satellite",
        central: "Livreur des repas",
        central_serving: "Livreur, avec service sur place",
      },
      canteenForTD: null,
      showTeledeclarationPreview: false,
      showMultipleTeledeclarationPreview: false,
      toDiagnose: [],
      diagLoading: false,
      diagSuccesses: [],
      toTeledeclare: [],
      tdIdx: 0,
      toTeledeclareCount: null,
      tdSuccesses: [],
      tdFailures: [],
      tdLoading: false,
      campaignDates: null,
    }
  },
  computed: {
    actions() {
      return {
        "10_add_satellites": {
          text: "Ajouter des satellites",
          icon: "$community-fill",
          display: "button",
        },
        "18_prefill_diagnostic": {
          text: "Créer le bilan " + this.year,
          icon: "$add-circle-fill",
          display: "button",
        },
        "20_create_diagnostic": {
          text: "Créer le bilan " + this.year,
          icon: "$add-circle-fill",
          display: "button",
        },
        "30_fill_diagnostic": {
          text: "Compléter le bilan " + this.year,
          icon: "$edit-box-fill",
          display: "button",
        },
        "35_fill_canteen_data": {
          text: "Compléter les infos de la cantine",
          icon: "$building-fill",
          display: "button",
        },
        "40_teledeclare": {
          text: "Télédéclarer",
          icon: "$send-plane-fill",
          display: "button",
        },
        "45_did_not_teledeclare": {
          display: "empty",
        },
        "90_nothing_satellite": {
          display: "empty",
        },
        "91_nothing_satellite_teledeclared": {
          text: "Votre livreur des repas a déclaré le bilan pour votre établissement",
          display: "text",
        },
        "95_nothing": {
          icon: "$edit-fill",
          text: `En cas d'erreur, vous pouvez modifier vos données jusqu’au ${this.lastDayToEdit} (heure de Paris)`,
          display: this.canEditTd ? "edit" : "empty",
        },
      }
    },
    lastDayToEdit() {
      if (!this.canEditTd) return null
      const date = this.campaignDates.inTeledeclaration
        ? this.campaignDates.teledeclarationEndDate
        : this.campaignDates.correctionEndDate
      const prettyDate = new Date(date).toLocaleDateString("fr-FR", {
        month: "long",
        day: "numeric",
        year: "numeric",
      })
      return prettyDate
    },
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
    diagnosticForTD() {
      if (this.canteenForTD) {
        return this.getDiagnostic(this.canteenForTD)
      } else {
        return null
      }
    },
    // if there are multiple pages, show the mass action buttons for convenience, otherwise
    // only show when there is more than 1 of that action to carry out
    showMassTD() {
      return this.toTeledeclare?.length && (this.showPagination || this.toTeledeclare > 1)
    },
    showMassDiagnose() {
      return this.toDiagnose?.length && (this.showPagination || this.toDiagnose > 1)
    },
  },
  methods: {
    populateInitialParameters() {
      this.page = this.$route.query.cantinePage ? parseInt(this.$route.query.cantinePage) : 1
    },
    fetchCampaignDates() {
      fetch(`/api/v1/campaignDates/${this.year}`)
        .then((response) => response.json())
        .then((response) => {
          this.campaignDates = response
          this.canEditTd = this.campaignDates.inCorrection || this.campaignDates.inTeledeclaration
        })
    },
    fetchCurrentPage() {
      let queryParam = `ordering=action&limit=${this.limit}&offset=${this.offset}`
      if (this.searchTerm) queryParam += `&search=${this.searchTerm}`
      this.searchTerm = this.$route.query.recherche || null
      this.loading = true

      return fetch(`/api/v1/actionableCanteens/${this.year}?${queryParam}`)
        .then((response) => {
          if (response.status < 200 || response.status >= 400) throw new Error(`Error encountered : ${response}`)
          return response.json()
        })
        .then((response) => {
          this.canteenCount = response.count
          this.visibleCanteens = response.results
          this.toDiagnose = response.undiagnosedCanteensWithPurchases
          this.$emit("canteen-count", this.canteenCount)
        })
        .catch((e) => {
          this.$store.dispatch("notifyServerError", e)
        })
        .finally(() => {
          this.loading = false
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
    toCanteen(canteen) {
      return {
        name: "DashboardManager",
        params: { canteenUrlComponent: this.$store.getters.getCanteenUrlComponent(canteen) },
      }
    },
    toTeledeclaration(canteen) {
      return {
        name: "MyProgress",
        params: {
          canteenUrlComponent: this.$store.getters.getCanteenUrlComponent(canteen),
          year: this.year,
        },
      }
    },
    getActionText(action) {
      return this.actions[action] && this.actions[action].text
    },
    getActionIcon(action) {
      return this.actions[action] && this.actions[action].icon
    },
    getActionDisplay(action) {
      return this.actions[action] && this.actions[action].display
    },
    actionLink(canteen) {
      if (canteen.action === "10_add_satellites") {
        return {
          name: "GestionnaireCantineSatellitesGerer",
          params: { canteenUrlComponent: this.$store.getters.getCanteenUrlComponent(canteen) },
        }
      } else if (canteen.action === "20_create_diagnostic" || canteen.action === "18_prefill_diagnostic") {
        return {
          name: "MyProgress",
          params: {
            canteenUrlComponent: this.$store.getters.getCanteenUrlComponent(canteen),
            year: this.year,
            measure: "qualite-des-produits",
          },
        }
      } else if (canteen.action === "30_fill_diagnostic") {
        return {
          name: "MyProgress",
          params: {
            canteenUrlComponent: this.$store.getters.getCanteenUrlComponent(canteen),
            year: this.year,
            measure: "qualite-des-produits",
          },
        }
      } else if (canteen.action === "35_fill_canteen_data") {
        return {
          name: "CanteenForm",
          params: { canteenUrlComponent: this.$store.getters.getCanteenUrlComponent(canteen) },
        }
      }
    },
    action(canteen) {
      if (actionIsTeledeclare(canteen.action)) {
        this.canteenForTD = canteen
        this.showTeledeclarationPreview = true
      }
    },
    addWatchers() {
      this.$watch("options", this.onOptionsChange, { deep: true })
      this.$watch("$route", this.onRouteChange)
      this.$watch("showMultipleTeledeclarationPreview", (open) => (open ? null : this.fetchDiagnosticsToTeledeclare()))
    },
    onOptionsChange() {
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
    getDiagnostic(canteen) {
      if (canteen.diagnostics?.length) {
        return canteen.diagnostics.find((d) => d.year === this.year)
      }
    },
    submitTeledeclaration(diagnostic, persist) {
      this.tdLoading = true
      diagnostic = diagnostic || this.diagnosticForTD
      this.$store
        .dispatch("submitTeledeclaration", { id: diagnostic.id })
        .then(() => {
          this.$store.dispatch("notify", {
            title: "Télédéclaration prise en compte",
            status: "success",
          })
        })
        .then(() => {
          if (this.tdIdx + 1 >= this.toTeledeclare.length) {
            this.fetchDiagnosticsToTeledeclare()
          } else {
            this.tdIdx++
          }
        })
        .then(() => {
          this.updateCanteen(diagnostic.canteen?.id || this.canteenForTD?.id)
        })
        .catch((e) => {
          this.$store.dispatch("notifyServerError", e)
        })
        .finally(() => {
          this.showTeledeclarationPreview = persist
          this.canteenForTD = null
          this.tdLoading = false
        })
    },
    updateCanteen(canteenId) {
      fetch(`/api/v1/actionableCanteens/${canteenId}/${this.year}`)
        .then((response) => {
          if (response.status < 200 || response.status >= 400) throw new Error(`Error encountered : ${response}`)
          return response.json()
        })
        .then((canteen) => {
          const canteenIdx = this.visibleCanteens.findIndex((c) => c.id === canteenId)
          this.visibleCanteens.splice(canteenIdx, 1, canteen)
        })
    },
    massDiagnose() {
      this.diagLoading = true
      this.$store
        .dispatch("createAndPrefillDiagnostics", { year: this.year, ids: this.toDiagnose })
        .then((response) => {
          this.diagSuccesses = response.results
          const title =
            this.diagSuccesses.length > 1
              ? `${this.diagSuccesses.length} diagnostics créés`
              : `${this.diagSuccesses.length} diagnostic créé`
          this.$store.dispatch("notify", {
            title,
            status: "success",
          })
        })
        .catch((e) => this.$store.dispatch("notifyServerError", e))
        // refresh actions
        .then(() => this.fetchCurrentPage())
        .finally(() => {
          this.diagLoading = false
        })
    },
    fetchDiagnosticsToTeledeclare() {
      this.loading = true
      return fetch(`/api/v1/diagnosticsToTeledeclare/${this.year}`)
        .then((response) => {
          if (response.status < 200 || response.status >= 400) throw new Error(`Error encountered : ${response}`)
          return response.json()
        })
        .then((response) => {
          this.toTeledeclare = response.results
          this.toTeledeclareCount = response.count
          this.tdIdx = 0
        })
        .catch((e) => {
          this.toTeledeclare = []
          this.$store.dispatch("notifyServerError", e)
        })
        .finally(() => (this.loading = false))
    },
    suggestTeledeclare() {
      if (
        (this.toTeledeclare.length > 1 || this.tdSuccesses.length || this.tdFailures.length) &&
        window.ENABLE_TELEDECLARATION
      )
        return true
    },
  },
  mounted() {
    this.clearSearch()
    this.populateInitialParameters()
    this.fetchCampaignDates()
    return this.fetchDiagnosticsToTeledeclare()
      .then(this.fetchCurrentPage)
      .then(this.addWatchers)
  },
}
</script>

<style scoped>
/* Hides rows-per-page */
.v-data-table >>> .v-data-footer__select {
  visibility: hidden;
}
</style>
