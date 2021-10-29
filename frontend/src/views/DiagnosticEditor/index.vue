<template>
  <div class="mt-n2">
    <v-row class="mt-2">
      <v-col cols="12" sm="4" md="3" v-if="canteen">
        <CanteenNavigation :canteen="canteen" />
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
        <div class="caption grey--text text--darken-1" v-else>
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
            heading="Au moins 50 % de produits de qualité et durables dont 20 % de bio"
            :summary="approSummary() || 'Incomplet'"
            :formIsValid="formIsValid.quality"
          >
            <v-form ref="quality" v-model="formIsValid.quality">
              <QualityMeasureValuesInput
                :originalDiagnostic="diagnostic"
                label="La valeur (en HT) de mes achats alimentaires..."
                :readonly="hasActiveTeledeclaration"
              />
              <fieldset class="d-flex flex-column mt-4">
                <legend class="body-2 mb-2">
                  Les valeurs par label des produits de qualité et durables hors bio (facultatif)
                </legend>
                <v-row>
                  <v-col cols="12" md="4" class="pr-0">
                    <label class="caption mb-1 mt-2">Label Rouge</label>
                    <v-container class="d-flex pa-0 pr-3 align-center right-border">
                      <img
                        src="/static/images/quality-labels/label-rouge.png"
                        alt=""
                        style="height: 2em;"
                        class="mr-2"
                      />
                      <v-text-field
                        hide-details="auto"
                        type="number"
                        suffix="€ HT"
                        :rules="[validators.nonNegativeOrEmpty]"
                        validate-on-blur
                        solo
                        dense
                        v-model.number="diagnostic.valueLabelRouge"
                        :readonly="hasActiveTeledeclaration"
                        :disabled="hasActiveTeledeclaration"
                      ></v-text-field>
                    </v-container>
                  </v-col>
                  <v-col cols="12" md="4" class="pr-0">
                    <label class="caption mb-1 mt-2">AOC / AOP / IGP</label>
                    <v-container class="d-flex pa-0 pr-3 align-center right-border">
                      <img
                        src="/static/images/quality-labels/Logo-AOC-AOP.png"
                        alt=""
                        style="height: 2em;"
                        class="mr-1"
                      />
                      <img src="/static/images/quality-labels/IGP.png" alt="" style="height: 2em;" class="mr-1" />
                      <v-text-field
                        hide-details="auto"
                        type="number"
                        suffix="€ HT"
                        :rules="[validators.nonNegativeOrEmpty]"
                        validate-on-blur
                        solo
                        dense
                        v-model.number="diagnostic.valueLabelAocIgp"
                        :readonly="hasActiveTeledeclaration"
                        :disabled="hasActiveTeledeclaration"
                      ></v-text-field>
                    </v-container>
                  </v-col>
                  <v-col cols="12" md="4">
                    <label class="caption mb-1 mt-2">Haute Valeur Environnementale</label>
                    <v-container class="d-flex pa-0 align-center">
                      <img src="/static/images/quality-labels/hve.png" alt="" style="height: 2em;" class="mr-2" />
                      <v-text-field
                        hide-details="auto"
                        type="number"
                        suffix="€ HT"
                        :rules="[validators.nonNegativeOrEmpty]"
                        validate-on-blur
                        solo
                        dense
                        v-model.number="diagnostic.valueLabelHve"
                        :readonly="hasActiveTeledeclaration"
                        :disabled="hasActiveTeledeclaration"
                      ></v-text-field>
                    </v-container>
                  </v-col>
                </v-row>
              </fieldset>
            </v-form>
          </DiagnosticExpansionPanel>

          <DiagnosticExpansionPanel
            iconColour="orange darken-2"
            icon="mdi-offer"
            heading="Lutte contre le gaspillage alimentaire et dons alimentaires"
            :formIsValid="formIsValid.waste"
          >
            <v-form ref="waste" v-model="formIsValid.waste">
              <WasteMeasure :diagnostic="diagnostic" :readonly="hasActiveTeledeclaration" :canteen="canteen" />
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
                :canteen="canteen"
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

        <div v-if="!hasActiveTeledeclaration && isTeledeclarationYear">
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
import CanteenNavigation from "@/components/CanteenNavigation"
import InformationMeasure from "@/components/KeyMeasureDiagnostic/InformationMeasure"
import WasteMeasure from "@/components/KeyMeasureDiagnostic/WasteMeasure"
import DiversificationMeasure from "@/components/KeyMeasureDiagnostic/DiversificationMeasure"
import NoPlasticMeasure from "@/components/KeyMeasureDiagnostic/NoPlasticMeasure"
import QualityMeasureValuesInput from "@/components/KeyMeasureDiagnostic/QualityMeasureValuesInput"
import DiagnosticExpansionPanel from "./DiagnosticExpansionPanel"
import TeledeclarationCancelDialog from "./TeledeclarationCancelDialog"
import { getObjectDiff, timeAgo, strictIsNaN, lastYear, diagnosticYears, getPercentage } from "@/utils"

