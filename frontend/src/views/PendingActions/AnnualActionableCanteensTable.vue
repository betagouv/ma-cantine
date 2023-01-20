<template>
  <div>
    <div v-if="loading" class="pa-10 text-center">
      <v-progress-circular indeterminate></v-progress-circular>
    </div>
    <div v-else>
      <div>
        <v-row v-if="tdLoading" class="green--text">
          <v-col cols="1" justify-self="center">
            <v-progress-circular indeterminate></v-progress-circular>
          </v-col>
          <v-col>
            <p>Télédéclarations en cours...</p>
          </v-col>
        </v-row>
        <p v-else-if="toTeledeclare.length > 1">
          Vous pouvez télédéclarer
          <span v-if="toTeledeclare.length > 1">{{ toTeledeclare.length }} cantines.</span>
          <span v-else>1 cantine.</span>
          <v-btn class="primary ml-2" @click="massTeledeclaration">
            <span v-if="toTeledeclare.length > 1">Télédeclarer {{ toTeledeclare.length }} cantines</span>
            <span v-else>Télédeclarer la cantine</span>
          </v-btn>
        </p>
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
      </div>
      <div>
        <v-row v-if="pubLoading" class="green--text">
          <v-col cols="1" justify-self="center">
            <v-progress-circular indeterminate></v-progress-circular>
          </v-col>
          <v-col>
            <p>Publications en cours...</p>
          </v-col>
        </v-row>
        <p v-else-if="showMassPublication">
          Vous pouvez publier
          <span v-if="toPublish.length > 1">{{ toPublish.length }} cantines.</span>
          <span v-else>1 cantine.</span>
          <v-btn class="primary ml-2" @click="massPublication">
            <span v-if="toPublish.length > 1">Publier {{ toPublish.length }} cantines</span>
            <span v-else>Publier la cantine</span>
          </v-btn>
        </p>
        <v-alert v-if="pubSuccesses.length" outlined type="success">
          <p v-if="pubSuccesses.length" class="mb-0">
            {{ pubSuccesses.length }} {{ pubSuccesses.length > 1 ? "cantines publiées" : "cantine publiée" }}
          </p>
        </v-alert>
      </div>
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
        @teledeclare="submitTeledeclaration(diagnosticForTD)"
        :canteen="canteenForTD"
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
        "20_create_diagnostic": {
          display: "Créer le diagnostic " + year,
          icon: "$add-circle-fill",
        },
        "30_complete_diagnostic": {
          display: "Completer le diagnostic " + year,
          icon: "$edit-box-fill",
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
      showPublicationForm: false,
      canteenForPublication: null,
      toTeledeclare: [],
      tdLoading: false,
      tdSuccesses: [],
      tdFailures: [],
      toPublish: [],
      pubLoading: false,
      pubSuccesses: [],
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
          this.toTeledeclare = response.diagnosticsToTeledeclare
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
      } else if (canteen.action === "20_create_diagnostic") {
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
    submitTeledeclaration(diagnostic) {
      this.$store
        .dispatch("submitTeledeclaration", { id: diagnostic.id, canteenId: this.canteenForTD.id })
        .then(() => {
          this.$store.dispatch("notify", {
            title: "Télédéclaration prise en compte",
            status: "success",
          })
          this.updateCanteen(this.canteenForTD.id)
        })
        .catch((e) => {
          this.$store.dispatch("notifyServerError", e)
        })
        .finally(() => {
          this.showTeledeclarationPreview = false
          this.canteenForTD = null
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
    massTeledeclaration() {
      this.tdLoading = true
      this.$store
        .dispatch("submitMultipleTeledeclarations", { ids: this.toTeledeclare })
        .then((response) => {
          const errors = response.errors
          this.tdSuccesses = response.teledeclarationIds
          this.tdFailures = Object.keys(errors)
          if (this.tdFailures.length === 0) {
            const title =
              this.tdSuccesses.length > 1
                ? `${this.tdSuccesses.length} diagnostics télédéclarés`
                : `${this.tdSuccesses.length} diagnostic télédéclaré`
            this.$store.dispatch("notify", {
              title,
              status: "success",
            })
          } else {
            const title =
              this.tdFailures.length > 1
                ? `${this.tdFailures.length} diagnostics pas télédéclarés`
                : `${this.tdFailures.length} diagnostic pas télédéclaré`
            this.$store.dispatch("notify", {
              title,
              status: "error",
            })
          }
        })
        .catch((e) => this.$store.dispatch("notifyServerError", e))
        // refresh actions
        .then(() => this.fetchCurrentPage())
        .finally(() => {
          this.tdLoading = false
        })
    },
    massPublication() {
      this.pubLoading = true
      this.$store
        .dispatch("submitMultiplePublications", { ids: this.toPublish })
        .then((response) => {
          this.pubSuccesses = response.ids
          const title =
            this.pubSuccesses.length > 1
              ? `${this.pubSuccesses.length} cantines publiées`
              : `${this.pubSuccesses.length} cantine publiée`
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
  },
  mounted() {
    this.populateInitialParameters()
    return this.fetchCurrentPage().then(this.addWatchers)
  },
}
</script>
