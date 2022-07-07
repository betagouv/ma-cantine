<template>
  <div class="mt-n2">
    <v-row class="mt-2">
      <v-col class="text-left pb-10">
        <h1 class="font-weight-black text-h4 mb-4 mt-1">
          {{ isNewDiagnostic ? "Nouveau diagnostic" : "Modifier mon diagnostic" }}
        </h1>

        <v-form ref="select" v-model="formIsValid.select">
          <v-row>
            <v-col cols="12" md="5">
              <p class="body-2 my-2">Cantine</p>
              <div class="text-h6 font-weight-bold">{{ originalCanteen.name }}</div>
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

            <div v-if="isTeledeclarationYear">
              <p v-if="!hasActiveTeledeclaration && !canSubmitTeledeclaration" class="text-caption ma-0 pl-4">
                <v-icon small>mdi-information-outline</v-icon>
                Vous pourrez télédéclarer ce diagnostic après avoir remplir les données d'approvisionnement
              </p>
              <p v-else-if="!hasActiveTeledeclaration" class="text-caption ma-0 pl-4">
                <v-icon small>mdi-information</v-icon>
                Vous n'avez pas encore télédéclaré ce diagnostic
              </p>
              <div v-else class="px-2 mt-2">
                <p class="text-caption mb-2">
                  <v-icon small>mdi-check-circle</v-icon>
                  Ce diagnostic a été télédéclaré {{ timeAgo(diagnostic.teledeclaration.creationDate, true) }}.
                </p>
                <v-btn
                  large
                  color="primary"
                  :href="`/api/v1/teledeclaration/${diagnostic.teledeclaration.id}/document.pdf`"
                >
                  <v-icon class="mr-2">mdi-file-download</v-icon>
                  Télécharger mon justificatif
                </v-btn>
              </div>
            </div>

            <v-col cols="12" class="mb-8 mt-3">
              <v-divider></v-divider>
            </v-col>
          </v-row>
        </v-form>

        <p class="caption grey--text text--darken-1" v-if="!hasActiveTeledeclaration">
          Cliquez sur les catégories ci-dessous pour remplir votre diagnostic
        </p>
        <div class="caption grey--text text--darken-1" v-if="hasActiveTeledeclaration">
          <p class="mb-0">Une fois télédéclaré, vous ne pouvez plus modifier votre diagnostic.</p>
          <TeledeclarationCancelDialog
            v-model="cancelDialog"
            @cancel="cancelTeledeclaration"
            :diagnostic="diagnostic"
          />
        </div>

        <v-expansion-panels class="mb-8" :disabled="!diagnosticIsUnique" :value="openedPanel">
          <DiagnosticExpansionPanel
            iconColour="red"
            icon="mdi-food-apple"
            heading="Plus de produits de qualité et durables dans nos assiettes"
            :summary="approSummary() || 'Incomplet'"
            :formIsValid="formIsValid.quality"
          >
            <v-form ref="quality" v-model="formIsValid.quality">
              <v-switch v-model="extendedDiagnostic" label="Activer la déclaration complète" />
              <div class="font-weight-bold mb-4">{{ diagnosticType }}</div>
              <SimplifiedQualityValues
                :originalDiagnostic="diagnostic"
                :readonly="hasActiveTeledeclaration"
                :purchasesSummary="purchasesSummary"
                v-if="!extendedDiagnostic"
              />
              <ExtendedQualityValues
                :originalDiagnostic="diagnostic"
                :readonly="hasActiveTeledeclaration"
                :purchasesSummary="purchasesSummary"
                v-else
                class="mb-4"
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
              <WasteMeasure :diagnostic="diagnostic" :readonly="hasActiveTeledeclaration" :canteen="originalCanteen" />
            </v-form>
          </DiagnosticExpansionPanel>

          <DiagnosticExpansionPanel
            iconColour="green darken-1"
            icon="mdi-leaf"
            heading="Diversification des sources de protéines et menus végétariens"
            :formIsValid="formIsValid.diversification"
          >
            <v-form ref="diversification" v-model="formIsValid.diversification">
              <DiversificationMeasure
                :diagnostic="diagnostic"
                :readonly="hasActiveTeledeclaration"
                :canteen="originalCanteen"
              />
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
              <NoPlasticMeasure :diagnostic="diagnostic" :readonly="hasActiveTeledeclaration" />
            </v-form>
          </DiagnosticExpansionPanel>

          <DiagnosticExpansionPanel
            iconColour="amber darken-2"
            icon="mdi-bullhorn"
            heading="Information des usagers et convives"
            :formIsValid="formIsValid.information"
          >
            <v-form ref="information" v-model="formIsValid.information">
              <InformationMeasure :diagnostic="diagnostic" :readonly="hasActiveTeledeclaration" />
            </v-form>
          </DiagnosticExpansionPanel>
        </v-expansion-panels>

        <v-sheet rounded color="grey lighten-4 pa-3" v-if="!hasActiveTeledeclaration" class="d-flex">
          <v-spacer></v-spacer>
          <v-btn x-large outlined color="primary" class="mr-4 align-self-center" :to="{ name: 'ManagementPage' }">
            Annuler
          </v-btn>
          <v-btn x-large color="primary" @click="saveDiagnostic" :disabled="!diagnosticIsUnique">
            Valider
          </v-btn>
        </v-sheet>

        <div v-if="!hasActiveTeledeclaration && isTeledeclarationYear && originalCanteen.productionType !== 'central'">
          <v-divider class="mt-8"></v-divider>
          <h2 class="font-weight-black text-h5 mt-8 mb-4">Télédéclarer mon diagnostic</h2>
          <p>
            Un bilan annuel relatif à la mise en œuvre des dispositions de la loi EGAlim, et notamment des objectifs
            d'approvisionnement en produits de qualité et durables dont bio dans les repas servis dans les restaurants
            collectifs, est prévu par le décret du 23 avril 2019.
          </p>
          <p>
            Nous vous proposons d’utiliser les informations de votre autodiagnostic {{ teledeclarationYear }} et de les
            transmettre, avec votre accord, à la DGAL, direction du Ministère de l'agriculture en charge de
            l'élaboration de ce bilan.
          </p>
          <v-form ref="teledeclarationForm" v-model="teledeclarationFormIsValid" id="teledeclaration-form">
            <v-checkbox
              :rules="[validators.checked]"
              label="Je déclare sur l’honneur la véracité de mes informations"
              :disabled="!canSubmitTeledeclaration"
            ></v-checkbox>
          </v-form>
          <v-sheet rounded color="white" class="d-flex">
            <v-spacer></v-spacer>
            <v-btn x-large color="primary" @click="submitTeledeclaration" :disabled="!canSubmitTeledeclaration">
              <v-icon class="mr-2">mdi-cloud-upload</v-icon>
              Télédéclarer mon diagnostic
            </v-btn>
          </v-sheet>
          <p
            v-if="!diagnostic.teledeclaration && !canSubmitTeledeclaration"
            class="text-caption mt-2 mb-0 text-right amber--text text--darken-3"
          >
            <v-icon small color="amber darken-3">mdi-alert</v-icon>
            Données d'approvisionnement manquantes
          </p>
        </div>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import validators from "@/validators"
