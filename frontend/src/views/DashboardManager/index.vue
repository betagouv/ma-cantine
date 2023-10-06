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
          class="mt-6"
          auto-select-first
          no-data-text="Pas de résultats"
          @blur="showCanteenSelection = false"
          autofocus
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
          <v-col cols="12" md="8">
            <PurchasesWidget :canteen="canteen" />
          </v-col>
          <v-col v-if="!canteen.isCentralCuisine" cols="12" md="4">
            <PublicationWidget :canteen="canteen" />
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
                  :class="`dsfr-table grey--table ${satellites.length && 'table-preview'}`"
                  dense
                >
                  <template v-slot:[`item.publicationStatus`]="{ item }">
                    <v-chip
                      :color="isSatellitePublished(item) ? 'green lighten-4' : 'grey lighten-2'"
                      :class="isSatellitePublished(item) ? 'green--text text--darken-4' : 'grey--text text--darken-2'"
                      class="font-weight-bold px-2 fr-text-xs text-uppercase"
                      style="border-radius: 4px !important;"
                      small
                      label
                    >
                      {{ isSatellitePublished(item) ? "Publiée" : "Non publiée" }}
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
                      <span v-if="canteen.productionType === 'central'">Couverts livrés à l'année :</span>
                      <span v-else-if="canteen.productionType === 'central_serving'">
                        Couverts à l'année (y compris livrés) :
                      </span>
                      <span v-else>Couverts par année :</span>
                      <span class="font-weight-medium ml-1">{{ canteen.yearlyMealCount || "Non renseigné" }}</span>
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
import EgalimProgression from "./EgalimProgression"
import PurchasesWidget from "./PurchasesWidget"
import PublicationWidget from "./PublicationWidget"
import DsfrAutocomplete from "@/components/DsfrAutocomplete"
import { capitalise } from "@/utils"
import Constants from "@/constants"

export default {
  name: "DashboardManager",
  components: { EgalimProgression, DsfrAutocomplete, PurchasesWidget, PublicationWidget },
  data() {
    const canteenId = +this.$route.query.cantine || this.$store.state.userCanteenPreviews[0]?.id
    return {
      canteenId,
      nextCanteenId: canteenId,
      canteen: null,
      showCanteenSelection: false,
      // canteen info widget
      centralKitchen: null,
      satellites: [],
      satelliteHeaders: [
        { text: "Nom", value: "name" },
        { text: "Statut", value: "publicationStatus" },
      ],
      satelliteCount: null,
    }
  },
  computed: {
    loggedUser() {
      return this.$store.state.loggedUser
    },
    canteenPreviews() {
      return this.$store.state.userCanteenPreviews
    },
    // team widget
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
  },
  methods: {
    fetchCanteenIfNeeded() {
      if (!this.canteenId) {
        this.canteen = null
        return
      }
      if (this.canteen?.id === this.canteenId) return
      const id = this.canteenId
      return this.$store
        .dispatch("fetchCanteen", { id })
        .then((canteen) => {
          this.canteen = canteen
          this.getCentralKitchen()
          this.updateSatelliteCount()
          this.$router.push({ query: { cantine: id } }).catch(() => {})
        })
        .catch(() => {
          this.canteen = null
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
    isSatellitePublished(canteen) {
      return canteen.publicationStatus === "published"
    },
  },
  mounted() {
    this.fetchCanteenIfNeeded()
  },
  watch: {
    canteenId() {
      this.fetchCanteenIfNeeded()
    },
    nextCanteenId(newValue) {
      if (newValue) {
        this.canteenId = newValue
        this.showCanteenSelection = false
      }
    },
    $route(newRoute, oldRoute) {
      if (newRoute.query.cantine !== oldRoute.query.cantine) {
        this.nextCanteenId = +newRoute.query.cantine
      }
    },
  },
}
</script>

<style scoped>
.constrained {
  max-width: 1200px !important;
}

ul {
  list-style: none;
}
/* https://developer.mozilla.org/en-US/docs/Web/CSS/list-style-type#accessibility_concerns */
ul li::before {
  content: "\200B";
}
</style>
