<template>
  <div class="text-left">
    <v-row>
      <v-col cols="12" :class="columnClasses">
        <v-card outlined class="mt-4 pa-4">
          <v-card-title>
            <h2 class="font-weight-bold text-h6">
              <KeyMeasureTitle class="flex-shrink-1" :measure="qualityMeasure" />
            </h2>
          </v-card-title>
          <v-card-text class="pb-0">
            <p class="grey--text text--darken-3">
              La loi EGAlim encadre la répartition des produits achetés pour la conception des repas. Les menus doivent
              comporter, au cours de l'année 2022, {{ applicableRules.qualityThreshold }} % de produits de qualité et
              durables dont {{ applicableRules.bioThreshold }} % issus de l’agriculture biologique ou en conversion,
              pour les cantines
              {{ regionDisplayName ? `dans la région de ${regionDisplayName}` : "en France métropolitaine" }}.
            </p>
            <MultiYearSummaryStatistics
              :diagnostics="dashboardDiagnostics"
              headingId="appro-heading"
              height="260"
              :width="$vuetify.breakpoint.mdAndUp ? '650px' : '100%'"
              :applicableRules="applicableRules"
            />
            <KeyMeasureResource :baseComponent="qualityMeasure.baseComponent" v-if="showResources" />
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" :md="singleColumn ? '12' : '6'" :class="columnClasses">
        <v-card outlined class="mt-4 pa-4">
          <v-card-title class="font-weight-bold">
            <h2 class="font-weight-bold text-h6">
              <KeyMeasureTitle class="flex-shrink-1" :measure="wasteMeasure" />
            </h2>
          </v-card-title>
          <v-card-text>
            <div class="actions">
              <!-- TODO: what about second sub measure "Interdiction de rendre impropre à la consommation les denrées alimentaires encore consommables." ? -->
              <KeyMeasureAction
                :isDone="latestDiagnostic.hasWasteDiagnostic"
                label="Réalisation d'un diagnostic sur le gaspillage alimentaire"
              />
              <KeyMeasureAction
                :isDone="latestDiagnostic.hasWastePlan"
                label="Mise en place d'un plan d'actions contre le gaspillage"
              />
              <ul class="specifics-actions ml-8">
                <li v-for="action in latestDiagnostic.wasteActions" :key="action" class="my-1">
                  {{ wasteActions[action] }}
                </li>
              </ul>
              <ul class="specifics-actions ml-8" v-if="latestDiagnostic.otherWasteAction">
                <li class="my-1">
                  {{ latestDiagnostic.otherWasteAction }}
                </li>
              </ul>
              <KeyMeasureAction
                :isDone="latestDiagnostic.hasDonationAgreement"
                label="Dons aux associations"
                v-if="applicableRules.hasDonationAgreement"
              />
            </div>
            <KeyMeasureResource :baseComponent="wasteMeasure.baseComponent" v-if="showResources" />
          </v-card-text>
        </v-card>

        <v-card outlined class="mt-4 pa-4">
          <v-card-title class="text-left">
            <h2 class="font-weight-bold text-h6">
              <KeyMeasureTitle class="flex-shrink-1" :measure="noPlasticMeasure" />
            </h2>
          </v-card-title>
          <v-card-text>
            <p>Dans l'établissement, ont été supprimé l'usage des :</p>
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

      <v-col cols="12" :md="singleColumn ? '12' : '6'" :class="columnClasses">
        <v-card outlined class="mt-4 pa-4">
          <v-card-title>
            <h2 class="font-weight-bold text-h6">
              <KeyMeasureTitle class="flex-shrink-1" :measure="diversificationMeasure" />
            </h2>
          </v-card-title>
          <v-card-text>
            <div class="actions">
              <KeyMeasureAction
                :isDone="latestDiagnostic.hasDiversificationPlan"
                label="Mise en place d'un plan pluriannuel de diversification des protéines"
                v-if="applicableRules.hasDiversificationPlan"
              />
              <KeyMeasureAction :isDone="hasVegetarianMenu" :label="vegetarianMenuActionLabel" />
            </div>
            <KeyMeasureResource :baseComponent="diversificationMeasure.baseComponent" v-if="showResources" />
          </v-card-text>
        </v-card>

        <v-card outlined class="mt-4 pa-4">
          <v-card-title>
            <h2 class="font-weight-bold text-h6">
              <KeyMeasureTitle class="flex-shrink-1" :measure="informationMeasure" />
            </h2>
          </v-card-title>
          <v-card-text>
            <div class="actions">
              <KeyMeasureAction
                :isDone="latestDiagnostic.communicatesOnFoodQuality"
                label="Communication sur la part de produits de qualité et durables entrant dans la composition des repas servis"
              />
              <KeyMeasureAction
                :isDone="latestDiagnostic.communicatesOnFoodPlan"
                label="Communication sur le plan alimentaire"
              />
              <KeyMeasureAction
                :isDone="latestDiagnostic.communicationSupports && latestDiagnostic.communicationSupports.length > 0"
                label="Communication à disposition des convives sur la qualité des approvisionnements"
              />
              <ul class="specifics-actions ml-4">
                <li v-for="action in latestDiagnostic.communicationSupports" :key="action" class="my-1">
                  {{ communicationSupports[action] }}
                </li>
              </ul>
              <ul class="specifics-actions ml-4" v-if="latestDiagnostic.otherCommunicationSupport">
                <li class="my-1">
                  {{ latestDiagnostic.otherCommunicationSupport }}
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
            <!-- TODO: what about the third sub-measure, etiquettage détaillé pour toutes les viandes ? -->
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
import KeyMeasureResource from "@/components/KeyMeasureResource"
import KeyMeasureAction from "@/components/KeyMeasureAction"
import KeyMeasureTitle from "@/components/KeyMeasureTitle"
import MultiYearSummaryStatistics from "./MultiYearSummaryStatistics"
import { lastYear, applicableDiagnosticRules } from "@/utils"
import regions from "@/regions.json"