import InformationMeasure from "@/components/KeyMeasureDiagnostic/InformationMeasure"
import WasteMeasure from "@/components/KeyMeasureDiagnostic/WasteMeasure"
import DiversificationMeasure from "@/components/KeyMeasureDiagnostic/DiversificationMeasure"
import NoPlasticMeasure from "@/components/KeyMeasureDiagnostic/NoPlasticMeasure"
import DiagnosticExpansionPanel from "./DiagnosticExpansionPanel"
import TeledeclarationCancelDialog from "./TeledeclarationCancelDialog"
import SimplifiedQualityValues from "./SimplifiedQualityValues"
import ExtendedQualityValues from "./ExtendedQualityValues"
import Constants from "@/constants"
import { getObjectDiff, timeAgo, strictIsNaN, lastYear, diagnosticYears, getPercentage, readCookie } from "@/utils"

const LEAVE_WARNING = "Voulez-vous vraiment quitter cette page ? Le diagnostic n'a pas été sauvegardé."

export default {
  name: "DiagnosticEditor",
  data() {
    return {
      diagnostic: {},
      bypassLeaveWarning: false,
      formIsValid: {
        quality: true,
        waste: true,
        plastic: true,
        diversification: true,
        information: true,
        select: true,
      },
      teledeclarationFormIsValid: true,
      openedPanel: null,
      cancelDialog: false,
      teledeclarationYear: lastYear(),
      purchasesSummary: null,
      extendedDiagnostic: false,
    }
  },
  components: {
    InformationMeasure,
    WasteMeasure,
    DiversificationMeasure,
    NoPlasticMeasure,
    DiagnosticExpansionPanel,
    TeledeclarationCancelDialog,
    SimplifiedQualityValues,
    ExtendedQualityValues,
  },
  props: {
    canteenUrlComponent: {
      type: String,
      required: true,
    },
    originalCanteen: {
      type: Object,
      required: true,
    },
    year: {
      required: false,
    },
  },
  computed: {
    isNewDiagnostic() {
      return !this.year
    },
    canteenId() {
      return this.originalCanteen.id
    },
    validators() {
      return {
        ...validators,
        diagnosticIsUnique: this.diagnosticIsUnique,
      }
    },
    originalDiagnostic() {
      if (this.isNewDiagnostic) return {}
      return this.originalCanteen.diagnostics.find((diagnostic) => diagnostic.year === parseInt(this.year))
    },
    diagnosticIsUnique() {
      if (!this.isNewDiagnostic || !this.diagnostic.year) return true
      const existingDiagnostic = this.originalCanteen.diagnostics.some((x) => x.year === this.diagnostic.year)
      return !existingDiagnostic
    },
    allowedYears() {
      const thisYear = new Date().getFullYear()
      return diagnosticYears().map((year) => {
        return {
          text: year + (year >= thisYear ? " (prévisionnel)" : ""),
          value: year,
        }
      })
    },
    hasChanged() {
      const diff = getObjectDiff(this.originalDiagnostic, this.diagnostic)
      return Object.keys(diff).length > 0
    },
    canSubmitTeledeclaration() {
      const { bioTotal, qualityTotal } = this.approTotals()
      return [parseFloat(bioTotal), parseFloat(qualityTotal), parseFloat(this.diagnostic.valueTotalHt)].every(
        (x) => !strictIsNaN(x)
      )
    },
    hasActiveTeledeclaration() {
      return this.diagnostic.teledeclaration && this.diagnostic.teledeclaration.status === "SUBMITTED"
    },
    isTeledeclarationYear() {
      return this.diagnostic.year === this.teledeclarationYear
    },
    displayPurchaseHints() {
      return (
        this.purchasesSummary && Object.values(this.purchasesSummary).some((x) => !!x) && !this.hasActiveTeledeclaration
      )
    },
    diagnosticType() {
      return this.extendedDiagnostic ? "Déclaration complète" : "Déclaration simplifiée"
    },
  },
  beforeMount() {
    this.refreshDiagnostic()
    this.extendedDiagnostic = this.showExtendedDiagnostic()
  },
  methods: {
    refreshDiagnostic() {
      const diagnostic = this.originalDiagnostic
      if (diagnostic) this.diagnostic = JSON.parse(JSON.stringify(diagnostic))
      else this.$router.replace({ name: "NotFound" })
    },
    approTotals() {
      let bioTotal = this.diagnostic.valueBioHt
      let qualityTotal = this.diagnostic.valueSustainableHt
      if (this.extendedDiagnostic) {
        bioTotal = 0
        qualityTotal = 0
        Object.keys(this.diagnostic).forEach((key) => {
          if (key.startsWith("value")) {
            const value = parseFloat(this.diagnostic[key])
            if (value) {
              if (key.endsWith("Bio")) {
                bioTotal += value
              } else if (!key.startsWith("valueLabel") && !key.endsWith("Ht")) {
                qualityTotal += value
              }
            }
          }
        })
      }
      return {
        bioTotal,
        qualityTotal,
      }
    },
    approSummary() {
      if (this.diagnostic.valueTotalHt > 0) {
        const { bioTotal, qualityTotal } = this.approTotals()
        let summary = []
        if (hasValue(bioTotal)) {
          summary.push(`${getPercentage(bioTotal, this.diagnostic.valueTotalHt)} % bio`)
        }
        if (hasValue(qualityTotal)) {
          summary.push(`${getPercentage(qualityTotal, this.diagnostic.valueTotalHt)} % de qualité et durable`)
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
      const diagnosticFormsAreValid = this.validateForms()

      if (!diagnosticFormsAreValid) {
        this.$store.dispatch("notifyRequiredFieldsError")
        this.openedPanel = Object.values(this.formIsValid).findIndex((isValid) => !isValid)
        return
      }
      // save to the diagnostic the aggregations of bio and quality if extended diagnostic used
      const { bioTotal, qualityTotal } = this.approTotals()
      this.diagnostic.valueBioHt = bioTotal
      this.diagnostic.valueSustainableHt = qualityTotal

      const payload = getObjectDiff(this.originalDiagnostic, this.diagnostic)

      if (this.isNewDiagnostic) {
        for (let i = 0; i < Constants.TrackingParams.length; i++) {
          const cookieValue = readCookie(Constants.TrackingParams[i])
          if (cookieValue) payload[`creation_${Constants.TrackingParams[i]}`] = cookieValue
        }
      }

      this.$store
        .dispatch(this.isNewDiagnostic ? "createDiagnostic" : "updateDiagnostic", {
          id: this.diagnostic.id,
          canteenId: this.canteenId,
          payload,
        })
        .then((diagnostic) => {
          this.bypassLeaveWarning = true
          this.$store.dispatch("notify", {
            title: "Mise à jour prise en compte",
            message: `Votre diagnostic a bien été ${this.isNewDiagnostic ? "créé" : "modifié"}`,
            status: "success",
          })
          this.updateFromServer(diagnostic)
          this.navigateToDiagnosticList()
        })
        .catch((e) => {
          this.$store.dispatch("notifyServerError", e)
        })
    },
    goToExistingDiagnostic() {
      this.bypassLeaveWarning = true
      const canteenUrlComponent = this.canteenUrlComponent
      const year = this.diagnostic.year
      this.$router.replace({ name: "DiagnosticModification", params: { canteenUrlComponent, year } })
    },
    navigateToDiagnosticList() {
      this.$router.push({ name: "DiagnosticList", params: { canteenUrlComponent: this.canteenUrlComponent } })
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
    submitTeledeclaration() {
      const diagnosticFormsAreValid = this.validateForms()
      const teledeclarationFormIsValid = this.$refs["teledeclarationForm"].validate()
      const payload = getObjectDiff(this.originalDiagnostic, this.diagnostic)

      if (!diagnosticFormsAreValid) return this.$store.dispatch("notifyRequiredFieldsError")

      if (!teledeclarationFormIsValid) return

      const saveIfChanged = () => {
        if (!this.hasChanged) return Promise.resolve()

        return this.$store
          .dispatch(this.isNewDiagnostic ? "createDiagnostic" : "updateDiagnostic", {
            id: this.diagnostic.id,
            canteenId: this.canteenId,
            payload,
          })
          .then((diagnostic) => {
            this.updateFromServer(diagnostic)
            this.$router.push({ name: "DiagnosticList", params: { canteenUrlComponent: this.canteenUrlComponent } })
          })
      }

      saveIfChanged()
        .then(() =>
          this.$store.dispatch("submitTeledeclaration", {
            id: this.diagnostic.id,
            canteenId: this.canteenId,
          })
        )
        .then((diagnostic) => {
          this.bypassLeaveWarning = true
          this.$store.dispatch("notify", {
            title: "Télédéclaration prise en compte",
            status: "success",
          })
          this.updateFromServer(diagnostic)
          this.navigateToDiagnosticList()
        })
        .catch((e) => this.$store.dispatch("notifyServerError", e))
    },
    cancelTeledeclaration() {
      return this.$store
        .dispatch("cancelTeledeclaration", {
          canteenId: this.canteenId,
          id: this.diagnostic.teledeclaration.id,
        })
        .then((diagnostic) => {
          this.bypassLeaveWarning = true
          this.$store.dispatch("notify", {
            title: "Votre télédéclaration a bien été annulée",
          })
          this.updateFromServer(diagnostic)
          this.navigateToDiagnosticList()
        })
        .catch((e) => this.$store.dispatch("notifyServerError", e))
    },
    updateFromServer(diagnostic) {
      if (this.isNewDiagnostic) {
        this.originalCanteen.diagnostics.push(diagnostic)
      } else {
        const diagnosticIndex = this.originalCanteen.diagnostics.findIndex((x) => x.id === diagnostic.id)
        if (diagnosticIndex > -1) this.originalCanteen.diagnostics.splice(diagnosticIndex, 1, diagnostic)
      }
    },
    timeAgo: timeAgo,
    fetchPurchasesSummary() {
      if (this.canteenId && this.diagnostic && this.diagnostic.year)
        fetch(`/api/v1/canteenPurchasesSummary/${this.canteenId}?year=${this.diagnostic.year}`)
          .then((response) => (response.ok ? response.json() : {}))
          .then((response) => (this.purchasesSummary = response))
    },
    showExtendedDiagnostic() {
      return Constants.TeledeclarationValuesKeys.some((key) => !!this.originalDiagnostic[key])
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
  watch: {
    year() {
      this.refreshDiagnostic()
    },
    "diagnostic.year": function() {
      this.fetchPurchasesSummary()
    },
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

<style scoped>
#teledeclaration-form >>> .v-input--checkbox .v-label.theme--light {
  font-size: 16px;
  font-weight: bold;
  color: rgba(0, 0, 0, 0.87);
}
#teledeclaration-form >>> .v-input--checkbox .v-label.theme--light.v-label--is-disabled {
  color: rgba(0, 0, 0, 0.37);
}
</style>
