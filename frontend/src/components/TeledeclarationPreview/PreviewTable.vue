<template>
  <!-- TODO: can the scrolling be replaced by https://v2.vuetifyjs.com/en/components/dialogs/#scrollable -->
  <v-card-text ref="innerTable" class="my-4 py-0" style="overflow-y: scroll; border: solid 1px #9b9b9b;">
    <v-simple-table ref="innerSimpleTable" dense class="my-0 py-0">
      <template v-slot:default>
        <thead>
          <tr>
            <th style="height: 0;" class="text-left"></th>
            <th style="height: 0;" class="text-left"></th>
          </tr>
        </thead>
        <tbody>
          <tr class="header">
            <td class="text-left font-weight-bold" colspan="2">
              Données relatives à votre établissement
            </td>
          </tr>
          <tr v-for="item in canteenItems" :key="item.label">
            <td class="text-left">{{ item.label }}</td>
            <td
              :class="item.isNumber ? 'text-right' : 'text-left'"
              :width="$vuetify.breakpoint.smAndUp ? '42%' : '50%'"
            >
              {{ item.value }}
            </td>
          </tr>
          <tr v-if="centralKitchenDiagnosticModeDisplay">
            <td class="text-left font-weight-bold" colspan="2">{{ centralKitchenDiagnosticModeDisplay }}</td>
          </tr>
          <tr class="header">
            <td class="text-left font-weight-bold" v-if="showApproItems">
              Saisie de données d'approvisionnement :
              {{ diagnostic.diagnosticType === "COMPLETE" ? "Détaillée" : "Simple" }}
            </td>
            <td class="text-left grey--text text--darken-3" colspan="2" v-if="showApproItems">
              {{ approSummary }}
            </td>
            <td class="text-left font-weight-bold" v-else colspan="2">
              Données d'approvisonnement renseignées par la cuisine centrale
            </td>
          </tr>
          <tr
            v-for="item in approItems"
            :key="item.param"
            :class="isTruthyOrZero(diagnostic[item.param]) ? '' : 'warn'"
          >
            <td class="text-left">{{ item.label }}</td>
            <td :class="isTruthyOrZero(diagnostic[item.param]) ? 'text-right' : 'text-left'">
              {{
                isTruthyOrZero(diagnostic[item.param]) ? `${toCurrency(diagnostic[item.param])} HT` : "Je ne sais pas"
              }}
            </td>
          </tr>
          <tr class="header">
            <td class="text-left font-weight-bold" colspan="2">
              Autres données EGalim
            </td>
          </tr>
          <tr v-for="item in additionalItems" :key="item.label" :class="item.class || ''">
            <td class="text-left">{{ item.label }}</td>
            <td :class="item.isNumber && isTruthyOrZero(item.value) ? 'text-right' : 'text-left'">
              {{ isTruthyOrZero(item.value) ? item.value : "Non renseigné" }}
            </td>
          </tr>
        </tbody>
      </template>
    </v-simple-table>
  </v-card-text>
</template>

<script>
import Constants from "@/constants"
import communicationSupports from "@/data/communication-supports.json"
import {
  sectorDisplayString,
  sectorsSelectList,
  approSummary,
  toCurrency,
  selectListToObject,
  formatDate,
  formatNumber,
} from "@/utils"

