<template>
  <div class="fr-text">
    <p class="my-0 fr-text-sm grey--text text--darken-1">Nom de la cantine</p>
    <p class="mt-1 mb-4 font-weight-bold">{{ canteen.name }}</p>
    <DsfrCallout>
      <p class="ma-0">
        Choisir un nom précis pour votre établissement permet aux convives de vous trouver plus facilement. Par exemple
        :
        <span class="font-italic">
          École maternelle Olympe de Gouges, Centre Hospitalier de Bayonne, Restaurant administratif Les Lucioles...
        </span>
      </p>
    </DsfrCallout>
    <v-row>
      <v-col cols="12" md="6" class="d-flex align-center pa-0 my-4 my-md-0 left-border">
        <div class="mx-8">
          <v-icon color="primary" x-large>$file-line</v-icon>
        </div>
        <div class="mt-n1">
          <p class="my-0 fr-text-sm grey--text text--darken-1">SIRET</p>
          <p class="my-0">{{ canteen.siret || "—" }}</p>
        </div>
      </v-col>
      <v-col cols="12" md="6" class="d-flex align-center pa-0 my-4 my-md-0 left-border">
        <div class="mx-8">
          <v-icon color="primary" x-large>$france-line</v-icon>
        </div>
        <div class="mt-n1">
          <p class="my-0 fr-text-sm grey--text text--darken-1">Commune</p>
          <p class="my-0">{{ canteen.city || "—" }}</p>
        </div>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" class="d-flex align-center pa-0 my-4 my-md-0 left-border">
        <div class="mx-8">
          <v-icon color="primary" x-large>$team-line</v-icon>
        </div>
        <div class="mt-n1">
          <p class="my-0 fr-text-sm grey--text text--darken-1">Type de production</p>
          <p class="my-0">{{ productionType || "—" }}</p>
          <p class="mb-0 mt-2 fr-text-sm grey--text text--darken-1">Mode de gestion</p>
          <p class="my-0">{{ managementType || "—" }}</p>
        </div>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="6" class="d-flex align-center pa-0 my-4 my-md-0 left-border">
        <div class="mx-8">
          <v-icon color="primary" x-large>$building-line</v-icon>
        </div>
        <div class="mt-n1">
          <p class="my-0 fr-text-sm grey--text text--darken-1">Secteur d'activité</p>
          <p class="my-0">{{ sectors || "—" }}</p>
          <p class="mb-0 mt-2 fr-text-sm grey--text text--darken-1">Type d'établissement</p>
          <p class="my-0">{{ managementType || "—" }}</p>
        </div>
      </v-col>
      <v-col cols="12" md="6" class="d-flex align-center pa-0 my-4 my-md-0 left-border">
        <div class="mx-8">
          <v-icon color="primary" x-large>$restaurant-line</v-icon>
        </div>
        <div class="mt-n1">
          <p class="my-0 fr-text-sm grey--text text--darken-1">Couverts moyens par jour</p>
          <p class="my-0">{{ parseInt(canteen.dailyMealCount).toLocaleString("fr-FR") || "—" }}</p>
          <p class="mb-0 mt-2 fr-text-sm grey--text text--darken-1">Nombre total de couverts à l’année</p>
          <p class="my-0">{{ parseInt(canteen.yearlyMealCount).toLocaleString("fr-FR") || "—" }}</p>
        </div>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import DsfrCallout from "@/components/DsfrCallout"
import Constants from "@/constants"
import { sectorDisplayString } from "@/utils"

export default {
  name: "CanteenSummary",
  components: { DsfrCallout },
  props: {
    canteen: {
      type: Object,
      required: true,
    },
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
    economicModel() {
      const managementType = Constants.EconomicModels.find((x) => x.value === this.canteen.economicModel)
      return managementType?.text
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
