<template>
  <div class="mt-n2">
    <TeledeclarationPreview
      v-if="diagnostic"
      :diagnostic="diagnostic"
      :canteen="originalCanteen"
      v-model="showTeledeclarationPreview"
      @teledeclare="submitTeledeclaration"
    />
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
            <v-col cols="12" md="3">
              <p class="body-2 my-2">Année</p>
              <DsfrSelect
                ref="yearSelect"
                v-model="diagnostic.year"
                :rules="[validators.required, validators.diagnosticIsUnique]"
                :items="allowedYears"
                hide-details="auto"
                placeholder="Année du diagnostic"
                v-if="isNewDiagnostic"
              />
              <div v-else class="text-h6 font-weight-bold">{{ diagnostic.year }}</div>
            </v-col>
            <v-col v-if="!diagnosticIsUnique" cols="12" class="ma-0 text-body-2 red--text">
              Un diagnostic pour cette cantine et cette année existe déjà.
              <v-btn small text class="text-decoration-underline text-body-2 mt-n1" @click="goToExistingDiagnostic">
                Modifier le diagnostic existant.
              </v-btn>
            </v-col>

            <div>
              <p
                v-if="
                  isTeledeclarationPhase && !hasActiveTeledeclaration && !canSubmitTeledeclaration && showApproPanel
                "
                class="text-caption ma-0 pl-4"
              >
                <v-icon small>mdi-information</v-icon>
                Vous pourrez télédéclarer ce diagnostic après avoir remplir les données d'approvisionnement
              </p>
              <p
                v-else-if="isTeledeclarationPhase && !hasActiveTeledeclaration && showExpansionPanels"
                class="text-body-2 pl-4 mb-0 d-md-flex align-center"
              >
                <v-icon small color="amber darken-3">mdi-alert</v-icon>
                &nbsp;Vous n'avez pas encore télédéclaré ce diagnostic -&nbsp;
                <a color="primary" href="#teledeclaration">
                  télédéclarez-le
                </a>
              </p>
              <div v-else-if="hasActiveTeledeclaration" class="px-2 mt-2">
                <p class="text-caption mb-2">
                  <v-icon small>$checkbox-fill</v-icon>
                  Ce diagnostic a été télédéclaré {{ timeAgo(diagnostic.teledeclaration.creationDate, true) }}.
                </p>
                <DownloadLink
                  :href="`/api/v1/teledeclaration/${diagnostic.teledeclaration.id}/document.pdf`"
                  label="Télécharger mon justificatif"
                  sizeStr="60 Ko"
                  target="_blank"
                />
              </div>
            </div>

            <v-col cols="12" class="mb-8 mt-3">
              <v-divider></v-divider>
            </v-col>
          </v-row>
        </v-form>

        <v-radio-group
          v-model="diagnostic.centralKitchenDiagnosticMode"
          :readonly="hasActiveTeledeclaration"
          :disabled="hasActiveTeledeclaration"
          class="mt-0"
          v-if="isCentralCanteen"
        >
          <v-radio v-for="type in centralKitchenDiagnosticModes" :key="type.key" :label="type.label" :value="type.key">
            <template v-slot:label>
              <span class="grey--text text--darken-3">{{ type.label }}</span>
            </template>
          </v-radio>
        </v-radio-group>

        <p class="body-2 grey--text text--darken-1" v-if="!hasActiveTeledeclaration && showExpansionPanels">
          Cliquez sur les catégories ci-dessous pour remplir votre diagnostic
        </p>
        <div class="body-2 grey--text text--darken-1" v-if="hasActiveTeledeclaration">
          <p class="mb-2">Une fois télédéclaré, vous ne pouvez plus modifier votre diagnostic.</p>
          <TeledeclarationCancelDialog
            v-model="cancelDialog"
            v-if="isTeledeclarationPhase"
            @cancel="cancelTeledeclaration"
            :diagnostic="diagnostic"
          />
        </div>

        <v-card v-if="dataDelegatedNotice" color="primary lighten-4" class="dsfr mb-6">
          <v-card-title class="font-weight-bold">{{ dataDelegatedNotice.title }}</v-card-title>
          <v-card-text>{{ dataDelegatedNotice.message }}</v-card-text>
        </v-card>

        <v-expansion-panels
          class="mb-8"
          :disabled="!diagnosticIsUnique"
          :value="openedPanel"
          v-if="showExpansionPanels"
        >
          <DiagnosticExpansionPanel
            iconColour="red"
            icon="mdi-food-apple"
            heading="Plus de produits de qualité et durables dans nos assiettes"
            :summary="approSummary() || 'Incomplet'"
            :formIsValid="formIsValid.quality"
            :disabled="!showApproPanel"
          >
            <v-form ref="quality" v-model="formIsValid.quality">
              <p>
                Suivant le niveau d'information disponible, vous pouvez choisir entre ces deux types de déclaration.
                Pour les achats des années 2021 et 2022, toutes les déclarations peuvent être remplies avec la "saisie
                simplifiée". Pour les données d'achats 2023, la "saisie simplifiée" sera accessible uniquement aux
                établissements de moins de 200 couverts/jour.
              </p>
              <v-radio-group
                v-model="diagnostic.diagnosticType"
                :readonly="hasActiveTeledeclaration"
                :disabled="hasActiveTeledeclaration"
              >
                <v-radio v-for="type in diagnosticTypes" :key="type.key" :label="type.label" :value="type.key">
                  <template v-slot:label>
                    <span class="grey--text text--darken-3 font-weight-bold">{{ type.label }}</span>
                    <span class="body-2 ml-3">{{ type.help }}</span>
                  </template>
                </v-radio>
              </v-radio-group>
              <div class="font-weight-bold mb-4">{{ diagnosticTypeLabel }}</div>
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
            :disabled="!showNonApproPanels"
          >
            <v-form ref="waste" v-model="formIsValid.waste">
              <WasteMeasure :diagnostic="diagnostic" :readonly="hasActiveTeledeclaration" :canteen="originalCanteen" />
            </v-form>
          </DiagnosticExpansionPanel>

          <DiagnosticExpansionPanel
            iconColour="green darken-1"
            icon="$leaf-fill"
            heading="Diversification des sources de protéines et menus végétariens"
            :formIsValid="formIsValid.diversification"
            :disabled="!showNonApproPanels"
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
            :disabled="!showNonApproPanels"
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
            :disabled="!showNonApproPanels"
          >
            <v-form ref="information" v-model="formIsValid.information">
              <InformationMeasure :diagnostic="diagnostic" :readonly="hasActiveTeledeclaration" />
            </v-form>
          </DiagnosticExpansionPanel>
        </v-expansion-panels>

        <p class="body-2 grey--text text--darken-1">
          Certaines informations liées à votre établissement seront incluses dans votre diagnostic. Merci de vérifier
          qu'elles sont à jour.
        </p>

        <v-expansion-panels
          class="mb-8"
          :disabled="!diagnosticIsUnique"
          :value="openedPanel"
          v-if="showExpansionPanels"
        >
          <DiagnosticExpansionPanel
            iconColour="purple"
            icon="$restaurant-fill"
            heading="Données relatives à mon établissement"
            :summary="'summary'"
            :formIsValid="formIsValid.canteen"
            :disabled="!showExpansionPanels"
          >
            <v-form ref="canteen" v-model="formIsValid.canteen">
              <CanteenPanel :originalCanteen="originalCanteen" />
            </v-form>
          </DiagnosticExpansionPanel>
        </v-expansion-panels>

        <div
          v-if="!hasActiveTeledeclaration && isTeledeclarationPhase && showExpansionPanels"
          class="mt-4"
          id="teledeclaration"
        >
          <h2 class="font-weight-black text-h5 mt-8 mb-4">Télédéclarer mon diagnostic</h2>
          <p>
            Un bilan statistique annuel de la mise en œuvre des obligations prévues par l’article L. 230-5-1 est établi
            par l’administration sur la base des éléments transmis, par les personnes morales de droit public et de
            droit privé mentionnées aux articles L. 230-5-1 et L. 230-5-2 (décret du 23 avril 2019). L’arrêté du 14
            septembre 2022 précise les modalités de transmission par les gestionnaires de restaurants collectifs des
            données nécessaires à l’établissement de ce bilan. Les informations saisies dans votre diagnostic 2022
            seront celles transmises à l’administration (DGAl, direction générale de l'alimentation du Ministère de
            l'agriculture MASA) en charge de l’élaboration de ce bilan.
          </p>
          <p>
            Nous vous proposons d’utiliser les informations de votre autodiagnostic {{ teledeclarationYear }} et de les
            transmettre, avec votre accord, à la DGAL, direction du Ministère de l'agriculture en charge de
            l'élaboration de ce bilan.
          </p>
        </div>

        <v-sheet rounded color="grey lighten-4" v-if="!hasActiveTeledeclaration && showExpansionPanels" class="pa-3">
          <div class="justify-md-end d-flex flex-column flex-md-row">
            <v-btn x-large outlined color="primary" class="ma-3" :to="{ name: 'ManagementPage' }">
              Annuler
            </v-btn>
            <v-btn
              x-large
              :outlined="isTeledeclarationPhase"
              color="primary"
              class="ma-3"
              @click="saveDiagnostic"
              :disabled="!diagnosticIsUnique"
            >
              Valider
            </v-btn>
            <v-btn
              x-large
              color="primary"
              class="ma-3"
              @click="openTeledeclarationPreview"
              :disabled="!canSubmitTeledeclaration"
              v-if="isTeledeclarationPhase"
            >
              <v-icon class="mr-2">$checkbox-circle-fill</v-icon>
              Valider et télédéclarer
            </v-btn>
          </div>
          <p
            class="text-caption amber--text text--darken-3 text-md-right mb-0 mx-3 mt-n1"
            v-if="isTeledeclarationPhase && !hasActiveTeledeclaration && !canSubmitTeledeclaration"
          >
            <v-icon small color="amber darken-3">mdi-alert</v-icon>
            Données d'approvisionnement manquantes.
            <span v-if="diagnostic.valueTotalHt === 0">
              Le total des achats doit être supérieur à zéro.
            </span>
          </p>
        </v-sheet>
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
import CanteenPanel from "./CanteenPanel"
import DownloadLink from "@/components/DownloadLink"
import DiagnosticExpansionPanel from "./DiagnosticExpansionPanel"
import TeledeclarationCancelDialog from "./TeledeclarationCancelDialog"
import SimplifiedQualityValues from "./SimplifiedQualityValues"
import ExtendedQualityValues from "./ExtendedQualityValues"
import TeledeclarationPreview from "@/components/TeledeclarationPreview"
import Constants from "@/constants"
import {
  getObjectDiff,
  timeAgo,
  strictIsNaN,
  lastYear,
  diagnosticYears,
  getPercentage,
  readCookie,
  capitalise,
} from "@/utils"
import DsfrSelect from "@/components/DsfrSelect"

const LEAVE_WARNING = "Voulez-vous vraiment quitter cette page ? Le diagnostic n'a pas été sauvegardé."

export default {
  name: "DiagnosticEditor",
  data() {
    const thisYear = new Date().getFullYear()
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
        canteen: true,
      },
      openedPanel: null,
      cancelDialog: false,
      teledeclarationYear: lastYear(),
      purchasesSummary: null,
      diagnosticTypes: [
        {
          key: "SIMPLE",
          label: "Télédéclaration - saisie simplifiée",
          help: "Vous connaissez les valeurs totaux, bio, et de qualité et durable",
        },
        {
          key: "COMPLETE",
          label: "Télédéclaration - saisie détaillée",
          help: "Vous connaissez les labels et les familles de produits de vos achats",
        },
      ],
      centralKitchenDiagnosticModes: [
        {
          key: "ALL",
          label: "Je rentre les données concernant toutes les mesures EGAlim pour mes cantines satellites",
        },
        {
          key: "APPRO",
          label: "Je rentre seulement les données d'approvisionnement pour mes cantines satellites",
        },
      ],
      showTeledeclarationPreview: false,
      allowedYears: diagnosticYears().map((year) => {
        return {
          text: year + (year >= thisYear ? " (prévisionnel)" : ""),
          value: year,
        }
      }),
    }
  },
  components: {
    InformationMeasure,
    WasteMeasure,
    DiversificationMeasure,
    NoPlasticMeasure,
    CanteenPanel,
    DiagnosticExpansionPanel,
    TeledeclarationCancelDialog,
    SimplifiedQualityValues,
    ExtendedQualityValues,
    TeledeclarationPreview,
    DownloadLink,
    DsfrSelect,
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
    hasChanged() {
      const diff = getObjectDiff(this.originalDiagnostic, this.diagnostic)
      return Object.keys(diff).length > 0
    },
    canSubmitTeledeclaration() {
      return !this.showApproPanel || this.diagnostic.valueTotalHt > 0
    },
    hasActiveTeledeclaration() {
      return this.diagnostic.teledeclaration && this.diagnostic.teledeclaration.status === "SUBMITTED"
    },
    isTeledeclarationPhase() {
      return window.ENABLE_TELEDECLARATION && this.diagnostic.year === this.teledeclarationYear
    },
    displayPurchaseHints() {
      return (
        this.purchasesSummary && Object.values(this.purchasesSummary).some((x) => !!x) && !this.hasActiveTeledeclaration
      )
    },
    diagnosticTypeLabel() {
      return this.diagnosticTypes.find((x) => x.key === this.diagnostic.diagnosticType).label
    },
    extendedDiagnostic() {
      return this.diagnostic.diagnosticType === "COMPLETE"
    },
    isCentralCanteen() {
      return (
        this.originalCanteen.productionType === "central_serving" || this.originalCanteen.productionType === "central"
      )
    },
    centralKitchenDiagostic() {
      if (this.diagnostic.year && this.originalCanteen?.centralKitchenDiagnostics)
        return this.originalCanteen.centralKitchenDiagnostics.find((x) => x.year === this.diagnostic.year)
      return null
    },
    showApproPanel() {
      if (this.originalCanteen.productionType === "site_cooked_elsewhere" && this.centralKitchenDiagostic) {
        return (
          this.centralKitchenDiagostic.centralKitchenDiagnosticMode !== "APPRO" &&
          this.centralKitchenDiagostic.centralKitchenDiagnosticMode !== "ALL"
        )
      }
      return true
    },
    showNonApproPanels() {
      if (this.originalCanteen.productionType === "site_cooked_elsewhere" && this.centralKitchenDiagostic)
        return this.centralKitchenDiagostic.centralKitchenDiagnosticMode !== "ALL"
      if (this.isCentralCanteen)
        return this.diagnostic.centralKitchenDiagnosticMode && this.diagnostic.centralKitchenDiagnosticMode !== "APPRO"
      return true
    },
    showExpansionPanels() {
      // can be false if all data is declared by the cuisine centrale
      return this.showApproPanel || this.showNonApproPanels
    },
    dataDelegatedNotice() {
      if (this.isCentralCanteen || this.showApproPanel) return null
      const centralKitchen = this.originalCanteen.centralKitchenName
        ? `« ${this.originalCanteen.centralKitchenName} »`
        : ""
      if (!this.showApproPanel && this.showNonApproPanels) {
        return {
          title: "Données d'approvisionnement déjà déclarées",
          message: `Votre cuisine centrale ${centralKitchen} avec le siret ${this.originalCanteen.centralProducerSiret} a déjà renseigné les
            données d'approvisionnement pour votre cantine. Les autres volets de la loi EGAlim vous restent accessibles.`,
        }
      }
      return {
        title: "Diagnostic déjà pris en compte par votre cuisine centrale",
        message: `Votre cuisine centrale ${centralKitchen} avec le siret ${this.originalCanteen.centralProducerSiret} a déjà rempli un
          diagnostic pour cette année pour votre cantine.`,
      }
    },
  },
  beforeMount() {
    this.refreshDiagnostic()
  },
  methods: {
    refreshDiagnostic() {
      const diagnostic = this.originalDiagnostic
      if (diagnostic) {
        this.$set(this, "diagnostic", JSON.parse(JSON.stringify(diagnostic)))
      } else this.$router.replace({ name: "NotFound" })
      const defaultDiagnosticType = this.showExtendedDiagnostic() ? "COMPLETE" : "SIMPLE"
      this.$set(this.diagnostic, "diagnosticType", this.diagnostic.diagnosticType || defaultDiagnosticType)
    },
    approTotals() {
      let bioTotal = this.diagnostic.valueBioHt
      let siqoTotal = this.diagnostic.valueSustainableHt
      let perfExtTotal = this.diagnostic.valueExternalityPerformanceHt
      let egalimOthersTotal = this.diagnostic.valueEgalimOthersHt
      if (this.extendedDiagnostic) {
        bioTotal = 0
        siqoTotal = 0
        perfExtTotal = 0
        egalimOthersTotal = 0
        const egalimFields = Constants.TeledeclarationCharacteristicGroups.egalim.fields
        egalimFields.forEach((field) => {
          const value = parseFloat(this.diagnostic[field])
          if (value) {
            if (field.endsWith("Bio")) {
              bioTotal += value
            } else if (!field.startsWith("valueLabel") && !field.endsWith("Ht")) {
              if (field.endsWith("LabelRouge") || field.endsWith("AocaopIgpStg")) {
                siqoTotal += value
              } else if (field.endsWith("Performance") || field.endsWith("Externalites")) {
                perfExtTotal += value
              } else {
                egalimOthersTotal += value
              }
            }
          }
        })
        bioTotal = +bioTotal.toFixed(2)
        siqoTotal = +siqoTotal.toFixed(2)
        perfExtTotal = +perfExtTotal.toFixed(2)
        egalimOthersTotal = +egalimOthersTotal.toFixed(2)
      }
      return {
        bioTotal,
        siqoTotal,
        perfExtTotal,
        egalimOthersTotal,
      }
    },
    meatPoultryTotals() {
      let meatPoultryEgalim = this.diagnostic.valueSustainableHt
      let meatPoultryFrance = this.diagnostic.valueExternalityPerformanceHt
      if (this.extendedDiagnostic) {
        meatPoultryEgalim = 0
        meatPoultryFrance = 0
        const egalimFields = Constants.TeledeclarationCharacteristicGroups.egalim.fields
        const outsideLawFields = Constants.TeledeclarationCharacteristicGroups.outsideLaw.fields
        const allFields = egalimFields.concat(outsideLawFields)

        allFields.forEach((field) => {
          const isMeatPoultry = field.includes("ViandesVolailles")
          const value = parseFloat(this.diagnostic[field])
          if (!isMeatPoultry || !value) return
          const isEgalim = egalimFields.includes(field)
          const isFrance = field.startsWith("value") && field.endsWith("France")

          // Note that it can be both egalim and provenance France
          if (isEgalim) meatPoultryEgalim += value
          if (isFrance) meatPoultryFrance += value
        })
        meatPoultryEgalim = +meatPoultryEgalim.toFixed(2)
        meatPoultryFrance = +meatPoultryFrance.toFixed(2)
      }
      return { meatPoultryEgalim, meatPoultryFrance }
    },
    fishTotals() {
      let fishEgalim = this.diagnostic.valueSustainableHt

      if (this.extendedDiagnostic) {
        fishEgalim = 0

        const egalimFields = Constants.TeledeclarationCharacteristicGroups.egalim.fields

        egalimFields.forEach((field) => {
          const isFish = field.includes("ProduitsDeLaMer")
          const value = parseFloat(this.diagnostic[field])
          if (!isFish || !value) return
          fishEgalim += value
        })
        fishEgalim = +fishEgalim.toFixed(2)
      }
      return { fishEgalim }
    },
    approSummary() {
      if (this.diagnostic.valueTotalHt > 0) {
        const { bioTotal, siqoTotal, perfExtTotal, egalimOthersTotal } = this.approTotals()
        const qualityTotal = (siqoTotal || 0) + (perfExtTotal || 0) + (egalimOthersTotal || 0)
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
      return capitalise(summary)
    },
    saveDiagnostic() {
      const diagnosticFormsAreValid = this.validateForms()

      if (!diagnosticFormsAreValid) {
        this.$store.dispatch("notifyRequiredFieldsError")
        this.openedPanel = Object.values(this.formIsValid).findIndex((isValid) => !isValid)
        return
      }

      // save to the diagnostic the simplified values if extended diagnostic used
      this.populateSimplifiedDiagnostic()

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
    populateSimplifiedDiagnostic() {
      if (!this.extendedDiagnostic) return
      const { bioTotal, siqoTotal, perfExtTotal, egalimOthersTotal } = this.approTotals()
      this.diagnostic.valueBioHt = bioTotal
      this.diagnostic.valueSustainableHt = siqoTotal
      this.diagnostic.valueExternalityPerformanceHt = perfExtTotal
      this.diagnostic.valueEgalimOthersHt = egalimOthersTotal

      const { meatPoultryEgalim, meatPoultryFrance } = this.meatPoultryTotals()
      this.diagnostic.valueMeatPoultryEgalimHt = meatPoultryEgalim
      this.diagnostic.valueMeatPoultryFranceHt = meatPoultryFrance

      const { fishEgalim } = this.fishTotals()
      this.diagnostic.valueFishEgalimHt = fishEgalim
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
    openTeledeclarationPreview() {
      const diagnosticFormsAreValid = this.validateForms()
      if (!diagnosticFormsAreValid) return this.$store.dispatch("notifyRequiredFieldsError")
      this.showTeledeclarationPreview = true
    },
    submitTeledeclaration() {
      const diagnosticFormsAreValid = this.validateForms()
      const payload = getObjectDiff(this.originalDiagnostic, this.diagnostic)

      if (!diagnosticFormsAreValid) return this.$store.dispatch("notifyRequiredFieldsError")

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
        .catch((e) => {
          this.$store.dispatch("notifyServerError", e)
        })
        .finally(() => {
          this.openTeledeclarationPreview = false
        })
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

        // We should not manually change the `year` parameter since it is populated by the router,
        // so when we create a diagnostic we need to ask the router to take us to that new diagnostic
        // in order to refresh the data
        this.bypassLeaveWarning = true
        this.$router.replace({
          name: "DiagnosticModification",
          params: { canteenUrlComponent: this.canteenUrlComponent, year: diagnostic.year },
        })
        this.bypassLeaveWarning = false
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
      const characteristicGroups = Constants.TeledeclarationCharacteristicGroups
      return (
        characteristicGroups.egalim.fields.some((key) => !!this.originalDiagnostic[key]) ||
        characteristicGroups.outsideLaw.fields.some((key) => !!this.originalDiagnostic[key])
      )
    },
  },
  created() {
    window.addEventListener("beforeunload", this.handleUnload)
  },
  mounted() {
    if (!this.diagnostic.year) {
      const suggestedYear = Number(this.$route.query.année)
      if (suggestedYear && this.allowedYears.find((y) => y.value === suggestedYear)) {
        this.diagnostic.year = suggestedYear
      }
    }
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
