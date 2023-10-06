<template>
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
</template>

<script>
import { capitalise } from "@/utils"
import Constants from "@/constants"

export default {
  name: "CanteenInfoWidget",
  props: {
    canteen: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      centralKitchen: null,
    }
  },
  computed: {
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
  },
  mounted() {
    this.getCentralKitchen()
  },
  watch: {
    canteen(newCanteen, oldCanteen) {
      if (newCanteen && newCanteen.id !== oldCanteen?.id) {
        this.getCentralKitchen()
      }
    },
  },
}
</script>
