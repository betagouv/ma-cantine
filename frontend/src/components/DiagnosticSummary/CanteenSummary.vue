<template>
  <div class="fr-text">
    <v-row>
      <v-col cols="12" md="6" class="d-flex align-center pa-0 my-4 my-md-0 left-border">
        <div class="mx-8">
          <v-icon color="primary" x-large>$file-line</v-icon>
        </div>
        <div class="mt-n1">
          <p class="my-0 fr-text-sm grey--text text--darken-1">Nom de la cantine</p>
          <p class="my-0">{{ canteen.name }}</p>
          <p class="mb-0 mt-2 fr-text-sm grey--text text--darken-1">SIRET</p>
          <p class="my-0">{{ canteen.siret || "inconnu" }}</p>
          <p v-if="canteen.sirenUniteLegale" class="mb-0 mt-2 fr-text-sm grey--text text--darken-1">SIREN</p>
          <p class="my-0">{{ canteen.sirenUniteLegale }}</p>
        </div>
      </v-col>
      <v-col cols="12" md="6" class="d-flex align-center pa-0 my-4 my-md-0 left-border">
        <div class="mx-8">
          <v-icon color="primary" x-large>$france-line</v-icon>
        </div>
        <div class="mt-n1">
          <div>
            <p class="my-0 fr-text-sm grey--text text--darken-1">Nombre moyen de couverts par jour</p>
            <p class="my-0">
              {{ canteen.dailyMealCount ? parseInt(canteen.dailyMealCount).toLocaleString("fr-FR") : "—" }}
            </p>
          </div>
          <p class="mb-0 mt-2 fr-text-sm grey--text text--darken-1">Nombre total de couverts par an</p>
          <p class="my-0">
            {{ canteen.yearlyMealCount ? parseInt(canteen.yearlyMealCount).toLocaleString("fr-FR") : "—" }}
          </p>
          <div v-if="isGroupe">
            <p class="mb-0 mt-2 fr-text-sm grey--text text--darken-1">
              Nombre de restaurants satellites à qui je fournis des repas
            </p>
            <p class="my-0">
              {{ canteen.satellitesCount ? parseInt(canteen.satellitesCount).toLocaleString("fr-FR") : "—" }}
            </p>
          </div>
        </div>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="6" class="d-flex align-center pa-0 my-4 my-md-0 left-border">
        <div class="mx-8">
          <v-icon color="primary" x-large>$team-line</v-icon>
        </div>
        <div class="mt-n1">
          <div v-if="!isGroupe">
            <p class="my-0 fr-text-sm grey--text text--darken-1">Modèle économique</p>
            <p class="my-0">{{ economicModel || "—" }}</p>
          </div>
          <p class="mb-0 mt-2 fr-text-sm grey--text text--darken-1">Mode de gestion</p>
          <p class="my-0">{{ managementType || "—" }}</p>
          <p class="mb-0 mt-2 fr-text-sm grey--text text--darken-1">Type de production</p>
          <p class="my-0">{{ productionType || "—" }}</p>
          <div v-if="canteen.groupe">
            <p class="mb-0 mt-2 fr-text-sm grey--text text--darken-1">
              Appartient au groupe de restaurants satellites :
            </p>
            <p class="my-0">« {{ canteen.groupe.name }} » :</p>
          </div>
          <div v-if="canteen.centralProducerSiret">
            <p class="mb-0 mt-2 fr-text-sm grey--text text--darken-1">SIRET de la cuisine centrale</p>
            <p class="my-0">{{ canteen.centralProducerSiret }}</p>
          </div>
        </div>
      </v-col>
      <v-col v-if="!isGroupe" cols="12" md="6" class="d-flex align-center pa-0 my-4 my-md-0 left-border">
        <div class="mx-8">
          <v-icon color="primary" x-large>$france-line</v-icon>
        </div>
        <div class="mt-n1">
          <p class="my-0 fr-text-sm grey--text text--darken-1">Commune</p>
          <p class="my-0">{{ canteen.city && canteen.cityInseeCode ? canteen.city : "—" }}</p>
        </div>
      </v-col>
    </v-row>
    <v-row v-if="hasSite">
      <v-col cols="12" class="d-flex align-center pa-0 my-4 my-md-0 left-border">
        <div class="mx-8">
          <v-icon color="primary" x-large>$building-line</v-icon>
        </div>
        <div class="mt-n1">
          <p class="my-0 fr-text-sm grey--text text--darken-1">Secteur d'activité</p>
          <p class="my-0">{{ sectors || "—" }}</p>
          <div v-if="lineMinistryRequired">
            <p class="mb-0 mt-2 fr-text-sm grey--text text--darken-1">
              Administration générale de tutelle
            </p>
            <p class="my-0">{{ lineMinistry || "—" }}</p>
          </div>
        </div>
      </v-col>
    </v-row>
    <SatellitesWidget v-if="isGroupe" :canteen="canteen" />
  </div>
</template>

<script>
import Constants from "@/constants"
import SatellitesWidget from "@/views/DashboardManager/SatellitesWidget.vue"
import { sectorDisplayString, lineMinistryRequired } from "@/utils"

export default {
  name: "CanteenSummary",
  components: { SatellitesWidget },
  props: {
    canteen: {
      type: Object,
      required: true,
    },
  },
  computed: {
    isGroupe() {
      return this.canteen.productionType === "groupe"
    },
    productionType() {
      const productionType = Constants.ProductionTypesDetailed.find((x) => x.value === this.canteen.productionType)
      return productionType?.body
    },
    managementType() {
      const managementType = Constants.ManagementTypes.find((x) => x.value === this.canteen.managementType)
      return managementType?.text
    },
    sectors() {
      return sectorDisplayString(this.canteen.sectorList, this.$store.state.sectors)
    },
    lineMinistryRequired() {
      return lineMinistryRequired(this.canteen, this.$store.state.sectors)
    },
    lineMinistry() {
      if (!this.canteen.lineMinistry) return
      const allMinistries = this.$store.state.lineMinistries
      const ministry = allMinistries.find((m) => m.value === this.canteen.lineMinistry)
      return ministry?.text
    },
    economicModel() {
      const managementType = Constants.EconomicModels.find((x) => x.value === this.canteen.economicModel)
      return managementType?.text
    },
    hasSite() {
      return this.canteen.productionType !== "central" && !this.isGroupe
    },
  },
}
</script>

<style scoped>
.left-border {
  border-left: solid #e3e3fd;
}
.row {
  margin: 36px 0;
}
</style>
