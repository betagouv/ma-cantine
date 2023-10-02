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
      <h2 class="mt-8 mb-2 fr-h4">
        Ma progression
      </h2>
      <p class="fr-text-sm">
        Vous trouverez ci-dessous une vue d'ensemble de votre progression sur les cinq volets de la loi EGAlim.
      </p>

      <div>
        <EgalimProgression v-if="hasProgression" />
        <EmptyProgression v-else />
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
              <v-card-title class="pb-0"><h3 class="fr-h4 mb-0">Mes achats</h3></v-card-title>
              <v-card-text class="fr-text-xs grey--text text--darken-2 py-0 mt-3">
                <p v-if="!purchases.length">
                  Renseignez vos achats pour calculer automatiquement votre progression sur le volet approvisionnements
                  EGAlim.
                </p>
                <p v-else>Source des données : {{ purchaseDataSourceString }}.</p>
              </v-card-text>
              <v-card-text class="pt-0">
                <v-data-table
                  :items="purchases"
                  :headers="purchaseHeaders"
                  :hide-default-footer="true"
                  :disable-sort="true"
                  class="dsfr-table"
                  :class="purchases.length && 'table-preview'"
                  dense
                >
                  <template v-slot:[`item.characteristics`]="{ item }">
                    {{ getProductCharacteristicsDisplayValue(item.characteristics) }}
                  </template>
                  <template v-slot:[`no-data`]>
                    <v-card outlined rounded class="my-4 py-4 no-purchases" v-if="!purchasesFetchingError">
                      <v-card-text class="fr-text-xs primary--text">
                        Saisissez vos achats manuellement ou connectez votre logiciel de gestion habituel
                      </v-card-text>
                      <v-card-actions class="justify-center">
                        <v-btn
                          :to="{ name: 'PurchasesHome' }"
                          color="primary"
                          class="mx-2 mb-2 fr-text-sm font-weight-medium"
                        >
                          Compléter mes achats
                        </v-btn>
                      </v-card-actions>
                    </v-card>
                    <v-alert outlined type="error" v-else>
                      <p>{{ purchasesFetchingError }}</p>
                      <v-btn @click="fetchPurchases" outlined color="primary">Essayer à nouveau</v-btn>
                    </v-alert>
                  </template>
                </v-data-table>
              </v-card-text>
              <v-spacer></v-spacer>
              <v-card-actions v-if="purchases.length || purchasesFetchingError">
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
            </v-card>
          </v-col>
          <v-col v-if="!canteen.isCentralCuisine" cols="12" md="4" id="publication">
            <v-card outlined class="fill-height d-flex flex-column pa-4">
              <v-card-title class="fr-h4">Ma vitrine en ligne</v-card-title>
              <v-card-text class="fr-text-xs">
                <p>TODO</p>
              </v-card-text>
              <v-spacer></v-spacer>
              <v-card-actions class="mx-2 mb-2 justify-end">
                <v-btn
                  :to="{
                    name: 'PublicationForm',
                    params: { canteenUrlComponent: $store.getters.getCanteenUrlComponent(canteen) },
                  }"
                  color="primary"
                  outlined
                >
                  Éditer ma vitrine
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
          <v-col v-else cols="12" md="4" id="satellites">
            <v-card outlined class="fill-height d-flex flex-column pa-4">
              <v-card-title class="pb-0"><h3 class="fr-h4 mb-0">Mes satellites</h3></v-card-title>
              <v-card-text v-if="!satellites.length" class="fr-text-xs grey--text text--darken-2 mt-3 pb-0">
                <p class="mb-0">Ajoutez et publiez les cantines que vous livrez</p>
              </v-card-text>
              <v-spacer v-if="!satellites.length" />
              <v-card-text class="fr-text-xs grey--text text--darken-2 mt-3 pb-0" v-if="canteen.satelliteCanteensCount">
                <p class="mb-0">{{ satelliteCount }} / {{ canteen.satelliteCanteensCount }} satellites renseignés</p>
              </v-card-text>
              <v-spacer v-if="satellites.length" />
              <v-card-text class="py-0" v-if="satellites.length">
                <v-data-table
                  :items="satellites"
                  :headers="satelliteHeaders"
                  :hide-default-footer="true"
                  :disable-sort="true"
                  class="dsfr-table grey--table"
                  :class="satellites.length && 'table-preview'"
                  dense
                >
                  <template v-slot:[`item.publicationStatus`]="{ item }">
                    <v-chip
                      :color="isPublished(item) ? 'green lighten-4' : 'grey lighten-2'"
                      :class="isPublished(item) ? 'green--text text--darken-4' : 'grey--text text--darken-2'"
                      class="font-weight-bold px-2 fr-text-xs"
                      style="border-radius: 4px !important;"
                      small
                      label
                    >
                      {{ isPublished(item) ? "PUBLIÉE" : "NON PUBLIÉE" }}
                    </v-chip>
                  </template>
                </v-data-table>
              </v-card-text>
              <v-spacer />
              <v-card-actions class="ma-2">
                <v-btn
                  :to="{
                    name: 'SatelliteManagement',
                    params: { canteenUrlComponent: $store.getters.getCanteenUrlComponent(canteen) },
                  }"
                  color="primary"
                  :outlined="!!satellites.length"
                >
                  {{ satellites.length ? "Modifier" : "Ajouter mes satellites" }}
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
          <v-col cols="12" md="8" id="canteen-info-card">
            <v-card outlined class="fill-height">
              <v-row>
                <v-col cols="4" v-if="$vuetify.breakpoint.smAndUp">
                  <v-img :src="canteenImage || '/static/images/canteen-default-image.jpg'" class="fill-height"></v-img>
                </v-col>
                <v-col class="py-8 pr-8">
                  <v-card-title class="fr-h4 mb-2">Mon établissement</v-card-title>
                  <v-card-text class="fr-text">
                    <p class="mb-0">
                      Nom :
                      <span class="font-weight-medium">{{ canteen.name }}</span>
                    </p>
                    <p class="mb-0">
                      Commune :
                      <span class="font-weight-medium">{{ canteenCommune }}</span>
                    </p>
                    <br />
                    <p class="mb-0">
                      <span class="font-weight-medium">{{ canteenProductionType }}</span>
                    </p>
                    <p v-if="centralKitchen">
                      Cuisine centrale :
                      <span class="font-weight-medium">
                        {{ centralKitchen.name || centralKitchen.siret || "Non renseignée" }}
                      </span>
                    </p>
                    <br />
                    <p class="mb-0">
                      Secteur d'activité :
                      <span class="font-weight-medium">{{ canteenSector }}</span>
                    </p>
                    <p class="mb-0">
                      Mode de gestion :
                      <span class="font-weight-medium">{{ canteenMgmt }}</span>
                    </p>
                    <br />
                    <p v-if="canteen.productionType !== 'central'" class="mb-0">
                      Couverts par jour :
                      <span class="font-weight-medium">{{ canteen.dailyMealCount || "Non renseigné" }}</span>
                    </p>
                    <p class="mb-0">
                      Couverts par année :
                      <span class="font-weight-medium">{{ canteen.yearlyMealCount || "Non renseigné" }}</span>
                    </p>
                  </v-card-text>
                  <v-spacer></v-spacer>
                  <v-card-actions class="mx-2 mb-2">
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
                </v-col>
              </v-row>
            </v-card>
          </v-col>
          <v-col cols="12" md="4" id="managers">
            <v-card outlined class="fill-height d-flex flex-column pa-4">
              <v-card-title class="fr-h4">
                Mon équipe
              </v-card-title>
              <v-card-text class="fill-height">
                <div v-if="managers.length > 1" class="fill-height d-flex flex-column">
                  <p class="fr-text mb-0 grey--text text--darken-3">
                    {{ managers.length }} personnes (dont vous) peuvent actuellement modifier cet établissement et
                    ajouter des données.
                  </p>
                  <v-spacer></v-spacer>
                  <ul class="pl-0 fr-text-xs grey--text text--darken-2 mb-n2">
                    <li v-for="manager in managers" :key="manager.email" class="mb-4">
                      <v-row class="align-center mx-0">
                        <v-icon small class="mr-2">
                          {{ manager.isInvite ? "$user-add-line" : "$user-line" }}
                        </v-icon>
                        {{ manager.isInvite ? manager.email : `${manager.firstName} ${manager.lastName}` }}
                        <span v-if="manager.email === loggedUser.email" class="ml-1">(vous)</span>
                      </v-row>
                    </li>
                  </ul>
                  <v-spacer></v-spacer>
                </div>
                <p class="fr-text grey--text text--darken-3" v-else>
                  Actuellement, vous êtes la seule personne qui peut modifier cet établissement et ajouter des données.
                </p>
              </v-card-text>
              <v-spacer></v-spacer>
              <v-card-actions>
                <v-btn
                  :to="{
                    name: 'CanteenManagers',
                    params: { canteenUrlComponent: this.$store.getters.getCanteenUrlComponent(canteen) },
                  }"
                  outlined
                  color="primary"
                  class="mx-2 mb-2"
                >
                  Modifier
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
import EmptyProgression from "./EmptyProgression.vue"
import EgalimProgression from "./EgalimProgression.vue"
import DsfrAutocomplete from "@/components/DsfrAutocomplete"
import { toCurrency, capitalise } from "@/utils"
import Constants from "@/constants"
import validators from "@/validators"

