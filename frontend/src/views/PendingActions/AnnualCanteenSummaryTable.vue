<template>
  <div>
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
          <div v-if="item.action === 'NOTHING'" class="px-3">
            <v-icon small class="mr-2" color="green">$checkbox-circle-fill</v-icon>
            <span class="caption">Rien à faire !</span>
          </div>
          <v-btn small outlined color="primary" :to="actionLink(item)" @click="action(item)" v-else>
            <v-icon small class="mr-2" color="primary">{{ actions[item.action].icon }}</v-icon>
            {{ actions[item.action].display }}
            <span class="d-sr-only">{{ item.userCanView ? "" : "de" }} {{ item.name }}</span>
          </v-btn>
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
</template>

<script>
import TeledeclarationPreview from "@/components/TeledeclarationPreview"
import DsfrTextarea from "@/components/DsfrTextarea"

export default {
  name: "AnnualCanteenSummaryTable",
  components: { TeledeclarationPreview, DsfrTextarea },
  data() {
    const year = 2021
    return {
      limit: 15,
      page: null,
      canteenCount: null,
      visibleCanteens: null,
      searchTerm: null,
      inProgress: false,
      year,
      unteledeclaredCount: 7,
      options: {
        sortBy: [],
        sortDesc: [],
        page: 1,
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
        CREATE: {
          display: "Créer le diagnostic " + year,
          icon: "$add-circle-fill",
        },
        COMPLETE: {
          display: "Completer le diagnostic " + year,
          icon: "$edit-box-fill",
        },
        TELEDECLARE: {
          display: "Télédéclarer",
          icon: "$send-plane-fill",
        },
        PUBLISH: {
          display: "Publier",
          icon: "mdi-bullhorn",
        },
        NOTHING: {
          display: "Rien à faire !",
          icon: "$checkbox-circle-fill",
        },
      },
      canteenForTD: null,
      showTeledeclarationPreview: false,
      showPublicationForm: false,
      canteenForPublication: null,
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
  },
  methods: {
    populateInitialParameters() {
      this.page = this.$route.query.cantinePage ? parseInt(this.$route.query.cantinePage) : 1
    },
    fetchCurrentPage() {
      let queryParam = `limit=${this.limit}&offset=${this.offset}`
      if (this.searchTerm) queryParam += `&search=${this.searchTerm}`
      this.searchTerm = this.$route.query.recherche || null
      this.inProgress = true

      return fetch(`/api/v1/canteens/?${queryParam}`)
        .then((response) => {
          if (response.status < 200 || response.status >= 400) throw new Error(`Error encountered : ${response}`)
          return response.json()
        })
        .then((response) => {
          this.canteenCount = response.count
          this.visibleCanteens = response.results
          this.visibleCanteens.forEach((canteen) => {
            canteen.action = this.determineAction(canteen)
          })
          this.$emit("canteen-count", this.canteenCount)
        })
        .catch((e) => {
          this.publishedCanteenCount = 0
          this.$store.dispatch("notifyServerError", e)
        })
        .finally(() => {
          this.inProgress = false
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
      if (canteen.action !== "TELEDECLARE" && canteen.action !== "PUBLISH") {
        return {
          name: "CanteenModification",
          params: { canteenUrlComponent: this.$store.getters.getCanteenUrlComponent(canteen) },
        }
      }
    },
    action(canteen) {
      if (canteen.action === "TELEDECLARE") {
        this.canteenForTD = canteen
        this.showTeledeclarationPreview = true
      } else if (canteen.action === "PUBLISH") {
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
          this.updateCanteen(canteen)
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
      // this.$watch("appliedFilters", this.onAppliedFiltersChange, { deep: true })
      this.$watch("options", this.onOptionsChange, { deep: true })
      this.$watch("$route", this.onRouteChange)
    },
    onOptionsChange() {
      // this.$router.push({ query: this.getUrlQueryParams() }).catch(() => {})
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
        .then((diagnostic) => {
          this.$store.dispatch("notify", {
            title: "Télédéclaration prise en compte",
            status: "success",
          })
          this.updateCanteen(this.canteenForTD, diagnostic)
        })
        .catch((e) => this.$store.dispatch("notifyServerError", e))
        .finally(() => {
          this.showTeledeclarationPreview = false
          this.canteenForTD = null
        })
    },
    updateCanteen(canteen, diagnostic) {
      const canteenIdx = this.visibleCanteens.findIndex((c) => c.id === canteen.id)
      this.visibleCanteens[canteenIdx] = canteen
      if (diagnostic) {
        const diagnosticIdx = this.visibleCanteens[canteenIdx].diagnostics.findIndex((d) => d.id === diagnostic.id)
        this.visibleCanteens[canteenIdx].diagnostics[diagnosticIdx] = diagnostic
      }
      this.visibleCanteens[canteenIdx].action = this.determineAction(this.visibleCanteens[canteenIdx])
      console.log(this.visibleCanteens[canteenIdx].action)
    },
    determineAction(canteen) {
      if (!canteen.diagnostics || canteen.diagnostics.length === 0) {
        return "CREATE"
      } else {
        const thisYearDiag = canteen.diagnostics.find((d) => d.year === this.year)
        if (!thisYearDiag) {
          return "CREATE"
        } else if (thisYearDiag.teledeclaration && thisYearDiag.teledeclaration.status === "SUBMITTED") {
          if (canteen.publicationStatus === "published") {
            return "NOTHING"
          } else {
            return "PUBLISH"
          }
        } else if (thisYearDiag.valueTotalHt) {
          return "TELEDECLARE"
        } else {
          return "COMPLETE"
        }
      }
    },
  },
  mounted() {
    this.populateInitialParameters()
    return this.fetchCurrentPage().then(this.addWatchers)
  },
}
</script>
