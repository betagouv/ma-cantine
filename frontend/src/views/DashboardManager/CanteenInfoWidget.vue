<template>
  <v-card outlined class="fill-height dsfr no-hover">
    <v-row>
      <v-col cols="4" v-if="$vuetify.breakpoint.smAndUp">
        <v-img :src="canteenImage || '/static/images/canteen-default-image.jpg'" class="fill-height"></v-img>
      </v-col>
      <v-col class="py-sm-8 pr-sm-8">
        <v-card-title><h3 class="fr-h4 mb-2">Mon établissement</h3></v-card-title>
        <v-card-text class="fr-text">
          <p class="mb-0">
            Nom :
            <span class="font-weight-medium">{{ canteen.name }}</span>
          </p>
          <p class="mb-0">
            SIRET :
            <span class="font-weight-medium">{{ canteen.siret || "inconnu" }}</span>
          </p>
          <p v-if="canteen.sirenUniteLegale" class="mb-0">
            SIREN de l'unité légale :
            <span class="font-weight-medium">{{ canteen.sirenUniteLegale }}</span>
          </p>
        </v-card-text>
        <v-spacer v-if="isSatellite"></v-spacer>
        <v-card v-if="isSatellite" class="mx-4 mb-4 mt-2 py-4 px-5" color="grey lighten-4">
          <p class="mb-0 grey--text text--darken-2">
            Mon établissement sert des repas préparés par
            <strong>{{ centralKitchenDisplayName }}</strong>
          </p>
        </v-card>
        <v-spacer></v-spacer>
        <v-card-actions class="mx-2 mb-2">
          <v-btn
            :to="{
              name: 'GestionnaireCantineGerer',
              params: { canteenUrlComponent: $store.getters.getCanteenUrlComponent(canteen) },
            }"
            color="primary"
            outlined
          >
            Gérer mon établissement
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
    isSatellite() {
      return this.canteen.productionType === "site_cooked_elsewhere"
    },
    centralKitchenDisplayName() {
      if (this.canteen.centralKitchen?.name) {
        return this.canteen.centralKitchen.name
      }
      return this.canteen.centralProducerSiret
        ? `l'établissement avec le SIRET ${this.canteen.centralProducerSiret}`
        : "un établissement inconnu"
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
