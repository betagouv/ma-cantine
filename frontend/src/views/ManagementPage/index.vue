<template>
  <div class="text-left">
    <v-alert type="success" v-if="$route.query.operation">
      Cantine bien {{ $route.query.operation === "cree" ? "crée" : "modifiée" }}
    </v-alert>
    <div class="mt-12">
      <h2 class="my-4">Mes cantines</h2>
      <v-row>
        <v-col cols="12" sm="6" md="4" height="100%" v-for="canteen in canteens" :key="`canteen-${canteen.id}`">
          <CanteenCard :canteen="canteen" class="fill-height" />
        </v-col>
        <v-col cols="12" sm="6" md="4" height="100%">
          <v-card
            color="grey lighten-5"
            class="fill-height d-flex flex-column align-center justify-center"
            :to="{ name: 'NewCanteen' }"
          >
            <v-icon size="100">mdi-plus</v-icon>
            <v-card-text class="font-weight-bold pt-0 text-center">
              Ajouter une cantine
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </div>
    <div class="my-12">
      <h2 class="">Mes diagnostics</h2>
      <v-btn text color="primary" class="mt-2 mb-8 ml-n4" :to="{ name: 'NewDiagnostic' }">
        <v-icon class="mr-2">mdi-plus</v-icon>
        Ajouter un diagnostic
      </v-btn>
      <v-row>
        <v-col cols="12" v-for="diagnostic in diagnostics" :key="`diagnostic-${diagnostic.id}`">
          <DiagnosticCard :diagnostic="diagnostic" class="fill-height" />
        </v-col>
      </v-row>
    </div>
    <div class="my-8">
      <h2 class="my-4">Mes outils</h2>
      <v-row>
        <v-col cols="12" sm="6" md="8" height="100%">
          <v-card outlined class="d-flex flex-column fill-height pa-2">
            <v-card-title class="font-weight-bold">Tableur d'aide pour le calcul</v-card-title>
            <v-card-text>
              Si vous ne connaissez pas votre part de bio, produits durables, produits issues du commerce équitable,
              nous vous proposons un outil simple pour les calculer. Sous forme de tableur, remplissez vos achats HT
              suivant leurs labels et/ou sigles de qualité.
            </v-card-text>
            <v-spacer></v-spacer>
            <v-card-actions class="px-4">
              <v-spacer></v-spacer>
              <v-dialog max-width="700" v-model="calculatorModal">
                <template v-slot:activator="{ on, attrs }">
                  <v-btn outlined color="primary" v-on="on" v-bind="attrs">
                    Télécharger notre tableur
                  </v-btn>
                </template>
                <CalculatorResourceModal @closeModal="closeCalculatorModal" />
              </v-dialog>
            </v-card-actions>
          </v-card>
        </v-col>
        <v-col cols="12" sm="6" md="4" height="100%">
          <v-card outlined class="d-flex flex-column fill-height pa-2">
            <v-card-title class="font-weight-bold">Documentation</v-card-title>
            <v-card-text>
              Ressources pour les acteurs et actrices de la restauration collective
            </v-card-text>
            <v-spacer></v-spacer>
            <v-card-actions class="px-4">
              <v-spacer></v-spacer>
              <v-btn href="https://ma-cantine-1.gitbook.io/ma-cantine-egalim/" target="_blank" outlined color="primary">
                Visiter
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12" sm="6" height="100%">
          <v-card outlined class="d-flex flex-column fill-height pa-2">
            <v-card-title class="font-weight-bold">Générateur d'affiches</v-card-title>
            <v-card-text>
              Vous pouvez générer une affiche à poser dans votre cantine ainsi qu’un email-type à destination des
              convives et parents d'élèves.
            </v-card-text>
            <v-spacer></v-spacer>
            <v-card-actions class="px-4">
              <v-spacer></v-spacer>
              <v-btn :to="{ name: 'GeneratePosterPage' }" outlined color="primary">J'informe mes convives</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
        <v-col cols="12" sm="6" height="100%">
          <v-card outlined class="d-flex flex-column fill-height pa-2">
            <v-card-title class="font-weight-bold">Blog</v-card-title>
            <v-card-text>
              Découvrez notre espace blog et témoignages
            </v-card-text>
            <v-spacer></v-spacer>
            <v-card-actions class="px-4">
              <v-spacer></v-spacer>
              <v-btn :to="{ name: 'BlogsHome' }" outlined color="primary">Visiter</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </div>
  </div>
</template>

<script>
import CanteenCard from "./CanteenCard"
import DiagnosticCard from "@/components/DiagnosticCard"
import CalculatorResourceModal from "@/components/KeyMeasureResource/CalculatorResourceModal"

export default {
  components: { CanteenCard, DiagnosticCard, CalculatorResourceModal },
  data() {
    return {
      calculatorModal: false,
    }
  },
  computed: {
    loggedUser() {
      return this.$store.state.loggedUser
    },
    canteens() {
      return this.$store.state.userCanteens
    },
    diagnostics() {
      let diagnostics = this.$store.state.userCanteens.flatMap((canteen) => canteen.diagnostics)
      diagnostics.sort((diag1, diag2) => diag2.year - diag1.year)
      return diagnostics
    },
  },
  methods: {
    closeCalculatorModal() {
      this.calculatorModal = false
    },
  },
}
</script>
