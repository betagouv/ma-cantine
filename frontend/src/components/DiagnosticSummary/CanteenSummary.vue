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
          <p v-if="canteen.sirenUniteLegale" class="mb-0 mt-2 fr-text-sm grey--text text--darken-1">
            SIREN de l'unité légale
          </p>
          <p class="my-0">{{ canteen.sirenUniteLegale }}</p>
        </div>
      </v-col>
      <v-col cols="12" md="6" class="d-flex align-center pa-0 my-4 my-md-0 left-border">
        <div class="mx-8">
          <v-icon color="primary" x-large>$france-line</v-icon>
        </div>
        <div class="mt-n1">
          <p class="my-0 fr-text-sm grey--text text--darken-1">Commune</p>
          <p class="my-0">{{ canteen.city && canteen.cityInseeCode ? canteen.city : "—" }}</p>
        </div>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="6" class="d-flex align-center pa-0 my-4 my-md-0 left-border">
        <div class="mx-8">
          <v-icon color="primary" x-large>$team-line</v-icon>
        </div>
        <div class="mt-n1">
          <p class="my-0 fr-text-sm grey--text text--darken-1">Type d'établissement</p>
          <p class="my-0">{{ economicModel || "—" }}</p>
          <p class="mb-0 mt-2 fr-text-sm grey--text text--darken-1">Mode de gestion</p>
          <p class="my-0">{{ managementType || "—" }}</p>
          <p class="mb-0 mt-2 fr-text-sm grey--text text--darken-1">Type de production</p>
          <p class="my-0">{{ productionType || "—" }}</p>
          <div v-if="isSatellite">
            <p class="mb-0 mt-2 fr-text-sm grey--text text--darken-1">SIRET du livreur</p>
            <p class="my-0">
              <span v-if="canteen.centralKitchen && canteen.centralKitchen.name">
                « {{ canteen.centralKitchen.name }} » :
              </span>
              {{ canteen.centralProducerSiret || "—" }}
            </p>
          </div>
        </div>
      </v-col>
      <v-col cols="12" md="6" class="d-flex align-center pa-0 my-4 my-md-0 left-border">
        <div class="mx-8">
          <v-icon color="primary" x-large>$restaurant-line</v-icon>
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
          <div v-if="canteen.isCentralCuisine">
            <p class="mb-0 mt-2 fr-text-sm grey--text text--darken-1">
              Nombre de cantines à qui je fournis des repas
            </p>
            <p class="my-0">
              {{
                canteen.satelliteCanteensCount ? parseInt(canteen.satelliteCanteensCount).toLocaleString("fr-FR") : "—"
              }}
            </p>
          </div>
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
    <v-row v-if="canteen.isCentralCuisine">
      <v-col cols="12" class="pb-0">
        <h3 class="fr-h6">Mes satellites</h3>
        <p class="fr-text-sm mb-1 d-flex align-center" :class="{ 'dark-orange': hasSatelliteInconsistency }">
          <v-icon v-if="hasSatelliteInconsistency" small class="mr-1 dark-orange">$alert-line</v-icon>
          {{ satelliteCountSentence }}
        </p>
      </v-col>
      <v-col cols="12" md="8">
        <v-data-table
          :items="canteen.satellites"
          :headers="satelliteHeaders"
          :hide-default-footer="true"
          :disable-sort="true"
          :class="`dsfr-table grey--table`"
          dense
        />
      </v-col>
      <v-col cols="12">
        <p>
          <v-btn :to="{ name: 'SatelliteManagement' }" outlined small color="primary" class="fr-btn--tertiary px-2">
            Gérer mes satellites
          </v-btn>
        </p>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import Constants from "@/constants"
import { lastYear, sectorDisplayString, hasSatelliteInconsistency, lineMinistryRequired } from "@/utils"

export default {
  name: "CanteenSummary",
  props: {
    canteen: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      satelliteHeaders: [
        { text: "Nom", value: "name" },
        { text: "SIRET", value: "siret" },
      ],
      lastYear: lastYear(),
    }
  },
  computed: {
    productionType() {
      const productionType = Constants.ProductionTypesDetailed.find((x) => x.value === this.canteen.productionType)
      return productionType?.body
    },
    managementType() {
      const managementType = Constants.ManagementTypes.find((x) => x.value === this.canteen.managementType)
      return managementType?.text
    },
    sectors() {
      return sectorDisplayString(this.canteen.sectors, this.$store.state.sectors)
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
      return this.canteen.productionType !== "central"
    },
    isSatellite() {
      return this.canteen?.productionType === "site_cooked_elsewhere"
    },
    hasSatelliteInconsistency() {
      return hasSatelliteInconsistency(this.canteen)
    },
    satelliteCountSentence() {
      const satPluralize = this.canteen.satelliteCanteensCount > 1 ? "satellites" : "satellite"
      const fillPluralize = this.canteen.satellites.length > 1 ? "renseignés" : "renseigné"
      return `${this.canteen.satellites.length} sur ${this.canteen.satelliteCanteensCount} ${satPluralize} ${fillPluralize}`
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