export default {
  props: {
    diagnostic: {
      required: true,
    },
    canteen: {
      required: true,
    },
  },
  data() {
    return {
      wasteMeasurements: [],
    }
  },
  mounted() {
    this.fetchWasteMeasurements()
  },
  computed: {
    centralKitchenDiagostic() {
      if (this.diagnostic.year && this.canteen.centralKitchenDiagnostics)
        return this.canteen.centralKitchenDiagnostics.find((x) => x.year === this.diagnostic.year)
      return null
    },
    showApproItems() {
      if (this.canteen.productionType === "site_cooked_elsewhere" && this.centralKitchenDiagostic) {
        return (
          this.centralKitchenDiagostic.centralKitchenDiagnosticMode !== "APPRO" &&
          this.centralKitchenDiagostic.centralKitchenDiagnosticMode !== "ALL"
        )
      }
      return true
    },
    showAdditionalItems() {
      const isSatellite = this.canteen.productionType === "site_cooked_elsewhere"

      if (isSatellite) {
        const centralKitchenDeclaresAll = this.centralKitchenDiagostic?.centralKitchenDiagnosticMode === "ALL"
        return !centralKitchenDeclaresAll
      } else if (this.canteen.isCentralCuisine) {
        const onlyDeclaresApproData = this.diagnostic.centralKitchenDiagnosticMode === "APPRO"
        return !onlyDeclaresApproData
      }

      return true
    },
    canteenItems() {
      const productionTypeDetail = Constants.ProductionTypesDetailed.find(
        (x) => x.value === this.canteen.productionType
      )
      const managementTypeDetail = Constants.ManagementTypes.find((x) => x.value === this.canteen.managementType)
      const economicModelDetail = Constants.EconomicModels.find((x) => x.value === this.canteen.economicModel)
      const ministryDetail = this.$store.state.lineMinistries.find((x) => x.value === this.canteen.lineMinistry)
      let items = [
        { value: this.canteen.name, label: "Nom de la cantine" },
        { value: this.canteen.siret || "inconnu", label: "Numéro SIRET" },
        { value: this.canteen.sirenUniteLegale, label: "Numéro SIREN de l'unité légale" },
        { value: this.canteen.city, label: "Ville" },
        { value: economicModelDetail ? economicModelDetail.text : "", label: "Modèle économique" },
        { value: managementTypeDetail ? managementTypeDetail.text : "", label: "Mode de gestion" },
        { value: productionTypeDetail ? productionTypeDetail.body : "", label: "Type de production" },
      ]
      if (this.usesCentralProducer)
        items.push({ value: this.canteen.centralProducerSiret, label: "SIRET de la cuisine centrale" })
      if (this.showSatelliteCanteensCount)
        items.push({
          value: this.canteen.satelliteCanteensCount,
          label: "Nombre de cantines à qui je fournis des repas",
          isNumber: true,
        })
      items.push({ value: this.canteen.dailyMealCount, label: "Nombre moyen de couverts par jour", isNumber: true })
      items.push({ value: this.canteen.yearlyMealCount, label: "Nombre total de couverts par an", isNumber: true })
      if (this.showSectors) items.push({ value: this.sectors, label: "Secteurs d'activité" })
      if (this.showMinistryField)
        items.push({
          value: ministryDetail ? ministryDetail.text : "",
          label: "Administration générale de tutelle (ministère ou ATE)",
        })
      return items
    },
    approItems() {
      if (!this.showApproItems) return []
      if (this.diagnostic.diagnosticType === "COMPLETE") {
        return [
          { param: "valueTotalHt", label: "Mes achats alimentaires total" },
          {
            param: "valueMeatPoultryHt",
            label: "Mes achats en viandes et volailles fraiches ou surgelées total",
          },
          { param: "valueFishHt", label: "Mes achats en poissons, produits de la mer et de l'aquaculture total" },
          { param: "valueViandesVolaillesBio", label: "Mes achats viandes et volailles Bio" },
          {
            param: "valueProduitsDeLaMerBio",
            label: "Mes achats poissons, produits de la mer et de l'aquaculture Bio",
          },
          { param: "valueFruitsEtLegumesBio", label: "Mes achats fruits et legumes Bio" },
          { param: "valueCharcuterieBio", label: "Mes achats charcuterie Bio" },
          { param: "valueProduitsLaitiersBio", label: "Mes achats produits laitiers Bio" },
          { param: "valueBoulangerieBio", label: "Mes achats boulangerie Bio" },
          { param: "valueBoissonsBio", label: "Mes achats boissons Bio" },
          { param: "valueAutresBio", label: "Mes autres achats Bio" },
          { param: "valueViandesVolaillesLabelRouge", label: "Mes achats viandes et volailles Label Rouge" },
          {
            param: "valueProduitsDeLaMerLabelRouge",
            label: "Mes achats poissons, produits de la mer et de l'aquaculture Label Rouge",
          },
          { param: "valueFruitsEtLegumesLabelRouge", label: "Mes achats fruits et legumes Label Rouge" },
          { param: "valueCharcuterieLabelRouge", label: "Mes achats charcuterie Label Rouge" },
          { param: "valueProduitsLaitiersLabelRouge", label: "Mes achats produits laitiers Label Rouge" },
          { param: "valueBoulangerieLabelRouge", label: "Mes achats boulangerie Label Rouge" },
          { param: "valueBoissonsLabelRouge", label: "Mes achats boissons Label Rouge" },
          { param: "valueAutresLabelRouge", label: "Mes autres achats Label Rouge" },
          {
            param: "valueViandesVolaillesAocaopIgpStg",
            label: "Mes achats viandes et volailles AOC / AOP, IGP ou STG",
          },
          {
            param: "valueProduitsDeLaMerAocaopIgpStg",
            label: "Mes achats poissons, produits de la mer et de l'aquaculture AOC / AOP, IGP ou STG",
          },
          { param: "valueFruitsEtLegumesAocaopIgpStg", label: "Mes achats fruits et legumes AOC / AOP, IGP ou STG" },
          { param: "valueCharcuterieAocaopIgpStg", label: "Mes achats charcuterie AOC / AOP, IGP ou STG" },
          { param: "valueProduitsLaitiersAocaopIgpStg", label: "Mes achats produits laitiers AOC / AOP, IGP ou STG" },
          { param: "valueBoulangerieAocaopIgpStg", label: "Mes achats boulangerie AOC / AOP, IGP ou STG" },
          { param: "valueBoissonsAocaopIgpStg", label: "Mes achats boissons AOC / AOP, IGP ou STG" },
          { param: "valueAutresAocaopIgpStg", label: "Mes autres achats AOC / AOP, IGP ou STG" },
          {
            param: "valueViandesVolaillesHve",
            label: "Mes achats viandes et volailles Certification Environnementale de Niveau 2 ou HVE",
          },
          {
            param: "valueProduitsDeLaMerHve",
            label:
              "Mes achats poissons, produits de la mer et de l'aquaculture Certification Environnementale de Niveau 2 ou HVE",
          },
          {
            param: "valueFruitsEtLegumesHve",
            label: "Mes achats fruits et legumes Certification Environnementale de Niveau 2 ou HVE",
          },
          {
            param: "valueCharcuterieHve",
            label: "Mes achats charcuterie Certification Environnementale de Niveau 2 ou HVE",
          },
          {
            param: "valueProduitsLaitiersHve",
            label: "Mes achats produits laitiers Certification Environnementale de Niveau 2 ou HVE",
          },
          {
            param: "valueBoulangerieHve",
            label: "Mes achats boulangerie Certification Environnementale de Niveau 2 ou HVE",
          },
          { param: "valueBoissonsHve", label: "Mes achats boissons Certification Environnementale de Niveau 2 ou HVE" },
          { param: "valueAutresHve", label: "Mes autres achats Certification Environnementale de Niveau 2 ou HVE" },
          { param: "valueViandesVolaillesPecheDurable", label: "Mes achats viandes et volailles Peche Durable" },
          {
            param: "valueProduitsDeLaMerPecheDurable",
            label: "Mes achats poissons, produits de la mer et de l'aquaculture Peche Durable",
          },
          { param: "valueFruitsEtLegumesPecheDurable", label: "Mes achats fruits et legumes Pêche Durable" },
          { param: "valueCharcuteriePecheDurable", label: "Mes achats charcuterie Pêche Durable" },
          { param: "valueProduitsLaitiersPecheDurable", label: "Mes achats produits laitiers Pêche Durable" },
          { param: "valueBoulangeriePecheDurable", label: "Mes achats boulangerie Pêche Durable" },
          { param: "valueBoissonsPecheDurable", label: "Mes achats boissons Pêche Durable" },
          { param: "valueAutresPecheDurable", label: "Mes autres achats Pêche Durable" },
          { param: "valueViandesVolaillesRup", label: "Mes achats viandes et volailles RUP" },
          {
            param: "valueProduitsDeLaMerRup",
            label: "Mes achats poissons, produits de la mer et de l'aquaculture RUP",
          },
          { param: "valueFruitsEtLegumesRup", label: "Mes achats fruits et legumes RUP" },
          { param: "valueCharcuterieRup", label: "Mes achats charcuterie RUP" },
          { param: "valueProduitsLaitiersRup", label: "Mes achats produits laitiers RUP" },
          { param: "valueBoulangerieRup", label: "Mes achats boulangerie RUP" },
          { param: "valueBoissonsRup", label: "Mes achats boissons RUP" },
          { param: "valueAutresRup", label: "Mes autres achats RUP" },
          { param: "valueViandesVolaillesFermier", label: "Mes achats viandes et volailles Fermier" },
          {
            param: "valueProduitsDeLaMerFermier",
            label: "Mes achats poissons, produits de la mer et de l'aquaculture Fermier",
          },
          { param: "valueFruitsEtLegumesFermier", label: "Mes achats fruits et legumes Fermier" },
          { param: "valueCharcuterieFermier", label: "Mes achats charcuterie Fermier" },
          { param: "valueProduitsLaitiersFermier", label: "Mes achats produits laitiers Fermier" },
          { param: "valueBoulangerieFermier", label: "Mes achats boulangerie Fermier" },
          { param: "valueBoissonsFermier", label: "Mes achats boissons Fermier" },
          { param: "valueAutresFermier", label: "Mes autres achats Fermier" },
          {
            param: "valueViandesVolaillesExternalites",
            label: "Mes achats viandes et volailles Externalités Environnementales",
          },
          {
            param: "valueProduitsDeLaMerExternalites",
            label: "Mes achats poissons, produits de la mer et de l'aquaculture Externalités Environnementales",
          },
          {
            param: "valueFruitsEtLegumesExternalites",
            label: "Mes achats fruits et legumes Externalités Environnementales",
          },
          { param: "valueCharcuterieExternalites", label: "Mes achats charcuterie Externalités Environnementales" },
          {
            param: "valueProduitsLaitiersExternalites",
            label: "Mes achats produits laitiers Externalités Environnementales",
          },
          { param: "valueBoulangerieExternalites", label: "Mes achats boulangerie Externalités Environnementales" },
          { param: "valueBoissonsExternalites", label: "Mes achats boissons Externalités Environnementales" },
          { param: "valueAutresExternalites", label: "Mes autres achats Externalités Environnementales" },
          {
            param: "valueViandesVolaillesCommerceEquitable",
            label: "Mes achats viandes et volailles Commerce Équitable",
          },
          {
            param: "valueProduitsDeLaMerCommerceEquitable",
            label: "Mes achats poissons, produits de la mer et de l'aquaculture Commerce Équitable",
          },
          { param: "valueFruitsEtLegumesCommerceEquitable", label: "Mes achats fruits et legumes Commerce Équitable" },
          { param: "valueCharcuterieCommerceEquitable", label: "Mes achats charcuterie Commerce Équitable" },
          { param: "valueProduitsLaitiersCommerceEquitable", label: "Mes achats produits laitiers Commerce Équitable" },
          { param: "valueBoulangerieCommerceEquitable", label: "Mes achats boulangerie Commerce Équitable" },
          { param: "valueBoissonsCommerceEquitable", label: "Mes achats boissons Commerce Équitable" },
          { param: "valueAutresCommerceEquitable", label: "Mes autres achats Commerce Équitable" },
          {
            param: "valueViandesVolaillesPerformance",
            label: "Mes achats viandes et volailles Performance Environnementale",
          },
          {
            param: "valueProduitsDeLaMerPerformance",
            label: "Mes achats poissons, produits de la mer et de l'aquaculture Performance Environnementale",
          },
          {
            param: "valueFruitsEtLegumesPerformance",
            label: "Mes achats fruits et legumes Performance Environnementale",
          },
          { param: "valueCharcuteriePerformance", label: "Mes achats charcuterie Performance Environnementale" },
          {
            param: "valueProduitsLaitiersPerformance",
            label: "Mes achats produits laitiers Performance Environnementale",
          },
          { param: "valueBoulangeriePerformance", label: "Mes achats boulangerie Performance Environnementale" },
          { param: "valueBoissonsPerformance", label: "Mes achats boissons Performance Environnementale" },
          { param: "valueAutresPerformance", label: "Mes autres achats Performance Environnementale" },
          {
            param: "valueViandesVolaillesNonEgalim",
            label: "Mes achats viandes et volailles non-EGalim",
          },
          {
            param: "valueProduitsDeLaMerNonEgalim",
            label: "Mes achats poissons, produits de la mer et de l'aquaculture non-EGalim",
          },
          {
            param: "valueFruitsEtLegumesNonEgalim",
            label: "Mes achats fruits et legumes non-EGalim",
          },
          { param: "valueCharcuterieNonEgalim", label: "Mes achats charcuterie non-EGalim" },
          {
            param: "valueProduitsLaitiersNonEgalim",
            label: "Mes achats produits laitiers non-EGalim",
          },
          { param: "valueBoulangerieNonEgalim", label: "Mes achats boulangerie non-EGalim" },
          { param: "valueBoissonsNonEgalim", label: "Mes achats boissons non-EGalim" },
          { param: "valueAutresNonEgalim", label: "Mes autres achats non-EGalim" },

          { param: "valueViandesVolaillesFrance", label: "Mes achats viandes et volailles provenance France" },
          {
            param: "valueProduitsDeLaMerFrance",
            label: "Mes achats poissons, produits de la mer et de l'aquaculture provenance France",
          },
          { param: "valueFruitsEtLegumesFrance", label: "Mes achats fruits et legumes provenance France" },
          { param: "valueCharcuterieFrance", label: "Mes achats charcuterie provenance France" },
          { param: "valueProduitsLaitiersFrance", label: "Mes achats produits laitiers provenance France" },
          { param: "valueBoulangerieFrance", label: "Mes achats boulangerie provenance France" },
          { param: "valueBoissonsFrance", label: "Mes achats boissons provenance France" },
          { param: "valueAutresFrance", label: "Mes autres achats provenance France" },
          { param: "valueViandesVolaillesShortDistribution", label: "Mes achats viandes et volailles circuit-court" },
          {
            param: "valueProduitsDeLaMerShortDistribution",
            label: "Mes achats poissons, produits de la mer et de l'aquaculture circuit-court",
          },
          { param: "valueFruitsEtLegumesShortDistribution", label: "Mes achats fruits et legumes circuit-court" },
          { param: "valueCharcuterieShortDistribution", label: "Mes achats charcuterie circuit-court" },
          { param: "valueProduitsLaitiersShortDistribution", label: "Mes achats produits laitiers circuit-court" },
          { param: "valueBoulangerieShortDistribution", label: "Mes achats boulangerie circuit-court" },
          { param: "valueBoissonsShortDistribution", label: "Mes achats boissons circuit-court" },
          { param: "valueAutresShortDistribution", label: "Mes autres achats circuit-court" },
          { param: "valueViandesVolaillesLocal", label: "Mes achats viandes et volailles Local" },
          {
            param: "valueProduitsDeLaMerLocal",
            label: "Mes achats poissons, produits de la mer et de l'aquaculture Local",
          },
          { param: "valueFruitsEtLegumesLocal", label: "Mes achats fruits et legumes Local" },
          { param: "valueCharcuterieLocal", label: "Mes achats charcuterie Local" },
          { param: "valueProduitsLaitiersLocal", label: "Mes achats produits laitiers Local" },
          { param: "valueBoulangerieLocal", label: "Mes achats boulangerie Local" },
          { param: "valueBoissonsLocal", label: "Mes achats boissons Local" },
          { param: "valueAutresLocal", label: "Mes autres achats Local" },
        ]
      }
      return [
        { param: "valueTotalHt", label: "Mes achats alimentaires total" },
        { param: "valueBioHt", label: "Mes achats Bio ou en conversion Bio" },
        { param: "valueSustainableHt", label: "Mes achats SIQO (Label Rouge, AOC / AOP, IGP, STG)" },
        {
          param: "valueExternalityPerformanceHt",
          label:
            "Mes achats prenant en compte les coûts imputés aux externalités environnementales ou acquis sur la base de leurs performances en matière environnementale",
        },
        { param: "valueEgalimOthersHt", label: "Autres achats EGalim" },
        {
          param: "valueMeatPoultryHt",
          label: "Mes achats en viandes et volailles fraiches ou surgelées total",
        },
        {
          param: "valueMeatPoultryEgalimHt",
          label: "Mes achats EGalim en viandes et volailles fraiches ou surgelées",
        },
        {
          param: "valueMeatPoultryFranceHt",
          label: "Mes achats provenance France en viandes et volailles fraiches ou surgelées",
        },
        { param: "valueFishHt", label: "Mes achats en poissons, produits de la mer et de l'aquaculture total" },
        {
          param: "valueFishEgalimHt",
          label: "Mes achats EGalim en poissons, produits de la mer et de l'aquaculture",
        },
      ]
    },
    additionalItems() {
      if (!this.showAdditionalItems) return []

      const diversificationPlanActions = this.getDiversificationPlanActions(this.diagnostic.diversificationPlanActions)
      const vegetarianWeeklyRecurrence = this.getVegetarianWeeklyRecurrence(this.diagnostic.vegetarianWeeklyRecurrence)
      const vegetarianMenuType = this.getVegetarianMenuType(this.diagnostic.vegetarianMenuType)
      const vegetarianMenuBases = this.getVegetarianMenuBases(this.diagnostic.vegetarianMenuBases)
      const communicationFrequency = this.getCommunicationFrequency(this.diagnostic.communicationFrequency)

      const beforeWasteMeasurements = [
        {
          label: "Diagnostic sur le gaspillage alimentaire réalisé",
          value: this.getNullableBooleanLabel(this.diagnostic.hasWasteDiagnostic),
          class: this.diagnostic.hasWasteDiagnostic === null ? "warn" : "",
        },
        // TODO: this question only asked if hasWasteDiagnostic
        {
          label: "Plan d'action contre le gaspillage en place",
          value: this.getNullableBooleanLabel(this.diagnostic.hasWastePlan),
          class: this.diagnostic.hasWastePlan === null ? "warn" : "",
        },
        {
          label: "Réalisé des mesures de gaspillage alimentaire",
          value: this.getNullableBooleanLabel(this.diagnostic.hasWasteMeasures),
          class: this.diagnostic.hasWasteMeasures === null ? "warn" : "",
        },
      ]

      const wasteMeasurements = []
      for (let i = 0; i < this.wasteMeasurements.length; i++) {
        const waste = this.wasteMeasurements[i]
        const total = formatNumber(waste.totalMass)
        const label = `Mesure du ${formatDate(waste.periodStartDate)} - ${formatDate(waste.periodEndDate)}`

        let value = `Total ${total}kg`
        if (waste.isSortedBySource) {
          const leftovers = formatNumber(waste.leftoversTotalMass)
          const unserved = formatNumber(waste.unservedTotalMass)
          const preparation = formatNumber(waste.preparationTotalMass)
          value += ` : reste assiette ${leftovers}kg, denrées présentées aux convives mais non servies ${unserved}kg, déchets alimentaires issus de la préparation ${preparation}kg`
        }
        wasteMeasurements.push({ label, value })
      }

      const afterWasteMeasurements = [
        {
          label: "Actions contre le gaspillage en place",
          value: this.getWasteActions(this.diagnostic.wasteActions),
        },
        {
          label: "Autres actions contre le gaspillage alimentaire",
          value: this.diagnostic.otherWasteActions || "Aucune",
        },
        // TODO: this question is only shown if applicable to canteen
        {
          label: "Propose des dons alimentaires",
          value: this.getNullableBooleanLabel(this.diagnostic.hasDonationAgreement),
          class: this.diagnostic.hasDonationAgreement === null ? "warn" : "",
        },
        // TODO: the next few questions only shown if hasDonationAgreement && applicable
        {
          label: "Fréquence de dons en dons/an",
          isNumber: true,
          value: this.diagnostic.donationFrequency,
          class: this.isTruthyOrZero(this.diagnostic.donationFrequency) ? "" : "warn",
        },
        {
          label: "Quantité des denrées données kg/an",
          isNumber: true,
          value: this.diagnostic.donationQuantity,
          class: this.isTruthyOrZero(this.diagnostic.donationQuantity) ? "" : "warn",
        },
        {
          label: "Type de denrées données",
          value: this.diagnostic.donationFoodType,
          class: this.isTruthyOrZero(this.diagnostic.donationFoodType) ? "" : "warn",
        },
        {
          label: "Autres commentaires sur le gaspillage",
          value: this.diagnostic.otherWasteComments || "Aucun",
        },
        {
          label: "Plan de diversification de protéines en place",
          value: this.getNullableBooleanLabel(this.diagnostic.hasDiversificationPlan),
          class: this.diagnostic.hasDiversificationPlan === null ? "warn" : "",
        },
        {
          label: "Actions incluses dans le plan de diversification des protéines",
          value: diversificationPlanActions,
          class: diversificationPlanActions === "Non renseigné" ? "warn" : "",
        },
        {
          label: "Menus végétariens par semaine",
          value: vegetarianWeeklyRecurrence,
          class: vegetarianWeeklyRecurrence === "Non renseigné" ? "warn" : "",
        },
        {
          label: "Menu végétarien proposé",
          value: vegetarianMenuType,
          class: vegetarianMenuType === "Non renseigné" ? "warn" : "",
        },
        {
          label: "Bases du menu végétarien",
          value: vegetarianMenuBases,
          class: vegetarianMenuBases === "Non renseigné" ? "warn" : "",
        },
        {
          label: "Contenants de cuisson en plastique remplacés",
          value: this.getNullableBooleanLabel(this.diagnostic.cookingPlasticSubstituted),
          class: this.diagnostic.cookingPlasticSubstituted === null ? "warn" : "",
        },
        {
          label: "Contenants de service en plastique remplacés",
          value: this.getNullableBooleanLabel(this.diagnostic.servingPlasticSubstituted),
          class: this.diagnostic.servingPlasticSubstituted === null ? "warn" : "",
        },
        {
          label: "Bouteilles en plastique remplacées",
          value: this.getNullableBooleanLabel(this.diagnostic.plasticBottlesSubstituted),
          class: this.diagnostic.plasticBottlesSubstituted === null ? "warn" : "",
        },
        {
          label: "Ustensils en plastique remplacés",
          value: this.getNullableBooleanLabel(this.diagnostic.plasticTablewareSubstituted),
          class: this.diagnostic.plasticTablewareSubstituted === null ? "warn" : "",
        },
        {
          label: "Supports de communication utilisés",
          value: this.getCommunicationSupports(this.diagnostic.communicationSupports),
        },
        {
          label: "Autres supports de communication",
          value: this.diagnostic.otherCommunicationSupport,
          class: this.diagnostic.otherCommunicationSupport ? "" : "warn",
        },
        {
          label: "Lien (URL) de communication",
          value: this.diagnostic.communicationSupportUrl || "Aucun",
        },
        {
          label: "Communique sur le plan alimentaire",
          value: this.getNullableBooleanLabel(this.diagnostic.communicatesOnFoodPlan),
          class: this.diagnostic.communicatesOnFoodPlan === null ? "warn" : "",
        },
        {
          label: "Communique sur les démarches qualité/durables/équitables",
          value: this.getNullableBooleanLabel(this.diagnostic.communicatesOnFoodQuality),
          class: this.diagnostic.communicatesOnFoodQuality === null ? "warn" : "",
        },
        {
          label: "Fréquence de communication",
          value: communicationFrequency,
          class: communicationFrequency === "Non renseigné" ? "warn" : "",
        },
      ]

      return [...beforeWasteMeasurements, ...wasteMeasurements, ...afterWasteMeasurements]
    },
    sectors() {
      return sectorDisplayString(this.canteen.sectors, this.$store.state.sectors)
    },
    usesCentralProducer() {
      return this.canteen.productionType === "site_cooked_elsewhere"
    },
    showSectors() {
      return this.canteen.productionType !== "central"
    },
    showSatelliteCanteensCount() {
      return this.canteen.productionType === "central" || this.canteen.productionType === "central_serving"
    },
    showMinistryField() {
      const sectors = sectorsSelectList(this.$store.state.sectors)
      const concernedSectors = sectors.filter((x) => !!x.hasLineMinistry).map((x) => x.id)
      if (concernedSectors.length === 0) return false
      return this.canteen.sectors.some((x) => concernedSectors.indexOf(x) > -1)
    },
    approSummary() {
      return approSummary(this.diagnostic)
    },
    centralKitchenDiagnosticModeDisplay() {
      if (this.diagnostic.centralKitchenDiagnosticMode) {
        const mode = Constants.CentralKitchenDiagnosticModes.find(
          (mode) => mode.key === this.diagnostic.centralKitchenDiagnosticMode
        )
        return mode?.label
      }
      return null
    },
    year() {
      return this.diagnostic.year
    },
  },
  methods: {
    getWasteActions(wasteActions) {
      if (!wasteActions || !wasteActions.length) return "Aucune"
      const actionItems = {
        INSCRIPTION: "Pré-inscription des convives obligatoire",
        AWARENESS: "Sensibilisation par affichage ou autre média",
        TRAINING: "Formation / information du personnel de restauration",
        DISTRIBUTION: "Réorganisation de la distribution des composantes du repas",
        PORTIONS: "Choix des portions (grande faim, petite faim)",
        REUSE: "Réutilisation des restes de préparation / surplus",
      }
      const actionLabels = wasteActions.map((x) => actionItems[x]).filter((x) => !!x)
      return actionLabels.join(", ")
    },
    getDiversificationPlanActions(diversificationPlanActions) {
      if (!diversificationPlanActions || !diversificationPlanActions.length) return "Non renseigné"
      const actionItems = selectListToObject(Constants.DiversificationMeasureStep.diversificationPlanActions.items)
      const labels = diversificationPlanActions.map((x) => actionItems[x]).filter((x) => !!x)
      return labels.join(", ")
    },
    getVegetarianWeeklyRecurrence(vegetarianWeeklyRecurrence) {
      if (!vegetarianWeeklyRecurrence) return "Non renseigné"
      const items = selectListToObject(Constants.DiversificationMeasureStep.vegetarianWeeklyRecurrence.items)
      return items[vegetarianWeeklyRecurrence] || "Non renseigné"
    },
    getVegetarianMenuType(vegetarianMenuType) {
      if (this.diagnostic.vegetarianWeeklyRecurrence === "NEVER") return "Non applicable"
      if (!vegetarianMenuType) return "Non renseigné"
      const items = selectListToObject(Constants.DiversificationMeasureStep.vegetarianMenuType.items)
      return items[vegetarianMenuType] || "Non renseigné"
    },
    getVegetarianMenuBases(vegetarianMenuBases) {
      if (this.diagnostic.vegetarianWeeklyRecurrence === "NEVER") return "Non applicable"
      if (!vegetarianMenuBases || !vegetarianMenuBases.length) return "Non renseigné"
      const actionItems = selectListToObject(Constants.DiversificationMeasureStep.vegetarianMenuBases.items)
      const labels = vegetarianMenuBases.map((x) => actionItems[x]).filter((x) => !!x)
      return labels.join(", ")
    },
    getCommunicationSupports(supports) {
      if (!supports || !supports.length) return "Aucun"
      const labels = supports.map((x) => communicationSupports[x]).filter((x) => !!x)
      return labels.join(", ")
    },
    getCommunicationFrequency(communicationFrequency) {
      if (!communicationFrequency) return "Non renseigné"
      const items = selectListToObject(Constants.CommunicationFrequencies)
      return items[communicationFrequency] || "Non renseigné"
    },
    isTruthyOrZero(value) {
      return !!value || value === 0
    },
    getNullableBooleanLabel(value) {
      if (value === null) return "Non renseigné"
      return value ? "Oui" : "Non"
    },
    toCurrency(value) {
      return toCurrency(value)
    },
    fetchWasteMeasurements() {
      if (!this.diagnostic.hasWasteMeasures) return
      const query = `period_start_date_after=${this.year}-01-01&period_end_date_before=${this.year + 1}-01-01`
      fetch(`/api/v1/canteens/${this.canteen.id}/wasteMeasurements?${query}`)
        .then((response) => response.json())
        .then((response) => {
          this.wasteMeasurements = response
        })
    },
  },
}
</script>

<style scoped>
.v-data-table >>> table {
  border-collapse: collapse;
}
tr:hover {
  background-color: transparent !important;
}
tr.warn,
tr.warn:hover {
  background: #fff6da !important;
}
tr.header,
tr.header:hover {
  background: #f0f0f0 !important;
  border-bottom: solid 1px #c8c8c8;
  border-top: solid 1px #e6e6e6;
}
</style>