export default {
  components: {
    KeyMeasureResource,
    KeyMeasureAction,
    KeyMeasureTitle,
    MultiYearSummaryStatistics,
  },
  props: {
    diagnostics: {
      Object,
      required: false,
    },
    showResources: Boolean,
    canteen: {
      type: Object,
      required: false,
    },
    singleColumn: Boolean,
  },
  data() {
    return {
      wasteActions,
      communicationSupports,
      qualityMeasure: keyMeasures.find((measure) => measure.id === "qualite-des-produits"),
      wasteMeasure: keyMeasures.find((measure) => measure.id === "gaspillage-alimentaire"),
      diversificationMeasure: keyMeasures.find((measure) => measure.id === "diversification-des-menus"),
      noPlasticMeasure: keyMeasures.find((measure) => measure.id === "interdiction-du-plastique"),
      informationMeasure: keyMeasures.find((measure) => measure.id === "information-des-usagers"),
    }
  },
  computed: {
    dashboardDiagnostics() {
      if (this.diagnostics) {
        return this.diagnostics
      }
      const diagCount = this.canteen.diagnostics.length
      if (!diagCount) {
        return {} // TODO: what to do?
      }
      const lastYearDiag = this.canteen.diagnostics.find((d) => d.year === lastYear())
      return {
        latest: lastYearDiag || this.canteen.diagnostics[diagCount - 1],
      }
    },
    latestDiagnostic() {
      return this.dashboardDiagnostics.latest
    },
    previousDiagnostic() {
      return this.dashboardDiagnostics.previous
    },
    vegetarianFrequency() {
      return this.latestDiagnostic.vegetarianWeeklyRecurrence
    },
    hasVegetarianMenu() {
      return this.vegetarianFrequency && this.vegetarianFrequency !== "LOW"
    },
    vegetarianMenuActionLabel() {
      if (this.vegetarianFrequency === "MID") {
        return "Mise en place d'un menu végétarien par semaine"
      } else if (this.vegetarianFrequency === "HIGH") {
        return "Mise en place d'un menu végétarien plusieurs fois par semaine"
      } else if (this.vegetarianFrequency === "DAILY") {
        return "Mise en place d'un menu végétarien de façon quotidienne"
      }
      return "Pas de menu végétarien hébdomadaire"
    },
    applicableRules() {
      return applicableDiagnosticRules(this.canteen)
    },
    regionDisplayName() {
      return this.applicableRules.hasQualityException
        ? regions.find((r) => r.regionCode === this.canteen.region).regionName
        : ""
    },
    columnClasses() {
      return this.singleColumn ? "pa-0" : ""
    },
  },
  methods: {
    prepareHref(link) {
      return link.startsWith("http") ? link : "//" + link
    },
  },
}
</script>
