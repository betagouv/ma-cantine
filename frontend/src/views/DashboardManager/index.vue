<template>
  <div class="text-left">
    <h1 class="my-4 fr-display-xs" v-if="canteen">{{ canteen.name }}</h1>
    <h1 class="my-4 fr-display-xs" v-else>Bienvenue {{ loggedUser.firstName }}</h1>
    <v-row v-if="canteenPreviews.length > 1">
      <v-col>
        <v-btn outlined small color="primary" :to="{ name: 'ManagementPage' }">
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
          <v-col v-else cols="12" md="4">
            <SatellitesWidget :canteen="canteen" />
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
import SatellitesWidget from "./SatellitesWidget"
import CanteenInfoWidget from "./CanteenInfoWidget"
import TeamWidget from "./TeamWidget"

export default {
  name: "DashboardManager",
  components: {
    EgalimProgression,
    PurchasesWidget,
    PublicationWidget,
    SatellitesWidget,
    CanteenInfoWidget,
    TeamWidget,
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
          this.$store.dispatch("notify", {
            message: "Nous n'avons pas trouvé cette cantine",
            status: "error",
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
</style>
