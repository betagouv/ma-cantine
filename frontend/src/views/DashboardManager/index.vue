<template>
  <div class="text-left">
    <v-row v-if="showCanteenSelection" class="my-6">
      <v-col cols="12" sm="6">
        <label class="body-2 d-sr-only" for="canteen">Établissement</label>
        <DsfrAutocomplete
          hide-details="auto"
          :items="canteenPreviews"
          placeholder="Choisissez l'établissement"
          v-model="nextCanteenId"
          item-text="name"
          item-value="id"
          id="canteen"
          class="mt-2"
          auto-select-first
          no-data-text="Pas de résultats"
          @blur="showCanteenSelection = false"
        />
      </v-col>
    </v-row>
    <h1 class="my-4 fr-h2" v-else-if="canteen">{{ canteen.name }}</h1>
    <h1 class="my-4 fr-h2" v-else>Bienvenue {{ loggedUser.firstName }}</h1>
    <v-row v-if="!showCanteenSelection">
      <v-col>
        <v-btn @click="showCanteenSelection = true" outlined small color="primary" v-if="canteenPreviews.length > 1">
          <v-icon class="mr-1" small>mdi-pencil</v-icon>
          Changer d'établissement
        </v-btn>
      </v-col>
    </v-row>

    <div v-if="canteen">
      <div class="mt-4">
        <EgalimProgression :canteen="canteen" />
      </div>

      <div v-if="canteen">
        <h2 class="mt-10 mb-2 fr-h4">
          Mon établissement
        </h2>
        <p class="fr-text-sm">
          Accédez ci-dessous aux différents outils de gestion de votre établissement sur la plateforme « ma cantine ».
        </p>
        <v-row>
          <v-col cols="12" md="8" id="latest-purchases">
            <!-- How relevant are purchases to satellites? -->
            <v-card outlined class="fill-height d-flex flex-column pa-4">
              <v-card-title class="fr-h4">Mes achats</v-card-title>
              <v-spacer></v-spacer>
              <v-card-text>
                <v-data-table
                  :items="purchases"
                  :headers="purchaseHeaders"
                  :hide-default-header="true"
                  :hide-default-footer="true"
                  :disable-sort="true"
                >
                  <template v-slot:[`item.characteristics`]="{ item }">
                    {{ getProductCharacteristicsDisplayValue(item.characteristics) }}
                  </template>
                  <template v-slot:[`no-data`]>
                    <v-card outlined rounded class="mb-4 py-4" color="primary lighten-5" v-if="!purchasesFetchingError">
                      <v-card-text class="fr-text-xs">
                        Saisissez vos achats manuellement ou connectez votre logiciel de gestion habituel
                      </v-card-text>
                    </v-card>
                    <v-alert outlined type="error" v-else>
                      <p>{{ purchasesFetchingError }}</p>
                      <v-btn @click="fetchPurchases" outlined color="primary">Essayer à nouveau</v-btn>
                    </v-alert>
                  </template>
                </v-data-table>
              </v-card-text>
              <v-spacer></v-spacer>
              <v-card-actions class="justify-end" v-if="purchases.length || purchasesFetchingError">
                <v-btn :to="{ name: 'NewPurchase' }" outlined color="primary" class="mx-2 mb-2">
                  Ajouter un achat
                </v-btn>
                <v-btn :to="{ name: 'PurchasesImporter' }" outlined color="primary" class="mx-2 mb-2">
                  Importer des achats
                </v-btn>
                <v-btn :to="{ name: 'PurchasesHome' }" outlined color="primary" class="mx-2 mb-2">
                  Tous mes achats
                </v-btn>
              </v-card-actions>
              <v-card-actions class="justify-end" v-else>
                <v-btn :to="{ name: 'NewPurchase' }" outlined color="primary" class="mx-2 mb-2">
                  Ajouter mon premier achat
                </v-btn>
                <v-btn :to="{ name: 'PurchasesImporter' }" outlined color="primary" class="mx-2 mb-2">
                  Importer mes achats
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
          <v-col cols="6" md="4" id="canteen-info-card">
            <v-card outlined class="fill-height d-flex flex-column pa-4">
              <v-card-title class="fr-h4">Mon établissement</v-card-title>
              <v-card-text class="fr-text-xs">
                <p>SIRET : {{ canteen.siret }}</p>
                <div v-if="centralKitchen">
                  <p>
                    La cuisine qui fournit les repas :
                    <router-link
                      :to="{
                        name: 'CanteenModification',
                        params: { canteenUrlComponent: this.$store.getters.getCanteenUrlComponent(centralKitchen) },
                      }"
                      target="_blank"
                      v-if="centralKitchen.isManagedByUser"
                    >
                      « {{ centralKitchen.name }} »
                      <v-icon small color="primary">mdi-open-in-new</v-icon>
                    </router-link>
                    <span v-else>« {{ centralKitchen.name }} »</span>
                  </p>
                </div>
                <CanteenIndicators :canteen="canteen" />
              </v-card-text>
              <v-spacer></v-spacer>
              <v-card-actions class="mx-2 mb-2 justify-end">
                <v-btn
                  :to="{
                    name: 'CanteenForm',
                    params: { canteenUrlComponent: $store.getters.getCanteenUrlComponent(canteen) },
                  }"
                  color="primary"
                  outlined
                >
                  Modifier
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
          <v-col cols="4" id="managers">
            <v-card outlined class="fill-height d-flex flex-column pa-4">
              <v-card-title class="fr-h4">
                Mon équipe
              </v-card-title>
              <v-card-text>
                <div v-if="managers.length > 1">
                  <p class="fr-text">
                    {{ managers.length }} personnes (dont vous) peuvent actuellement modifier cet établissement et
                    ajouter des données
                  </p>
                  <ul class="pl-0 fr-text-xs">
                    <li v-for="(manager, idx) in managers" :key="manager.email">
                      <v-icon>
                        {{ manager.isInvite ? "mdi-account-clock-outline" : "mdi-account-check-outline" }}
                      </v-icon>
                      {{ manager.isInvite ? manager.email : `${manager.firstName} ${manager.lastName}` }}
                      <span v-if="idx === 0">(vous)</span>
                    </li>
                  </ul>
                </div>
                <p class="fr-text" v-else>
                  Actuellement, vous êtes la seule personne qui peut modifier cet établissement et ajouter des données
                </p>
              </v-card-text>
              <v-spacer></v-spacer>
              <v-card-actions class="justify-end">
                <v-btn
                  :to="{
                    name: 'CanteenManagers',
                    params: { canteenUrlComponent: this.$store.getters.getCanteenUrlComponent(canteen) },
                  }"
                  outlined
                  color="primary"
                  class="mx-2 mb-2"
                >
                  Gérer mon équipe
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </div>
    </div>
    <v-row v-else>
      <v-col cols="12" sm="6" md="4" height="100%" class="d-flex flex-column">
        <v-card
          class="d-flex flex-column align-center justify-center dsfr"
          outlined
          min-height="220"
          height="80%"
          :to="{ name: 'NewCanteen' }"
        >
          <v-icon size="100" class="primary--text">mdi-plus</v-icon>
          <v-card-text class="font-weight-bold pt-0 text-center primary--text text-body-1">
            Ajouter une cantine
          </v-card-text>
        </v-card>
        <v-spacer></v-spacer>
        <div class="d-flex mt-4 mb-2 align-center px-2">
          <v-divider></v-divider>
          <p class="mx-2 my-0 caption">ou</p>
          <v-divider></v-divider>
        </div>
        <v-spacer></v-spacer>
        <v-btn text color="primary" :to="{ name: 'DiagnosticsImporter' }">
          <v-icon class="mr-2">mdi-file-upload-outline</v-icon>
          Créer plusieurs cantines depuis un fichier
        </v-btn>
      </v-col>
    </v-row>

    <h2 class="mt-10 mb-2 text-h6 font-weight-bold">
      Mes ressources personalisées
    </h2>
    <p class="body-2">
      Découvrez ci-dessous des articles et des outils pratiques, ainsi que des suggestions de partenaires et des
      cantines inspirantes sur votre territoire qui correspondent à vos enjeux.
    </p>
  </div>
