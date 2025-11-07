<template>
  <div class="text-left" v-if="canteen">
    <v-row>
      <v-col>
        <ProductionTypeTag :canteen="canteen" class="mt-2" />
        <h1 class="fr-h3 mt-2 mb-2">{{ canteen.name }}</h1>
        <p class="mb-0">SIRET : {{ canteen.siret || "inconnu" }}</p>
        <p v-if="canteen.sirenUniteLegale" class="mb-0">
          <span>SIREN de l'unité légale : {{ canteen.sirenUniteLegale }}</span>
        </p>
      </v-col>
    </v-row>

    <v-row v-if="canteenPreviews.length > 1">
      <v-col>
        <v-btn outlined color="primary" class="fr-btn--tertiary" :to="{ name: 'GestionnaireTableauDeBord' }">
          Changer d'établissement
        </v-btn>
      </v-col>
    </v-row>

    <div>
      <div class="mt-4">
        <EgalimProgression :canteen="canteen" />
      </div>

      <div>
        <h2 class="mt-10 mb-2 fr-h2">
          Mon établissement
        </h2>
        <p class="fr-text-sm">
          Accédez ci-dessous aux différents outils de gestion de votre établissement sur la plateforme « ma cantine ».
        </p>
        <v-row v-if="canteen.isCentralCuisine">
          <v-col cols="12" md="6">
            <SatellitesWidget :canteen="canteen" />
          </v-col>
          <v-col cols="12" md="6">
            <PublicationWidget :canteen="canteen" />
          </v-col>
          <v-col cols="12">
            <PurchasesWidget :canteen="canteen" />
          </v-col>
          <v-col cols="12" md="8">
            <CanteenInfoWidget :canteen="canteen" />
          </v-col>
          <v-col cols="12" md="4">
            <TeamWidget :canteen="canteen" />
          </v-col>
        </v-row>
        <v-row v-else>
          <v-col cols="12" md="8">
            <PurchasesWidget :canteen="canteen" />
          </v-col>
          <v-col cols="12" md="4">
            <PublicationWidget :canteen="canteen" />
          </v-col>
          <v-col cols="12" md="8">
            <CanteenInfoWidget :canteen="canteen" />
          </v-col>
          <v-col cols="12" md="4">
            <TeamWidget :canteen="canteen" />
          </v-col>
        </v-row>
      </div>
    </div>
  </div>
</template>

<script>
import EgalimProgression from "./EgalimProgression"
import PurchasesWidget from "./PurchasesWidget"
import PublicationWidget from "./PublicationWidget"
import SatellitesWidget from "./SatellitesWidget"
import CanteenInfoWidget from "./CanteenInfoWidget"
import TeamWidget from "./TeamWidget"
import ProductionTypeTag from "@/components/ProductionTypeTag"

export default {
  name: "DashboardManager",
  components: {
    EgalimProgression,
    PurchasesWidget,
    PublicationWidget,
    SatellitesWidget,
    CanteenInfoWidget,
    TeamWidget,
    ProductionTypeTag,
  },
  data() {
    return {
      canteen: null,
      showCanteenSelection: false,
    }
  },
  props: {
    canteenUrlComponent: {
      type: String,
    },
  },
  computed: {
    canteenId() {
      return this.canteenUrlComponent.split("--")[0]
    },
    loggedUser() {
      return this.$store.state.loggedUser
    },
    canteenPreviews() {
      return this.$store.state.userCanteenPreviews
    },
    welcomesGuests() {
      return this.canteen?.productionType !== "central"
    },
    isCentralWithSite() {
      return this.canteen?.productionType === "central_serving"
    },
  },
  methods: {
    fetchCanteenIfNeeded() {
      if (this.canteen?.id === this.canteenId) return
      const id = this.canteenId
      return this.$store
        .dispatch("fetchCanteen", { id })
        .then((canteen) => {
          this.$set(this, "canteen", canteen)
        })
        .catch(() => {
          this.$set(this, "canteen", null)
          this.$router.replace({ name: "GestionnaireTableauDeBord" }).then(() => {
            this.$store.dispatch("notify", {
              message: "Nous n'avons pas trouvé cette cantine",
              status: "error",
            })
          })
        })
    },
  },
  mounted() {
    this.fetchCanteenIfNeeded()
  },
  watch: {
    canteenUrlComponent() {
      this.$set(this, "canteen", null)
      this.fetchCanteen()
    },
    $route() {
      this.fetchCanteenIfNeeded()
    },
  },
}
</script>

<style scoped>
.constrained {
  max-width: 1200px !important;
}
.v-card.dsfr {
  border: solid 1.5px #dddddd;
}
</style>
