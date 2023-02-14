<template>
  <v-dialog v-model="isOpen" max-width="750">
    <v-card ref="content">
      <v-card-title class="font-weight-bold">
        {{ canteen ? "Télédéclaration : " + canteen.name : "Votre télédéclaration" }}
      </v-card-title>
      <v-card-text class="text-left pb-0">
        Veuillez vérifier les données pour {{ diagnostic.year }} ci-dessous.
      </v-card-text>
      <v-card-text ref="table" class="my-4 py-0" style="overflow-y: scroll; border: solid 1px #9b9b9b;">
        <v-simple-table ref="innerSimpleTable" dense class="my-0 py-0">
          <template v-slot:default>
            <thead>
              <tr>
                <th style="height: 0;" class="text-left"></th>
                <th style="height: 0; min-width: 150px;" class="text-left"></th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td class="text-left font-weight-bold">
                  Données relatives à votre établissement
                </td>
                <td class="text-left font-weight-bold"></td>
              </tr>
              <tr v-for="item in canteenItems" :key="item.label">
                <td class="text-left">{{ item.label }}</td>
                <td :class="item.isNumber ? 'text-right' : 'text-left'">{{ item.value }}</td>
              </tr>
              <tr>
                <td class="text-left font-weight-bold">
                  Type de déclaration : {{ diagnostic.diagnosticType === "COMPLETE" ? "Complète" : "Simple" }}
                </td>
                <td class="text-left font-weight-bold"></td>
              </tr>
              <tr v-for="item in approItems" :key="item.param" :class="diagnostic[item.param] ? '' : 'warn'">
                <td class="text-left">{{ item.label }}</td>
                <td :class="diagnostic[item.param] ? 'text-right' : 'text-left'">
                  {{ diagnostic[item.param] ? `${diagnostic[item.param]} HT` : "Je ne sais pas" | toCurrency }}
                </td>
              </tr>
              <tr v-for="item in additionalItems" :key="item.label" :class="item.class || ''">
                <td class="text-left">{{ item.label }}</td>
                <td class="text-left">{{ item.value }}</td>
              </tr>
            </tbody>
          </template>
        </v-simple-table>
      </v-card-text>
      <div v-if="unusualData.length" class="text-left px-6">
        <p>Ces données sont-elles correctes ?</p>
        <ul>
          <li v-for="msg in unusualData" :key="msg" class="mb-4">{{ msg }}</li>
        </ul>
      </div>
      <v-form ref="teledeclarationForm" v-model="teledeclarationFormIsValid" id="teledeclaration-form" class="px-6">
        <v-checkbox
          :rules="[validators.checked]"
          label="Je déclare sur l’honneur la véracité de mes informations"
        ></v-checkbox>
      </v-form>
      <v-card-actions class="d-flex pr-4 pb-4">
        <v-spacer></v-spacer>
        <v-btn outlined color="primary" class="px-4" @click="closeDialog">Annuler</v-btn>
        <v-btn outlined color="primary" class="ml-4 px-4" @click="goToEditing" v-if="canteen">Modifier</v-btn>
        <v-btn color="primary" class="ml-4 px-4" @click="confirmTeledeclaration">Télédéclarer ces données</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import Constants from "@/constants"
import validators from "@/validators"
import { capitalise, sectorsSelectList } from "@/utils"