</template>

<script>
import EgalimProgression from "./EgalimProgression.vue"
import CanteenIndicators from "@/components/CanteenIndicators"
import DsfrAutocomplete from "@/components/DsfrAutocomplete"
import { toCurrency } from "@/utils"
import Constants from "@/constants"
import validators from "@/validators"

export default {
  name: "DashboardManager",
  components: { EgalimProgression, CanteenIndicators, DsfrAutocomplete },
  data() {
    // const canteenId = this.$store.state.userCanteenPreviews[0]?.id
    const canteenId = 6 // Site avec diag
    // const canteenId = 227 // Satellite sans diag
    return {
      canteenId,
      nextCanteenId: canteenId,
      canteen: null,
      centralKitchen: null,
      purchases: [],
      purchaseHeaders: [
        {
          text: "Date",
          align: "start",
          value: "relativeDate",
        },
        { text: "Produit", value: "description" },
        { text: "Caractéristiques", value: "characteristics" },
        { text: "Prix HT", value: "priceHt", align: "end" },
      ],
      purchasesFetchingError: null,
      showCanteenSelection: false,
      validators,
    }
  },
  computed: {
    loggedUser() {
      return this.$store.state.loggedUser
    },
    canteenPreviews() {
      return this.$store.state.userCanteenPreviews
    },
    managers() {
      if (!this.canteen) []
      const managersCopy = [...this.canteen.managers]
      const loggedUserIndex = managersCopy.findIndex((x) => x.email === this.$store.state.loggedUser.email)
      managersCopy.splice(0, 0, managersCopy.splice(loggedUserIndex, 1)[0])
      return managersCopy.concat(this.managerInvitations)
    },
    managerInvitations() {
      return (
        this.canteen?.managerInvitations.map((i) => {
          i.isInvite = true
          return i
        }) || []
      )
    },
  },
  methods: {
    fetchCanteenIfNeeded() {
      if (this.canteen || !this.canteenId) return
      const id = this.canteenId
      return this.$store
        .dispatch("fetchCanteen", { id })
        .then((canteen) => {
          this.canteen = canteen
          this.getCentralKitchen()
          this.fetchPurchases()
        })
        .catch(() => {
          this.$store.dispatch("notify", {
            message: "Nous n'avons pas trouvé cette cantine",
            status: "error",
          })
        })
    },
    getCentralKitchen() {
      this.centralKitchen = null
      if (
        this.canteen &&
        this.canteen.centralProducerSiret &&
        this.canteen.siret !== this.canteen.centralProducerSiret
      ) {
        fetch("/api/v1/canteenStatus/siret/" + this.canteen.centralProducerSiret)
          .then((response) => response.json())
          .then((response) => (this.centralKitchen = response))
      }
    },
    fetchPurchases() {
      this.purchasesFetchingError = null
      const purchaseLimit = 3
      const query = `limit=${purchaseLimit}&ordering=-date&canteen__id=${this.canteenId}`
      return fetch(`/api/v1/purchases/?${query}`)
        .then((response) => {
          if (response.status < 200 || response.status >= 400) throw new Error(`Error encountered : ${response}`)
          return response.json()
        })
        .then((response) => {
          this.purchases = response.results
          this.purchases.forEach((purchase) => {
            purchase.priceHt = toCurrency(purchase.priceHt)
            const dateDelta = Date.now() - new Date(purchase.date).getTime()
            const millisecondsInDay = 1000 * 60 * 60 * 24
            const daysAgo = Math.floor(dateDelta / millisecondsInDay)
            const weeksAgo = Math.floor(daysAgo / 7)
            const monthsAgo = Math.floor(daysAgo / 30)
            const yearsAgo = Math.floor(daysAgo / 365)
            if (yearsAgo > 0) {
              purchase.relativeDate = `il y a ${yearsAgo} an${yearsAgo === 1 ? "" : "s"}`
            } else if (monthsAgo > 0) {
              purchase.relativeDate = `il y a ${monthsAgo} mois`
            } else if (weeksAgo > 0) {
              purchase.relativeDate = `il y a ${weeksAgo} semaine${weeksAgo === 1 ? "" : "s"}`
            } else {
              purchase.relativeDate = `il y a ${daysAgo} jour${daysAgo === 1 ? "" : "s"}`
            }
          })
        })
        .catch(() => {
          this.purchases = []
          this.purchasesFetchingError = "Échec lors du téléchargement des achats"
        })
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
  },
  mounted() {
    this.fetchCanteenIfNeeded()
  },
  watch: {
    canteenId() {
      this.canteen = null
      this.fetchCanteenIfNeeded()
    },
    nextCanteenId(newValue) {
      if (newValue) {
        this.canteenId = newValue
        this.showCanteenSelection = false
      }
    },
  },
}
</script>

<style scoped>
ul {
  list-style: none;
}
/* https://developer.mozilla.org/en-US/docs/Web/CSS/list-style-type#accessibility_concerns */
ul li::before {
  content: "\200B";
}
</style>
