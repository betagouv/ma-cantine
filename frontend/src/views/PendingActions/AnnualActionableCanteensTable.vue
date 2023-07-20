<template>
  <div>
    <div v-if="loading" class="pa-10 text-center">
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
                Vous pouvez créer
                <span v-if="toDiagnose.length > 1">{{ toDiagnose.length }} diagnostics</span>
                <span v-else>1 diagnostic</span>
                depuis les achats renseignés.
              </v-card-text>
              <v-card-actions class="pb-4">
                <v-btn class="primary ml-2" @click="massDiagnose">
                  <span v-if="toDiagnose.length > 1">Créer {{ toDiagnose.length }} diagnostics</span>
                  <span v-else>Créer le diagnostic</span>
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
        <v-col
          v-if="(toTeledeclare.length > 1 || tdSuccesses.length || tdFailures.length) && shouldTeledeclare()"
          cols="12"
          sm="6"
          md="4"
        >
          <v-card outlined v-if="toTeledeclare.length > 1">
            <v-card-text>
              Vous pouvez dès à présent effectuer la télédéclaration pour
              <span v-if="toTeledeclare.length > 1">{{ toTeledeclareCount }} cantines.</span>
              <span v-else>une cantine.</span>
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
        <v-col v-if="pubLoading || showMassPublication" cols="12" sm="6" md="4">
          <v-card outlined>
            <v-row v-if="pubLoading" class="green--text">
              <v-col cols="1" justify-self="center">
                <v-progress-circular indeterminate></v-progress-circular>
              </v-col>
              <v-col>
                <p>Publications en cours...</p>
              </v-col>
            </v-row>
            <div v-else-if="showMassPublication">
              <v-card-text>
                Vous pouvez publier
                <span v-if="toPublish.length > 1">{{ toPublish.length }} cantines.</span>
                <span v-else>1 cantine.</span>
              </v-card-text>
              <v-card-actions class="pb-4">
                <v-btn class="primary ml-2" @click="massPublication">
                  <span v-if="toPublish.length > 1">Publier {{ toPublish.length }} cantines</span>
                  <span v-else>Publier la cantine</span>
                </v-btn>
              </v-card-actions>
            </div>
          </v-card>
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
          <template v-slot:[`item.productionType`]="{ item }">
            {{ typeDisplay[item.productionType] }}
          </template>
          <template v-slot:[`item.action`]="{ item }">
            <v-fade-transition>
              <div :key="`${item.id}_${item.action}`">
                <div v-if="item.action === '95_nothing'" class="px-3">
                  <v-icon small class="mr-2" color="green">$checkbox-circle-fill</v-icon>
                  <span class="caption">Rien à faire !</span>
                </div>
                <v-btn small outlined color="primary" :to="actionLink(item)" @click="action(item)" v-else>
                  <v-icon small class="mr-2" color="primary">
                    {{ actions[item.action] && actions[item.action].icon }}
                  </v-icon>
                  {{ actions[item.action] && actions[item.action].display }}
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
      <v-dialog v-model="showPublicationForm" max-width="750" v-if="canteenForPublication">
        <v-card class="text-left">
          <v-card-title class="font-weight-bold">Publication : {{ canteenForPublication.name }}</v-card-title>
          <v-card-text class="mt-2">
            <p>
              Les publications sont affichées dans
              <router-link :to="{ name: 'CanteensHome' }" target="_blank">nos cantines</router-link>
              pour informer les convives.
            </p>
            <v-form>
              <label class="body-2" for="general">
                Décrivez si vous le souhaitez le fonctionnement, l'organisation, l'historique de votre établissement...
              </label>
              <DsfrTextarea
                id="general"
                class="my-2"
                rows="3"
                counter="500"
                v-model="canteenForPublication.publicationComments"
                hint="Vous pouvez par exemple raconter l'histoire du lieu, du bâtiment, de l'association ou de l'entreprise ou des personnes qui gérent cet établissement, ses spécificités, ses caractéristiques techniques, logistiques... Cela peut aussi être une anecdote dont vous êtes fiers, une certification, un label..."
              />
            </v-form>
          </v-card-text>
          <v-card-actions class="d-flex pr-6 pb-4">
            <v-spacer></v-spacer>
            <v-btn color="primary" outlined class="px-4 mr-2" @click="closePublication">Annuler</v-btn>
            <v-btn color="primary" class="px-4" @click="publish">Publier</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </div>
  </div>
</template>

<script>
import TeledeclarationPreview from "@/components/TeledeclarationPreview"
import DsfrTextarea from "@/components/DsfrTextarea"
import { lastYear } from "@/utils"