export default {
  props: {
    value: {
      required: true,
    },
    diagnostic: {
      required: true,
    },
    canteen: {
      required: true,
    },
  },
  data() {
    return {
      teledeclarationFormIsValid: true,
      validators,
      maxSatellitesExpected: 200,
      minCostPerMealExpected: 0.1,
      maxCostPerMealExpected: 10,
    }
  },
  computed: {
    isOpen: {
      get() {
        return this.value
      },
      set(newValue) {
        this.$emit("input", newValue)
      },
    },
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
      const ministryDetail = Constants.Ministries.find((x) => x.value === this.canteen.lineMinistry)
      let items = [
        { value: this.canteen.name, label: "Nom de la cantine" },
        { value: this.canteen.siret, label: "Numéro SIRET" },
        { value: this.canteen.city, label: "Ville" },
        { value: managementTypeDetail ? managementTypeDetail.text : "", label: "Mode de gestion" },
        { value: productionTypeDetail ? productionTypeDetail.body : "", label: "Type d'établissement" },
      ]
      if (this.usesCentralProducer)
        items.push({ value: this.canteen.centralProducerSiret, label: "SIRET de la cuisine centrale" })
      if (this.showSatelliteCanteensCount)
        items.push({
          value: this.canteen.satelliteCanteensCount,
          label: "Nombre de cantines à qui je fournis des repas",
          isNumber: true,
        })
      if (this.showDailyMealCount)
        items.push({ value: this.canteen.dailyMealCount, label: "Couverts moyen par jour", isNumber: true })
      items = items.concat([
        { value: this.canteen.yearlyMealCount, label: "Nombre total de couverts à l'année", isNumber: true },
        { value: this.sectors, label: "Secteurs d'activité" },
      ])
      if (this.showMinistryField)
        items.push({ value: ministryDetail ? ministryDetail.text : "", label: "Ministère de tutelle" })

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
          { param: "valueViandesVolaillesAocaopIgpStg", label: "Mes achats viandes et volailles AOC/AOP, IGP ou STG" },
          {
            param: "valueProduitsDeLaMerAocaopIgpStg",
            label: "Mes achats poissons, produits de la mer et de l'aquaculture AOC/AOP, IGP ou STG",
          },
          { param: "valueFruitsEtLegumesAocaopIgpStg", label: "Mes achats fruits et legumes AOC/AOP, IGP ou STG" },
          { param: "valueCharcuterieAocaopIgpStg", label: "Mes achats charcuterie AOC/AOP, IGP ou STG" },
          { param: "valueProduitsLaitiersAocaopIgpStg", label: "Mes achats produits laitiers AOC/AOP, IGP ou STG" },
          { param: "valueBoulangerieAocaopIgpStg", label: "Mes achats boulangerie AOC/AOP, IGP ou STG" },
          { param: "valueBoissonsAocaopIgpStg", label: "Mes achats boissons AOC/AOP, IGP ou STG" },
          { param: "valueAutresAocaopIgpStg", label: "Mes autres achats AOC/AOP, IGP ou STG" },
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
            label: "Mes achats viandes et volailles non-EGAlim",
          },
          {
            param: "valueProduitsDeLaMerNonEgalim",
            label: "Mes achats poissons, produits de la mer et de l'aquaculture non-EGAlim",
          },
          {
            param: "valueFruitsEtLegumesNonEgalim",
            label: "Mes achats fruits et legumes non-EGAlim",
          },
          { param: "valueCharcuterieNonEgalim", label: "Mes achats charcuterie non-EGAlim" },
          {
            param: "valueProduitsLaitiersNonEgalim",
            label: "Mes achats produits laitiers non-EGAlim",
          },
          { param: "valueBoulangerieNonEgalim", label: "Mes achats boulangerie non-EGAlim" },
          { param: "valueBoissonsNonEgalim", label: "Mes achats boissons non-EGAlim" },
          { param: "valueAutresNonEgalim", label: "Mes autres achats non-EGAlim" },

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
        { param: "valueSustainableHt", label: "Mes achats SIQO (AOP/AOC, IGP, STG)" },
        {
          param: "valueExternalityPerformanceHt",
          label:
            "Mes achats prenant en compte les coûts imputés aux externalités environnementales ou acquis sur la base de leurs performances en matière environnementale",
        },
        { param: "valueEgalimOthersHt", label: "Autres achats EGAlim" },
        {
          param: "valueMeatPoultryHt",
          label: "Mes achats en viandes et volailles fraiches ou surgelées total",
        },
        {
          param: "valueMeatPoultryEgalimHt",
          label: "Mes achats EGAlim en viandes et volailles fraiches ou surgelées",
        },
        {
          param: "valueMeatPoultryFranceHt",
          label: "Mes achats provenance France en viandes et volailles fraiches ou surgelées",
        },
        { param: "valueFishHt", label: "Mes achats en poissons, produits de la mer et de l'aquaculture total" },
        {
          param: "valueFishEgalimHt",
          label: "Mes achats EGAlim en poissons, produits de la mer et de l'aquaculture",
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

      return [
        {
          label: "Diagnostic sur le gaspillage alimentaire réalisé",
          value: this.diagnostic.hasWasteDiagnostic ? "Oui" : "Non",
        },
        {
          label: "Plan d'action contre le gaspillage en place",
          value: this.diagnostic.hasWastePlan ? "Oui" : "Non",
        },
        {
          label: "Actions contre le gaspillage en place",
          value: this.getWasteActions(this.diagnostic.wasteActions),
        },
        {
          label: "Autres actions contre le gaspillage alimentaire",
          value: this.diagnostic.otherWasteActions || "Aucune",
        },
        {
          label: "Propose des dons alimentaires",
          value: this.diagnostic.hasDonationAgreement ? "Oui" : "Non",
        },
        {
          label: "Réalise des mesures de gaspillage alimentaire",
          value: this.diagnostic.hasWasteMeasures ? "Oui" : "Non",
        },
        {
          label: "Restes de pain kg/an",
          value: this.diagnostic.breadLeftovers || "Non renseigné",
          class: this.diagnostic.breadLeftovers ? "" : "warn",
        },
        {
          label: "Restes servis (plateau) kg/an",
          value: this.diagnostic.servedLeftovers || "Non renseigné",
          class: this.diagnostic.servedLeftovers ? "" : "warn",
        },
        {
          label: "Restes non servis kg/an",
          value: this.diagnostic.unservedLeftovers || "Non renseigné",
          class: this.diagnostic.unservedLeftovers ? "" : "warn",
        },
        {
          label: "Restes de composantes kg/an",
          value: this.diagnostic.sideLeftovers || "Non renseigné",
          class: this.diagnostic.sideLeftovers ? "" : "warn",
        },
        {
          label: "Fréquence de dons en dons/an",
          value: this.diagnostic.donationFrequency || "Non renseigné",
          class: this.diagnostic.donationFrequency ? "" : "warn",
        },
        {
          label: "Quantité des denrées données kg/an",
          value: this.diagnostic.donationQuantity || "Non renseigné",
          class: this.diagnostic.donationQuantity ? "" : "warn",
        },
        {
          label: "Type de denrées données",
          value: this.diagnostic.donationFoodType || "Non renseigné",
          class: this.diagnostic.donationFoodType ? "" : "warn",
        },
        {
          label: "Autres commentaires sur le gaspillage",
          value: this.diagnostic.otherWasteComments || "Aucun",
        },
        {
          label: "Plan de diversification de protéines en place",
          value: this.diagnostic.hasDiversificationPlan ? "Oui" : "Non",
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
          value: this.diagnostic.cookingPlasticSubstituted ? "Oui" : "Non",
        },
        {
          label: "Contenants de service en plastique remplacés",
          value: this.diagnostic.servingPlasticSubstituted ? "Oui" : "Non",
        },
        {
          label: "Bouteilles en plastique remplacées",
          value: this.diagnostic.plasticBottlesSubstituted ? "Oui" : "Non",
        },
        {
          label: "Ustensils en plastique remplacés",
          value: this.diagnostic.plasticTablewareSubstituted ? "Oui" : "Non",
        },
        {
          label: "Supports de communication utilisés",
          value: this.getCommunicationSupports(this.diagnostic.communicationSupports),
        },
        {
          label: "Autres supports de communication",
          value: this.diagnostic.otherCommunicationSupport || "Non renseigné",
          class: this.diagnostic.otherCommunicationSupport ? "" : "warn",
        },
        {
          label: "Lien (URL) de communication",
          value: this.diagnostic.communicationSupportUrl || "Aucun",
        },
        {
          label: "Communique sur le plan alimentaire",
          value: this.diagnostic.communicatesOnFoodPlan ? "Oui" : "Non",
        },
        {
          label: "Communique sur les démarches qualité/durables/équitables",
          value: this.diagnostic.communicatesOnFoodQuality ? "Oui" : "Non",
        },
        {
          label: "Fréquence de communication",
          value: communicationFrequency,
          class: communicationFrequency === "Non renseigné" ? "warn" : "",
        },
      ]
    },
    canteenUrlComponent() {
      return this.canteen ? this.$store.getters.getCanteenUrlComponent(this.canteen) : null
    },
    sectors() {
      if (!this.canteen.sectors) return ""
      const sectors = this.$store.state.sectors
      const sectorDisplay = this.canteen.sectors
        .map((sectorId) => sectors.find((x) => x.id === sectorId).name.toLowerCase())
        .join(", ")
      return capitalise(sectorDisplay)
    },
    usesCentralProducer() {
      return this.canteen.productionType === "site_cooked_elsewhere"
    },
    showSatelliteCanteensCount() {
      return this.canteen.productionType === "central" || this.canteen.productionType === "central_serving"
    },
    showDailyMealCount() {
      return this.canteen.productionType && this.canteen.productionType !== "central"
    },
    showMinistryField() {
      const sectors = sectorsSelectList(this.$store.state.sectors)
      const concernedSectors = sectors.filter((x) => !!x.hasLineMinistry).map((x) => x.id)
      if (concernedSectors.length === 0) return false
      return this.canteen.sectors.some((x) => concernedSectors.indexOf(x) > -1)
    },
    unusualData() {
      const unusualData = []
      if (this.isCentralCuisine) {
        if (this.canteen.satelliteCanteensCount === 1) {
          unusualData.push("Votre établissement livre des repas à un seul site")
        } else if (this.canteen.satelliteCanteensCount > this.maxSatellitesExpected) {
          unusualData.push(
            `Votre établissement livre des repas à plus de 200 sites (${this.canteen.satelliteCanteensCount} au total)`
          )
        }
      }
      if (this.showApproItems) {
        if (this.costPerMeal > this.maxCostPerMealExpected || this.costPerMeal < this.minCostPerMealExpected) {
          unusualData.push(
            `Votre cout denrées est estimé à ${this.costPerMeal} € par repas servi. S'il s'agit d'une erreur, veuillez modifier les données d'achat et/ou le nombre de repas par an.`
          )
        }
      }
      return unusualData
    },
    isCentralCuisine() {
      // cannot use this.canteen.isCentralCuisine because that field may not be updated with latest canteen changes
      return this.canteen.productionType === "central" || this.canteen.productionType === "central_serving"
    },
    costPerMeal() {
      if (!this.showApproItems || !this.canteen.yearlyMealCount) return
      return Number(this.diagnostic.valueTotalHt / this.canteen.yearlyMealCount).toFixed(2)
    },
  },
  methods: {
    calculateTableHeight() {
      if (!this.$refs || !this.$refs.table || !this.$refs.content || !this.$refs.innerSimpleTable) return
      const contentHeight = this.$refs.content.$el.offsetHeight
      const currentTableHeight = this.$refs.table.offsetHeight
      const remainingItemsHeight = contentHeight - currentTableHeight
      const innerTableHeight = this.$refs.innerSimpleTable.$el.offsetHeight + 4 // 4 is the padding value
      const calculatedHeight = Math.min(window.innerHeight * 0.9 - remainingItemsHeight, innerTableHeight)
      this.$refs.table.style.height = `${parseInt(calculatedHeight)}px`
    },
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
      const actionItems = {
        PRODUCTS:
          "Agir sur les plats et les produits (diversification, gestion des quantités, recette traditionnelle, gout...)",
        PRESENTATION: "Agir sur la manière dont les aliments sont présentés aux convives (visuellement attrayants)",
        MENU: "Agir sur la manière dont les menus sont conçus ces plats en soulignant leurs attributs positifs",
        PROMOTION: "Agir sur la mise en avant des produits (plats recommandés, dégustation, mode de production...)",
        TRAINING:
          "Agir sur la formation du personnel, la sensibilisation des convives, l’investissement dans de nouveaux équipements de cuisine...",
      }
      const labels = diversificationPlanActions.map((x) => actionItems[x]).filter((x) => !!x)
      return labels.join(", ")
    },
    getVegetarianWeeklyRecurrence(vegetarianWeeklyRecurrence) {
      if (!vegetarianWeeklyRecurrence) return "Non renseigné"
      const items = {
        LOW: "Moins d'une fois par semaine",
        MID: "Une fois par semaine",
        HIGH: "Plus d'une fois par semaine",
        DAILY: "De façon quotidienne",
      }
      return items[vegetarianWeeklyRecurrence] || "Non renseigné"
    },
    getVegetarianMenuType(vegetarianMenuType) {
      if (!vegetarianMenuType) return "Non renseigné"
      const items = {
        UNIQUE: "Un menu végétarien en plat unique, sans choix",
        SEVERAL: "Un menu végétarien composé de plusieurs choix de plats végétariens",
        ALTERNATIVES: "Un menu végétarien au choix, en plus d'autres plats non végétariens",
      }
      return items[vegetarianMenuType] || "Non renseigné"
    },
    getVegetarianMenuBases(vegetarianMenuBases) {
      if (!vegetarianMenuBases || !vegetarianMenuBases.length) return "Non renseigné"
      const actionItems = {
        GRAIN: "De céréales et/ou les légumes secs (hors soja)",
        SOY: "De soja",
        CHEESE: "De fromage",
        EGG: "D’œufs",
        READYMADE: "Plats prêts à l'emploi",
      }
      const labels = vegetarianMenuBases.map((x) => actionItems[x]).filter((x) => !!x)
      return labels.join(", ")
    },
    getCommunicationSupports(communicationSupports) {
      if (!communicationSupports || !communicationSupports.length) return "Aucun"
      const supportItems = {
        EMAIL: "Envoi d'e-mail aux convives ou à leurs représentants",
        DISPLAY: "Par affichage sur le lieu de restauration",
        WEBSITE: "Sur site internet ou intranet (mairie, cantine)",
        OTHER: "Autres moyens d'affichage et de communication électronique",
        DIGITAL: "Par voie électronique",
      }
      const labels = communicationSupports.map((x) => supportItems[x]).filter((x) => !!x)
      return labels.join(", ")
    },
    getCommunicationFrequency(communicationFrequency) {
      if (!communicationFrequency) return "Non renseigné"
      const items = {
        REGULARLY: "Régulièrement au cours de l’année",
        YEARLY: "Une fois par an",
        LESS_THAN_YEARLY: "Moins d'une fois par an",
      }
      return items[communicationFrequency] || "Non renseigné"
    },
    closeDialog() {
      this.$emit("input", false)
    },
    confirmTeledeclaration() {
      if (this.$refs["teledeclarationForm"]) {
        const teledeclarationFormIsValid = this.$refs["teledeclarationForm"].validate()
        if (!teledeclarationFormIsValid) return
      }
      this.$emit("teledeclare")
    },
    goToEditing() {
      this.$emit("input", false)
      this.$router
        .push({
          name: "DiagnosticModification",
          params: { canteenUrlComponent: this.canteenUrlComponent, year: this.diagnostic.year },
        })
        .catch(() => {})
    },
  },
  mounted() {
    window.addEventListener("resize", this.calculateTableHeight)
    this.calculateTableHeight()
  },
  beforeDestroy() {
    window.removeEventListener("resize", this.calculateTableHeight)
  },
  watch: {
    value(newValue) {
      if (newValue) {
        this.$nextTick().then(this.calculateTableHeight)
      }
    },
  },
  filters: {
    toCurrency(value) {
      if (typeof value !== "number") {
        return value
      }
      const formatter = new Intl.NumberFormat("fr-FR", {
        style: "currency",
        currency: "EUR",
      })
      return formatter.format(value)
    },
  },
}
</script>

<style scoped>
.warn {
  background: #fff6da;
}
</style>