const LEAVE_WARNING = "Voulez-vous vraiment quitter cette page ? Le diagnostic n'a pas été sauvegardé."

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
      teledeclarationFormIsValid: true,
      openedPanel: null,
      cancelDialog: false,
      teledeclarationYear: lastYear(),
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
    TeledeclarationCancelDialog,
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
      return [
        parseFloat(this.diagnostic.valueBioHt),
        parseFloat(this.diagnostic.valueSustainableHt),
        parseFloat(this.diagnostic.valueTotalHt),
      ].every((x) => !strictIsNaN(x))
    },
    hasActiveTeledeclaration() {
      return this.diagnostic.teledeclaration && this.diagnostic.teledeclaration.status === "SUBMITTED"
    },
    isTeledeclarationYear() {
      return this.diagnostic.year === this.teledeclarationYear
    },
  },
  beforeMount() {
    if (this.userCanteens.length === 1) {
      this.selectedCanteenId = this.userCanteens[0].id
    }
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
          summary.push(`${getPercentage(this.diagnostic.valueBioHt, this.diagnostic.valueTotalHt)} % bio`)
        }
        if (hasValue(this.diagnostic.valueSustainableHt)) {
          summary.push(
            `${getPercentage(this.diagnostic.valueSustainableHt, this.diagnostic.valueTotalHt)} % de qualité et durable`
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
      const diagnosticFormsAreValid = this.validateForms()

      if (!diagnosticFormsAreValid) {
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
          this.navigateToDiagnosticList()
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
    navigateToDiagnosticList() {
      let canteenUrlComponent = this.canteenUrlComponent
      if (!canteenUrlComponent && this.canteen) {
        canteenUrlComponent = this.$store.getters.getCanteenUrlComponent(this.canteen)
      } else if (!canteenUrlComponent) {
        let canteen = this.userCanteens.find((x) => x.id === this.canteenId)
        canteenUrlComponent = this.$store.getters.getCanteenUrlComponent(canteen)
      }
      this.$router.push({ name: "DiagnosticList", params: { canteenUrlComponent } })
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

        return this.$store.dispatch(this.isNewDiagnostic ? "createDiagnostic" : "updateDiagnostic", {
          id: this.diagnostic.id,
          canteenId: this.canteenId,
          payload,
        })
      }

      saveIfChanged()
        .then(() =>
          this.$store.dispatch("submitTeledeclaration", {
            id: this.diagnostic.id,
            canteenId: this.canteenId,
          })
        )
        .then(() => {
          this.bypassLeaveWarning = true
          this.$store.dispatch("notify", {
            title: "Télédéclaration prise en compte",
            status: "success",
          })
          this.navigateToDiagnosticList()
        })
        .catch(() => this.$store.dispatch("notifyServerError"))
    },
    cancelTeledeclaration() {
      return this.$store
        .dispatch("cancelTeledeclaration", {
          canteenId: this.canteenId,
          id: this.diagnostic.teledeclaration.id,
        })
        .then(() => {
          this.bypassLeaveWarning = true
          this.$store.dispatch("notify", {
            title: "Votre télédéclaration a bien été annulée",
          })
          this.navigateToDiagnosticList()
        })
        .catch(() => this.$store.dispatch("notifyServerError"))
    },
    timeAgo: timeAgo,
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

<style scoped>
#teledeclaration-form >>> .v-input--checkbox .v-label.theme--light {
  font-size: 16px;
  font-weight: bold;
  color: rgba(0, 0, 0, 0.87);
}
#teledeclaration-form >>> .v-input--checkbox .v-label.theme--light.v-label--is-disabled {
  color: rgba(0, 0, 0, 0.37);
}
fieldset {
  border: none;
}
.right-border {
  border-right: solid 1px #ccc;
}

@media (max-width: 960px) {
  .right-border {
    border-right: none;
  }
}
</style>
