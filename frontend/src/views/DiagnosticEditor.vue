<template>
  <div class="text-left pb-10">
    <h1 class="font-weight-black text-h4 my-4">
      {{ isNewDiagnostic ? "Nouveaux diagnostic" : "Modifier mon diagnostic" }}
    </h1>
    <v-form ref="form" v-model="formIsValid">
      <v-row>
        <v-col cols="12" md="5">
          <p class="body-2 my-2">Cantine</p>
          <v-select
            solo
            ref="canteenSelect"
            v-model="selectedCanteenId"
            :rules="[validators.notEmpty, validators.diagnosticIsUnique]"
            :items="userCanteens"
            item-text="name"
            item-value="id"
            hide-details="auto"
            placeholder="Choisissez votre cantine"
            v-if="isNewDiagnostic"
          ></v-select>
          <div v-else class="text-h6 font-weight-bold">{{ canteen.name }}</div>
        </v-col>
        <v-col cols="12" md="3">
          <p class="body-2 my-2">Année</p>
          <v-select
            solo
            ref="yearSelect"
            v-model="diagnostic.year"
            :rules="[validators.notEmpty, validators.diagnosticIsUnique]"
            :items="allowedYears"
            hide-details="auto"
            placeholder="Année du diagnostic"
            v-if="isNewDiagnostic"
          ></v-select>
          <div v-else class="text-h6 font-weight-bold">{{ diagnostic.year }}</div>
        </v-col>
        <v-col v-if="!diagnosticIsUnique" cols="12" class="ma-0 text-body-2 red--text">
          Un diagnostic pour cette cantine et cette année existe déjà.
          <v-btn small text class="text-decoration-underline text-body-2 mt-n1" @click="goToExistingDiagnostic">
            Modifier le diagnostic existant.
          </v-btn>
        </v-col>
        <v-col cols="12" class="mb-8 mt-3">
          <v-divider></v-divider>
        </v-col>
      </v-row>

      <p class="caption grey--text">Cliquez sur les catégories ci-dessous pour remplir votre diagnostic</p>

      <v-expansion-panels class="mb-8" :disabled="!diagnosticIsUnique">
        <v-expansion-panel>
          <v-expansion-panel-header>
            <template v-slot:default="{ open }">
              <v-row no-gutters>
                <v-col cols="7" class="font-weight-bold">
                  <v-icon class="mr-2" color="red">
                    mdi-food-apple
                  </v-icon>
                  Au moins 50% de produits de qualité et durables dont 20% de bio
                </v-col>
                <v-col cols="5" class="text--secondary text-right pr-2 align-self-center align-self-center">
                  <v-fade-transition leave-absolute>
                    <span v-if="!open" key="0">
                      {{ approSummary() || "Incomplèt" }}
                    </span>
                  </v-fade-transition>
                </v-col>
              </v-row>
            </template>
          </v-expansion-panel-header>
          <v-expansion-panel-content>
            <QualityMeasureValuesInput
              :originalDiagnostic="diagnostic"
              label="La valeur (en HT) de mes achats alimentaires..."
            />
          </v-expansion-panel-content>
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
          <!-- TODO: waste actions multiple choice not working -->
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
            <template v-slot:default="{ open }">
              <v-row no-gutters>
                <v-col cols="4" class="font-weight-bold">
                  <v-icon class="mr-2" color="blue darken-1">
                    mdi-weather-windy
                  </v-icon>
                  Substitution des plastiques
                </v-col>
                <v-col cols="8" class="text--secondary text-right pr-2 align-self-center">
                  <v-fade-transition leave-absolute>
                    <span v-if="!open" key="0">
                      {{ plasticSummary() }}
                    </span>
                  </v-fade-transition>
                </v-col>
              </v-row>
            </template>
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
      <v-btn x-large outlined color="primary" class="mr-4 align-self-center" :to="{ name: 'ManagementPage' }">
        Annuler
      </v-btn>
      <v-btn x-large color="primary" @click="saveDiagnostic" :disabled="!diagnosticIsUnique">
        Valider
      </v-btn>
    </v-sheet>
  </div>
</template>

<script>
import validators from "@/validators"
import InformationMeasure from "@/components/KeyMeasureDiagnostic/InformationMeasure"
import WasteMeasure from "@/components/KeyMeasureDiagnostic/WasteMeasure"
import DiversificationMeasure from "@/components/KeyMeasureDiagnostic/DiversificationMeasure"
import NoPlasticMeasure from "@/components/KeyMeasureDiagnostic/NoPlasticMeasure"
import QualityMeasureValuesInput from "@/components/KeyMeasureDiagnostic/QualityMeasureValuesInput"
import { getObjectDiff } from "@/utils"

function percentage(part, total) {
  return Math.round((part / total) * 100)
}

const LEAVE_WARNING = "Êtes-vous sûr de vouloir quitter cette page ? Le diagnostic n'a pas été sauvegardé."

