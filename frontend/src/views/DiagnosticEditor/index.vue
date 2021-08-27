<template>
  <div>
    <v-row class="mt-2">
      <v-col cols="12" sm="4" md="3" v-if="canteen">
        <CanteenNavigation :canteen="canteen" />
        <!-- TODO: add general navigation if no canteen -->
      </v-col>
      <v-col class="text-left pb-10">
        <h1 class="font-weight-black text-h4 my-4">
          {{ isNewDiagnostic ? "Nouveau diagnostic" : "Modifier mon diagnostic" }}
        </h1>
        <v-form ref="select" v-model="formIsValid.select">
          <v-row>
            <v-col cols="12" md="5">
              <p class="body-2 my-2">Cantine</p>
              <v-select
                solo
                ref="canteenSelect"
                v-model="selectedCanteenId"
                :rules="[validators.required, validators.diagnosticIsUnique]"
                :items="userCanteens"
                item-text="name"
                item-value="id"
                hide-details="auto"
                placeholder="Choisissez votre cantine"
                v-if="!canteen"
              ></v-select>
              <div v-else class="text-h6 font-weight-bold">{{ canteen.name }}</div>
            </v-col>
            <v-col cols="12" md="4">
              <p class="body-2 my-2">Année</p>
              <v-select
                solo
                ref="yearSelect"
                v-model="diagnostic.year"
                :rules="[validators.required, validators.diagnosticIsUnique]"
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
        </v-form>

        <p class="caption grey--text text--darken-1">
          Cliquez sur les catégories ci-dessous pour remplir votre diagnostic
        </p>

        <v-expansion-panels class="mb-8" :disabled="!diagnosticIsUnique" :value="openedPanel">
          <DiagnosticExpansionPanel
            iconColour="red"
            icon="mdi-food-apple"
            heading="Au moins 50% de produits de qualité et durables dont 20% de bio"
            :summary="approSummary() || 'Incomplet'"
            :formIsValid="formIsValid.quality"
          >
            <v-form ref="quality" v-model="formIsValid.quality">
              <QualityMeasureValuesInput
                :originalDiagnostic="diagnostic"
                label="La valeur (en HT) de mes achats alimentaires..."
              />
            </v-form>
          </DiagnosticExpansionPanel>

          <DiagnosticExpansionPanel
            iconColour="orange darken-2"
            icon="mdi-offer"
            heading="Lutte contre le gaspillage alimentaire et dons alimentaires"
            :formIsValid="formIsValid.waste"
          >
            <v-form ref="waste" v-model="formIsValid.waste">
              <WasteMeasure :diagnostic="diagnostic" />
            </v-form>
          </DiagnosticExpansionPanel>

          <DiagnosticExpansionPanel
            iconColour="green darken-1"
            icon="mdi-leaf"
            heading="Diversification des sources de protéines et menus végétariens"
            :formIsValid="formIsValid.diversification"
          >
            <v-form ref="diversification" v-model="formIsValid.diversification">
              <DiversificationMeasure :diagnostic="diagnostic" />
            </v-form>
          </DiagnosticExpansionPanel>

          <DiagnosticExpansionPanel
            iconColour="blue darken-1"
            icon="mdi-weather-windy"
            heading="Substitution des plastiques"
            :summary="plasticSummary()"
            :formIsValid="formIsValid.plastic"
          >
            <v-form ref="plastic" v-model="formIsValid.plastic">
              <NoPlasticMeasure :diagnostic="diagnostic" />
            </v-form>
          </DiagnosticExpansionPanel>

          <DiagnosticExpansionPanel
            iconColour="amber darken-2"
            icon="mdi-bullhorn"
            heading="Information des usagers et convives"
            :formIsValid="formIsValid.information"
          >
            <v-form ref="information" v-model="formIsValid.information">
              <InformationMeasure :diagnostic="diagnostic" />
            </v-form>
          </DiagnosticExpansionPanel>
        </v-expansion-panels>

        <v-sheet rounded color="grey lighten-4 pa-3" class="d-flex">
          <v-spacer></v-spacer>
          <v-btn x-large outlined color="primary" class="mr-4 align-self-center" :to="{ name: 'ManagementPage' }">
            Annuler
          </v-btn>
          <v-btn x-large color="primary" @click="saveDiagnostic" :disabled="!diagnosticIsUnique">
            Valider
          </v-btn>
        </v-sheet>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import validators from "@/validators"
