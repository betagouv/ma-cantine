<template>
  <div>
    <v-row>
      <v-col cols="12">
        <v-card outlined class="mt-4 pa-4">
          <v-card-title class="font-weight-bold">
            Données d'approvisionnements en produits durables et de qualité
          </v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12" md="6" class="d-flex flex-column align-center">
                <h3 class="text-h6">Sur l'année 2019</h3>
                <SummaryStatistics :qualityDiagnostic="previousDiagnostic" />
              </v-col>
              <v-col cols="12" md="6" class="d-flex flex-column align-center">
                <h3 class="text-h6">Sur l'année 2020</h3>
                <SummaryStatistics :qualityDiagnostic="latestDiagnostic" />
              </v-col>
              <v-col cols="12" md="6" class="d-flex flex-column align-center">
                <h3 class="text-h6">Prévisionnel 2021</h3>
                <SummaryStatistics :qualityDiagnostic="this.diagnostics.provisionalYear1" />
              </v-col>
              <v-col cols="12" md="6" class="d-flex flex-column align-center">
                <h3 class="text-h6">Prévisionnel 2022</h3>
                <SummaryStatistics :qualityDiagnostic="this.diagnostics.provisionalYear2" />
              </v-col>
            </v-row>
            <KeyMeasureResource :baseComponent="qualityMeasure.baseComponent" v-if="showResources" />
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="6">
        <v-card outlined class="mt-4 pa-4">
          <v-card-title class="font-weight-bold">Initiatives contre le gaspillage alimentaire</v-card-title>
          <v-card-text>
            <div class="actions">
              <KeyMeasureAction
                :isDone="latestDiagnostic.hasWasteDiagnostic"
                label="Réalisation d'un diagnostic sur le gaspillage alimentaire"
              />
              <KeyMeasureAction
                :isDone="latestDiagnostic.hasWastePlan"
                label="Mise en place d'un plan d'actions contre le gaspillage"
              />
              <ul class="specifics-actions text-left ml-4">
                <li v-for="action in latestDiagnostic.wasteActions" :key="action" class="my-1">
                  {{ wasteActions[action] }}
                </li>
              </ul>
              <KeyMeasureAction :isDone="latestDiagnostic.hasDonationAgreement" label="Dons aux associations" />
            </div>
            <KeyMeasureResource :baseComponent="wasteMeasure.baseComponent" v-if="showResources" />
          </v-card-text>
        </v-card>

        <v-card outlined class="mt-4 pa-4">
          <v-card-title class="font-weight-bold text-left">
            Dans l'établissement, ont été supprimé l'usage des :
          </v-card-title>
          <v-card-text>
            <div class="actions">
              <KeyMeasureAction
                :isDone="latestDiagnostic.cookingPlasticSubstituted"
                label="Contenants de cuisson / de réchauffe en plastique"
              />
              <KeyMeasureAction
                :isDone="latestDiagnostic.servingPlasticSubstituted"
                label="Contenants de service en plastique"
              />
              <KeyMeasureAction
                :isDone="latestDiagnostic.plasticBottlesSubstituted"
                label="Bouteilles d'eau en plastique"
              />
              <KeyMeasureAction
                :isDone="latestDiagnostic.plasticTablewareSubstituted"
                label="Ustensiles à usage unique en plastique"
              />
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="6">
        <v-card outlined class="mt-4 pa-4">
          <v-card-title class="font-weight-bold">{{ diversificationMeasure.shortTitle }}</v-card-title>
          <v-card-text>
            <div class="actions">
              <KeyMeasureAction
                :isDone="latestDiagnostic.hasDiversificationPlan"
                label="Mise en place d'un plan pluriannuel de diversification des protéines"
              />
              <KeyMeasureAction :isDone="hasVegetarianMenu" :label="vegetarianMenuActionLabel" />
            </div>
            <KeyMeasureResource :baseComponent="diversificationMeasure.baseComponent" v-if="showResources" />
          </v-card-text>
        </v-card>

        <v-card outlined class="mt-4 pa-4">
          <v-card-title class="font-weight-bold">{{ informationMeasure.shortTitle }}</v-card-title>
          <v-card-text>
            <div class="actions">
              <KeyMeasureAction
                :isDone="latestDiagnostic.communicatesOnFoodPlan"
                label="Communication sur le plan alimentaire"
              />
              <KeyMeasureAction
                :isDone="latestDiagnostic.communicationSupports.length > 0"
                label="Communication à disposition des convives sur la qualité des approvisionnements"
              />
              <ul class="specifics-actions text-left ml-4">
                <li v-for="action in latestDiagnostic.communicationSupports" :key="action" class="my-1">
                  {{ communicationSupports[action] }}
                </li>
              </ul>

              <v-btn
                v-if="latestDiagnostic.communicationSupportUrl"
                color="primary"
                :href="prepareHref(latestDiagnostic.communicationSupportUrl)"
                target="_blank"
                outlined
                class="my-2"
              >
                Lien vers le support de communication
                <v-icon small class="ml-2">mdi-open-in-new</v-icon>
              </v-btn>
            </div>
            <KeyMeasureResource baseComponent="InformDiners" v-if="showResources" />
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import keyMeasures from "@/data/key-measures.json"
import wasteActions from "@/data/waste-actions.json"
import communicationSupports from "@/data/communication-supports.json"
import SummaryStatistics from "@/components/SummaryStatistics"
import KeyMeasureResource from "@/components/KeyMeasureResource"
import KeyMeasureAction from "@/components/KeyMeasureAction"

export default {
  components: {
    SummaryStatistics,
    KeyMeasureResource,
    KeyMeasureAction,
  },
  props: {
    diagnostics: Object,
    showResources: Boolean,
  },
  data() {
    const latestDiagnostic = this.diagnostics.latest
    const vegetarianFrequency = latestDiagnostic.vegetarianWeeklyRecurrence
    const hasVegetarianMenu = vegetarianFrequency && vegetarianFrequency !== "LOW"

    return {
      latestDiagnostic,
      previousDiagnostic: this.diagnostics.previous,
      wasteActions,
      communicationSupports,
      qualityMeasure: keyMeasures.find((measure) => measure.id === "qualite-des-produits"),
      wasteMeasure: keyMeasures.find((measure) => measure.id === "gaspillage-alimentaire"),
      diversificationMeasure: keyMeasures.find((measure) => measure.id === "diversification-des-menus"),
      noPlasticMeasure: keyMeasures.find((measure) => measure.id === "interdiction-du-plastique"),
      informationMeasure: keyMeasures.find((measure) => measure.id === "information-des-usagers"),
      vegetarianFrequency,
      hasVegetarianMenu,
      vegetarianMenuActionLabel: getVegetarianMenuActionLabel(hasVegetarianMenu, vegetarianFrequency),
    }
  },
  methods: {
    prepareHref(link) {
      return link.startsWith("http") ? link : "//" + link
    },
  },
}

function getVegetarianMenuActionLabel(hasVegetarianMenu, vegetarianFrequency) {
  if (!hasVegetarianMenu) {
    return "Pas de menu végétarien"
  } else if (vegetarianFrequency === "MID") {
    return "Mise en place d'un menu végétarien"
  } else if (vegetarianFrequency === "HIGH") {
    return "Plusieurs menus végétariens"
  }
}
</script>