export default {
  name: "DashboardManager",
  components: { EmptyProgression, EgalimProgression, DsfrAutocomplete },
  data() {
    const canteenId = this.$store.state.userCanteenPreviews[6]?.id
    return {
      canteenId,
      nextCanteenId: canteenId,
      canteen: null,
      centralKitchen: null,
      satellites: [],
      satelliteHeaders: [
        { text: "Nom", value: "name" },
        { text: "Statut", value: "publicationStatus" },
      ],
      satelliteCount: null,
      purchases: [],
      purchaseHeaders: [
        { text: "Date", value: "relativeDate" },
        { text: "Produit", value: "description" },
        { text: "Caractéristiques", value: "characteristics" },
        { text: "Prix HT", value: "priceHt" },
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
    hasProgression() {
      return false
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
    // canteen info widget
    canteenCommune() {
      if (!this.canteen.city) {
        return "Non renseigné"
      }
      const departmentString = this.canteen.department ? ` (${this.canteen.department})` : ""
      return `${this.canteen.city}${departmentString}`
    },
    canteenProductionType() {
      const type = Constants.ProductionTypesDetailed.find((mt) => mt.value === this.canteen.productionType)
      return type?.title ? capitalise(type?.title) : "Mode de production non renseigné"
    },
    sectors() {
      const sectors = this.$store.state.sectors
      return this.canteen.sectors.map((sectorId) => sectors.find((s) => s.id === sectorId))
    },
    canteenSector() {
      const sectorString = this.sectors.map((x) => x.name.toLowerCase()).join(", ")
      return sectorString ? capitalise(sectorString) : "Non renseigné"
    },
    canteenMgmt() {
      const type = Constants.ManagementTypes.find((mt) => mt.value === this.canteen.managementType)
      return type?.text || "Non renseigné"
    },
    canteenImage() {
      if (!this.canteen.images || this.canteen.images.length === 0) return null
      return this.canteen.images[0].image
    },
    // purchases widget
    purchaseDataSourceString() {
      if (!this.purchases.length) return
      // TODO: if the latest purchase source is API show that too
      return this.purchases[0].importSource ? "import en masse" : "ajout manuel"
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
          this.updateSatelliteCount()
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
    updateSatelliteCount() {
      if (!this.canteen.isCentralCuisine) return
      const url = `/api/v1/canteens/${this.canteen.id}/satellites?limit=3`
      fetch(url)
        .then((response) => response.json())
        .then((response) => {
          this.satelliteCount = response.count
          this.satellites = response.results
        })
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
    isPublished(canteen) {
      return canteen.publicationStatus === "published"
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
.no-purchases {
  background-color: #f5f5fe;
  border: thin dashed #000091;
}
.v-application .rounded {
  border-radius: 8px !important;
}
</style>
