<template>
  <div class="text-left pb-10">
    <h1 class="font-weight-black text-h4 my-4">
      {{ isNewDiagnostic ? "Nouveaux diagnostic" : "Modifier mon diagnostic" }}
    </h1>
    <div class="mb-8 mt-2" v-if="!isNewDiagnostic && canteen">
      <v-chip small :color="canteen.dataIsPublic ? 'green lighten-4' : 'grey lighten-4'" label>
        {{ canteen.dataIsPublic ? "Publiée" : "Pas encore publiée" }}
      </v-chip>
    </div>
    <v-form>
      <v-row>
        <v-col cols="12" md="5">
          <p class="body-2 my-2">Cantine</p>
          <v-select
            solo
            ref="canteenSelect"
            :value="canteen ? canteen.id : undefined"
            :rules="[validators.notEmpty]"
            :items="$store.state.userCanteens"
            item-text="name"
            item-value="id"
            hide-details="auto"
            placeholder="Choisissez votre cantine"
          ></v-select>
        </v-col>
        <v-col cols="12" md="3">
          <p class="body-2 my-2">Année</p>
          <v-select
            solo
            v-model="diagnostic.year"
            :rules="[validators.notEmpty]"
            :items="allowedYears"
            hide-details="auto"
            placeholder="Année du diagnostic"
          ></v-select>
        </v-col>
        <v-col cols="12" class="mb-8 mt-4">
          <v-divider></v-divider>
        </v-col>
      </v-row>

      <p class="caption grey--text">Cliquez sur les catégories ci-dessous pour remplir votre diagnostic</p>

      <v-expansion-panels class="mb-8">
        <v-expansion-panel>
          <v-expansion-panel-header>
            <div class="font-weight-bold">
              <v-icon class="mr-2" color="red">
                mdi-food-apple
              </v-icon>
              Au moins 50% de produits de qualité et durables dont 20% de bio
            </div>
          </v-expansion-panel-header>
          <v-expansion-panel-content>TODO</v-expansion-panel-content>
        </v-expansion-panel>

        <v-expansion-panel>
          <v-expansion-panel-header>
            <div class="font-weight-bold">
              <v-icon class="mr-2" color="orange darken-2">
                mdi-offer
              </v-icon>
              Lutte contre le gaspillage alimentaire et dons alimentaires
            </div>
          </v-expansion-panel-header>
          <v-expansion-panel-content><WasteMeasure :diagnostic="diagnostic" /></v-expansion-panel-content>
        </v-expansion-panel>
        <v-expansion-panel>
          <v-expansion-panel-header>
            <div class="font-weight-bold">
              <v-icon class="mr-2" color="green darken-1">
                mdi-leaf
              </v-icon>
              Diversification des sources de protéines et menus végétariens
            </div>
          </v-expansion-panel-header>
          <v-expansion-panel-content><DiversificationMeasure :diagnostic="diagnostic" /></v-expansion-panel-content>
        </v-expansion-panel>
        <v-expansion-panel>
          <v-expansion-panel-header>
            <div class="font-weight-bold">
              <v-icon class="mr-2" color="blue darken-1">
                mdi-weather-windy
              </v-icon>
              Substitution des plastiques
            </div>
          </v-expansion-panel-header>
          <v-expansion-panel-content><NoPlasticMeasure :diagnostic="diagnostic" /></v-expansion-panel-content>
        </v-expansion-panel>
        <v-expansion-panel>
          <v-expansion-panel-header>
            <div class="font-weight-bold">
              <v-icon class="mr-2" color="amber darken-2">
                mdi-bullhorn
              </v-icon>
              Information des usagers et convives
            </div>
          </v-expansion-panel-header>
          <v-expansion-panel-content><InformationMeasure :diagnostic="diagnostic" /></v-expansion-panel-content>
        </v-expansion-panel>
      </v-expansion-panels>
    </v-form>

    <v-sheet rounded color="grey lighten-4 pa-3" class="d-flex">
      <v-spacer></v-spacer>
      <v-btn x-large color="primary">Valider</v-btn>
    </v-sheet>
  </div>
</template>

<script>
import validators from "@/validators"
import InformationMeasure from "@/components/KeyMeasureDiagnostic/InformationMeasure"
import WasteMeasure from "@/components/KeyMeasureDiagnostic/WasteMeasure"
import DiversificationMeasure from "@/components/KeyMeasureDiagnostic/DiversificationMeasure"
import NoPlasticMeasure from "@/components/KeyMeasureDiagnostic/NoPlasticMeasure"

export default {
  name: "DiagnosticEditor",
  data() {
    return {
      diagnostic: {},
    }
  },
  components: { InformationMeasure, WasteMeasure, DiversificationMeasure, NoPlasticMeasure },
  props: {
    canteenUrlComponent: {
      type: String,
      required: false,
    },
    year: {
      required: false,
    },
  },
  computed: {
    isNewDiagnostic() {
      return !this.canteenUrlComponent && !this.year
    },
    canteen() {
      if (this.isNewDiagnostic) return null
      return this.$store.getters.getCanteenFromUrlComponent(this.canteenUrlComponent)
    },
    validators() {
      return validators
    },
    allowedYears() {
      return [
        {
          text: "2019",
          value: 2019,
        },
        {
          text: "2020",
          value: 2020,
        },
        {
          text: "2021 (prévisionnel)",
          value: 2021,
        },
        {
          text: "2022 (prévisionnel)",
          value: 2022,
        },
      ]
    },
  },
  mounted() {
    if (this.isNewDiagnostic) return

    if (!this.canteen) this.$router.push({ name: "Landing" })

    const diagnostic = this.canteen.diagnostics.find((diagnostic) => diagnostic.year === parseInt(this.year))
    if (diagnostic) this.diagnostic = JSON.parse(JSON.stringify(diagnostic))
    else this.$router.push({ name: "Landing" })
  },
}
</script>