export default {
  name: "AnnualActionableCanteensTable",
  components: { TeledeclarationPreview, DsfrTextarea },
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
        "10_add_satellites": {
          display: "Ajouter des satellites",
          icon: "$community-fill",
        },
        "18_prefill_diagnostic": {
          display: "Créer le diagnostic " + year,
          icon: "$add-circle-fill",
        },
        "20_create_diagnostic": {
          display: "Créer le diagnostic " + year,
          icon: "$add-circle-fill",
        },
        "30_complete_diagnostic": {
          display: "Compléter le diagnostic " + year,
          icon: "$edit-box-fill",
        },
        "35_fill_canteen_data": {
          display: "Compléter les infos de la cantine",
          icon: "$building-fill",
        },
        "40_teledeclare": {
          display: "Télédéclarer",
          icon: "$send-plane-fill",
        },
        "50_publish": {
          display: "Publier",
          icon: "mdi-bullhorn",
        },
        "95_nothing": {
          display: "Rien à faire !",
          icon: "$checkbox-circle-fill",
        },
      },
      canteenForTD: null,
      showTeledeclarationPreview: false,
      showMultipleTeledeclarationPreview: false,
      showPublicationForm: false,
      canteenForPublication: null,
      toDiagnose: [],
      diagLoading: false,
      diagSuccesses: [],
      toTeledeclare: [],
      tdIdx: 0,
      toTeledeclareCount: null,
      tdSuccesses: [],
      tdFailures: [],
      toPublish: [],
      pubLoading: false,
      tdLoading: false,
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
    showMassPublication() {
      return this.toPublish?.length && (this.showPagination || this.toPublish > 1)
    },
    showMassDiagnose() {
      return this.toDiagnose?.length && (this.showPagination || this.toDiagnose > 1)
    },
  },
  methods: {
    populateInitialParameters() {
      this.page = this.$route.query.cantinePage ? parseInt(this.$route.query.cantinePage) : 1
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
          this.toPublish = response.canteensToPublish
          this.$emit("canteen-count", this.canteenCount)
        })
        .catch((e) => {
          this.publishedCanteenCount = 0
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
        name: "CanteenModification",
        params: { canteenUrlComponent: this.$store.getters.getCanteenUrlComponent(canteen) },
      }
    },
    actionLink(canteen) {
      if (canteen.action === "10_add_satellites") {
        return {
          name: "SatelliteManagement",
          params: { canteenUrlComponent: this.$store.getters.getCanteenUrlComponent(canteen) },
        }
      } else if (canteen.action === "20_create_diagnostic" || canteen.action === "18_prefill_diagnostic") {
        return {
          name: "NewDiagnosticForCanteen",
          params: { canteenUrlComponent: this.$store.getters.getCanteenUrlComponent(canteen) },
          query: { année: this.year },
        }
      } else if (canteen.action === "30_complete_diagnostic") {
        return {
          name: "DiagnosticModification",
          params: { canteenUrlComponent: this.$store.getters.getCanteenUrlComponent(canteen), year: this.year },
        }
      } else if (canteen.action === "35_fill_canteen_data") {
        return {
          name: "CanteenForm",
          params: { canteenUrlComponent: this.$store.getters.getCanteenUrlComponent(canteen) },
        }
      }
    },
    action(canteen) {
      if (canteen.action === "40_teledeclare") {
        this.canteenForTD = canteen
        this.showTeledeclarationPreview = true
      } else if (canteen.action === "50_publish") {
        this.canteenForPublication = canteen
        this.showPublicationForm = true
      }
    },
    publish() {
      this.$store
        .dispatch("publishCanteen", {
          id: this.canteenForPublication.id,
          payload: this.canteenForPublication,
        })
        .then((canteen) => {
          this.$store.dispatch("notify", { title: "Votre cantine est publiée", status: "success" })
          this.updateCanteen(canteen.id)
        })
        .catch((e) => {
          this.$store.dispatch("notifyServerError", e)
        })
        .finally(() => {
          this.closePublication()
        })
    },
    closePublication() {
      this.canteenForPublication = null
      this.showPublicationForm = false
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
    massPublication() {
      this.pubLoading = true
      this.$store
        .dispatch("submitMultiplePublications", { ids: this.toPublish })
        .then((response) => {
          let pubSuccesses = response.ids
          const title =
            pubSuccesses.length > 1
              ? `${pubSuccesses.length} cantines publiées`
              : `${pubSuccesses.length} cantine publiée`
          this.$store.dispatch("notify", {
            title,
            status: "success",
          })
        })
        .catch((e) => this.$store.dispatch("notifyServerError", e))
        // refresh actions
        .then(() => this.fetchCurrentPage())
        .finally(() => {
          this.pubLoading = false
        })
    },
    fetchDiagnosticsToTeledeclare() {
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
    },
    shouldTeledeclare() {
      if (window.ENABLE_TELEDECLARATION) return true
      else return false
    },
  },
  mounted() {
    this.populateInitialParameters()
    return this.fetchDiagnosticsToTeledeclare()
      .then(this.fetchCurrentPage)
      .then(this.addWatchers)
  },
}
</script>