import CanteenNavigation from "@/components/CanteenNavigation"
import InformationMeasure from "@/components/KeyMeasureDiagnostic/InformationMeasure"
import WasteMeasure from "@/components/KeyMeasureDiagnostic/WasteMeasure"
import DiversificationMeasure from "@/components/KeyMeasureDiagnostic/DiversificationMeasure"
import NoPlasticMeasure from "@/components/KeyMeasureDiagnostic/NoPlasticMeasure"
import QualityMeasureValuesInput from "@/components/KeyMeasureDiagnostic/QualityMeasureValuesInput"
import DiagnosticExpansionPanel from "./DiagnosticExpansionPanel"
import { getObjectDiff, strictIsNaN } from "@/utils"

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
      formIsValid: {
        quality: true,
        waste: true,
        plastic: true,
        diversification: true,
        information: true,
        select: true,
      },
      openedPanel: null,
    }
  },
  components: {
    CanteenNavigation,
    InformationMeasure,
    WasteMeasure,
    DiversificationMeasure,
    NoPlasticMeasure,
    QualityMeasureValuesInput,
    DiagnosticExpansionPanel,
  },
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
      return !this.year
    },
    canteen() {
      if (!this.canteenUrlComponent) return null
      return this.$store.getters.getCanteenFromUrlComponent(this.canteenUrlComponent)
    },
    canteenId() {
      return this.selectedCanteenId || this.canteen?.id
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
      if (this.isNewDiagnostic) return {}
      return this.canteen.diagnostics.find((diagnostic) => diagnostic.year === parseInt(this.year))
    },
    diagnosticIsUnique() {
      if (!this.isNewDiagnostic) return true
      if (!this.canteenId || !this.diagnostic.year) return true

      const existingDiagnostic = this.userCanteens
        .find((x) => x.id === this.canteenId)
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
        if (hasValue(this.diagnostic.valueBioHt)) {
          summary.push(`${percentage(this.diagnostic.valueBioHt, this.diagnostic.valueTotalHt)} % bio`)
        }
        if (hasValue(this.diagnostic.valueSustainableHt)) {
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
      if (summary.length === 0) return "Pas de mesures de substitution"
      summary = summary.join(", ") + " substitués"
      return summary.charAt(0).toUpperCase() + summary.slice(1)
    },
    saveDiagnostic() {
      const allFormsAreValid = this.validateForms()

      if (!allFormsAreValid) {
        this.$store.dispatch("notifyRequiredFieldsError")
        this.openedPanel = Object.values(this.formIsValid).findIndex((isValid) => !isValid)
        return
      }
      const payload = getObjectDiff(this.originalDiagnostic, this.diagnostic)
      this.$store
        .dispatch(this.isNewDiagnostic ? "createDiagnostic" : "updateDiagnostic", {
          id: this.diagnostic.id,
          canteenId: this.canteenId,
          payload,
        })
        .then(() => {
          this.bypassLeaveWarning = true
          this.$store.dispatch("notify", {
            title: "Mise à jour prise en compte",
            message: `Votre diagnostic a bien été ${this.isNewDiagnostic ? "créé" : "modifié"}`,
            status: "success",
          })
          let canteenUrlComponent = this.canteenUrlComponent
          if (!canteenUrlComponent && this.canteen) {
            canteenUrlComponent = this.$store.getters.getCanteenUrlComponent(this.canteen)
          } else if (!canteenUrlComponent) {
            let canteen = this.userCanteens.find((x) => x.id === this.canteenId)
            canteenUrlComponent = this.$store.getters.getCanteenUrlComponent(canteen)
          }
          this.$router.push({ name: "DiagnosticList", params: { canteenUrlComponent } })
        })
        .catch(() => {
          this.$store.dispatch("notifyServerError")
        })
    },
    goToExistingDiagnostic() {
      this.bypassLeaveWarning = true
      const existingCanteen = this.userCanteens.find((x) => x.id === this.canteenId)
      const canteenUrlComponent = this.$store.getters.getCanteenUrlComponent(existingCanteen)
      const year = this.diagnostic.year
      this.$router.replace({ name: "DiagnosticModification", params: { canteenUrlComponent, year } })
    },
    validateForms() {
      const refs = this.$refs
      Object.keys(this.formIsValid).forEach((ref) => refs[ref] && refs[ref].validate())
      return Object.values(this.formIsValid).every((isValid) => isValid)
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

function hasValue(val) {
  if (typeof val === "string") {
    return !!val
  } else {
    return !strictIsNaN(val)
  }
}
</script>