export default {
  name: "DiagnosticEditor",
  data() {
    return {
      diagnostic: {},
      selectedCanteenId: undefined,
      bypassLeaveWarning: false,
      formIsValid: true,
    }
  },
  components: { InformationMeasure, WasteMeasure, DiversificationMeasure, NoPlasticMeasure, QualityMeasureValuesInput },
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
    userCanteens() {
      return this.$store.state.userCanteens
    },
    validators() {
      return {
        ...validators,
        diagnosticIsUnique: this.diagnosticIsUnique,
      }
    },
    originalDiagnostic() {
      if (!this.canteen) return {}
      return this.canteen.diagnostics.find((diagnostic) => diagnostic.year === parseInt(this.year))
    },
    diagnosticIsUnique() {
      if (!this.isNewDiagnostic) return true
      if (!this.selectedCanteenId || !this.diagnostic.year) return true

      const existingDiagnostic = this.userCanteens
        .find((x) => x.id === this.selectedCanteenId)
        .diagnostics.some((x) => x.year === this.diagnostic.year)

      return !existingDiagnostic
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
    hasChanged() {
      const diff = getObjectDiff(this.originalDiagnostic, this.diagnostic)
      return Object.keys(diff).length > 0
    },
  },
  beforeMount() {
    if (this.isNewDiagnostic) return

    if (!this.canteen) this.$router.replace({ name: "NotFound" })

    const diagnostic = this.originalDiagnostic
    if (diagnostic) this.diagnostic = JSON.parse(JSON.stringify(diagnostic))
    else this.$router.replace({ name: "NotFound" })
  },
  methods: {
    approSummary() {
      if (this.diagnostic.valueTotalHt > 0) {
        let summary = []
        if (this.diagnostic.valueBioHt) {
          summary.push(`${percentage(this.diagnostic.valueBioHt, this.diagnostic.valueTotalHt)} % bio`)
        }
        if (this.diagnostic.valueSustainableHt) {
          summary.push(
            `${percentage(this.diagnostic.valueSustainableHt, this.diagnostic.valueTotalHt)} % de qualité et durable`
          )
        }
        return summary.join(", ")
      }
    },
    plasticSummary() {
      let summary = []
      if (this.diagnostic.cookingPlasticSubstituted) summary.push("contenants de cuisson")
      if (this.diagnostic.servingPlasticSubstituted) summary.push("contenants de service")
      if (this.diagnostic.plasticBottlesSubstituted) summary.push("bouteilles")
      if (this.diagnostic.plasticTablewareSubstituted) summary.push("ustensils")
      if (summary.length === 0) summary.push("rien")
      summary = summary.join(", ") + " substitués"
      return summary.charAt(0).toUpperCase() + summary.slice(1)
    },
    saveDiagnostic() {
      this.$refs.form.validate()

      if (!this.formIsValid) {
        // TODO: how to nicely handle revealing validation issues in collapsed panels?
        this.$store.dispatch("notifyRequiredFieldsError")
        return
      }
      const payload = getObjectDiff(this.originalDiagnostic, this.diagnostic)
      this.$store
        .dispatch(this.isNewDiagnostic ? "createDiagnostic" : "updateDiagnostic", {
          id: this.diagnostic.id,
          canteenId: this.selectedCanteenId || this.canteen.id,
          payload,
        })
        .then(() => {
          this.bypassLeaveWarning = true
          this.$store.dispatch("notify", {
            title: "Mise à jour prise en compte",
            message: `Votre diagnostic a bien été ${this.isNewDiagnostic ? "créé" : "modifié"}`,
            status: "success",
          })
          this.$router.push({
            name: "ManagementPage",
          })
        })
        .catch(() => {
          this.$store.dispatch("notifyServerError")
        })
    },
    goToExistingDiagnostic() {
      this.bypassLeaveWarning = true
      const existingCanteen = this.userCanteens.find((x) => x.id === this.selectedCanteenId)
      const canteenUrlComponent = this.$store.getters.getCanteenUrlComponent(existingCanteen)
      const year = this.diagnostic.year
      this.$router.replace({ name: "DiagnosticModification", params: { canteenUrlComponent, year } })
    },
    handleUnload(e) {
      if (this.hasChanged && !this.bypassLeaveWarning) {
        e.preventDefault()
        e.returnValue = LEAVE_WARNING
      } else {
        delete e["returnValue"]
      }
    },
  },
  created() {
    window.addEventListener("beforeunload", this.handleUnload)
  },
  beforeDestroy() {
    window.removeEventListener("beforeunload", this.handleUnload)
  },
  beforeRouteLeave(to, from, next) {
    if (!this.hasChanged || this.bypassLeaveWarning) {
      next()
      return
    }
    window.confirm(LEAVE_WARNING) ? next() : next(false)
  },
}
</script>
