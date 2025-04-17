<template>
  <div class="text-left">
    <BreadcrumbsNav
      :links="[
        { to: { name: 'ManagementPage' } },
        { to: { name: 'DashboardManager' }, title: canteen ? canteen.name : 'Dashboard' },
      ]"
    />
    <v-row align="end">
      <v-col cols="12" md="9" lg="10">
        <DataInfoBadge
          :currentYear="+year === currentYear"
          :missingData="!readyToTeledeclare"
          :readyToTeledeclare="readyToTeledeclare"
          :hasActiveTeledeclaration="hasActiveTeledeclaration"
          :canteenAction="canteenAction"
          class="my-2"
        />
        <ProductionTypeTag v-if="canteen" :canteen="canteen" class="ml-3" />
        <h1 class="fr-h3 mt-1 mb-2" v-if="canteen">{{ canteen.name }} : Télédéclaration</h1>
        <p class="mb-0">SIRET : {{ canteen.siret || "inconnu" }}</p>
        <p v-if="canteen.sirenUniteLegale" class="mb-0">
          <span>SIREN de l'unité légale : {{ canteen.sirenUniteLegale }}</span>
        </p>
      </v-col>
      <v-col cols="12" md="3" lg="2">
        <v-btn
          v-if="canteenPreviews.length > 1"
          outlined
          color="primary"
          class="fr-btn--tertiary"
          :to="{ name: 'ManagementPage' }"
        >
          Changer d'établissement
        </v-btn>
      </v-col>
    </v-row>
    <v-row v-if="canteen" class="mt-5 mt-md-10">
      <!-- Sidebar -->
      <v-col cols="12" md="3" lg="2" style="border-right: 1px solid #DDD;" class="fr-text-sm pt-1">
        <DsfrNativeSelect v-model="selectedYear" :items="yearOptions" class="mb-3 mt-2" />
        <DataInfoBadge
          :currentYear="+year === currentYear"
          :missingData="!readyToTeledeclare"
          :readyToTeledeclare="readyToTeledeclare"
          :hasActiveTeledeclaration="hasActiveTeledeclaration"
          :canteenAction="canteenAction"
          class="my-2"
        />
        <div v-if="hasActiveTeledeclaration">
          <p>
            Votre bilan a été télédéclaré
            <b>{{ timeAgo(diagnostic.teledeclaration.creationDate, true) }}.</b>
          </p>
          <DownloadLink
            :href="`/api/v1/teledeclaration/${diagnostic.teledeclaration.id}/document.pdf`"
            label="Télécharger le justificatif"
            sizeStr="60 Ko"
            target="_blank"
            class="mr-4"
          />
          <p v-if="inTeledeclarationCampaign || inCorrectionCampaign">
            En cas d'erreur, vous pouvez modifier vos données
            <span v-if="campaignEndDate">
              jusqu’au
              {{ campaignEndDate.toLocaleString("fr-FR", { month: "long", day: "numeric", year: "numeric" }) }} (heure
              de Paris).
            </span>
            <span v-else>
              jusqu’à la fin de la campagne.
            </span>
          </p>
          <TeledeclarationCancelDialog
            v-model="cancelDialog"
            v-if="inTeledeclarationCampaign || inCorrectionCampaign"
            @cancel="cancelTeledeclaration"
            :diagnostic="diagnostic"
          >
            <template v-slot:activator="{ on, attrs }">
              <v-btn outlined small color="primary" class="fr-btn--tertiary px-2" v-on="on" v-bind="attrs">
                Corriger ma télédéclaration
              </v-btn>
            </template>
          </TeledeclarationCancelDialog>
        </div>
        <div v-else-if="isSatelliteWithCompleteCentralDiagnostic">
          <p>
            Votre livreur des repas {{ isSatelliteWithCentralDiagnosticTeledeclared ? "a déclaré" : "va déclarer" }} le
            bilan pour votre établissement.
          </p>
        </div>
        <div v-else-if="inTeledeclarationCampaign || (inCorrectionCampaign && hasCancelledTeledeclaration)">
          <div v-if="isSatelliteWithApproCentralDiagnostic">
            <p>
              Votre livreur des repas
              {{ isSatelliteWithCentralDiagnosticTeledeclared ? "a déclaré" : "va déclarer" }} les données
              d'approvisionnement pour votre établissement.
            </p>
            <p>Pour aller plus loin, vous pouvez télédéclarer les autres volets du bilan.</p>
          </div>
          <ul class="progress-list">
            <li
              v-for="tab in tabHeaders"
              :key="tab.id"
              v-show="!usesSatelliteDiagnosticForMeasure(tab)"
              class="mb-2 progress-list__item"
            >
              <p class="mb-0 font-weight-bold">
                <v-icon small class="black--text">{{ tab.icon }}</v-icon>
                {{ tab.text }}
              </p>
              <KeyMeasureBadge :diagnostic="diagnostic" :year="selectedYear" :canteen="canteen" :id="tab.id" />
            </li>
          </ul>
          <ul>
            <li v-if="hasSatelliteInconsistency" class="mb-1">
              <router-link
                :to="{
                  name: 'SatelliteManagement',
                  params: { canteenUrlComponent: $store.getters.getCanteenUrlComponent(canteen) },
                }"
              >
                Mettre à jour vos satellites
              </router-link>
            </li>
            <li v-if="missingDeclarationMode">
              Choisir comment les données sont saisis pour vos satellites
            </li>
          </ul>
          <v-btn
            color="primary"
            :disabled="!readyToTeledeclare"
            @click="showTeledeclarationPreview = true"
            class="mt-3"
          >
            Télédéclarer
          </v-btn>
        </div>
        <div v-else-if="+year >= currentYear">
          <p>
            Vous pouvez commencer ce bilan et le télédéclarer pendant la campagne de télédéclaration en
            {{ +year + 1 }}.
          </p>
        </div>
        <div v-else>
          <p>La campagne de télédéclaration pour {{ year }} a pris fin. Aucune action n'est requise de votre part.</p>
        </div>
        <p class="mt-4">
          Question, problème ?
          <router-link :to="{ name: 'ContactPage' }" class="grey--text text--darken-4">Contactez-nous</router-link>
        </p>
      </v-col>
      <!-- Diagnostic tabs -->
      <v-col cols="12" md="9" lg="10">
        <v-card v-if="isCentralKitchen" class="pa-6 mb-4 mr-1" style="background: #f5f5fe">
          <v-radio-group
            v-model="centralKitchenDiagnosticMode"
            :readonly="hasActiveTeledeclaration"
            :disabled="hasActiveTeledeclaration"
            class="py-0 mt-0"
            hide-details
            @change="handleModeChange"
          >
            <template v-slot:label>
              <span class="fr-text font-weight-bold grey--text text--darken-4">
                Pour mes cantines satellites, je saisis :
              </span>
            </template>
            <v-row class="my-0">
              <v-col
                cols="12"
                md="6"
                v-for="type in centralKitchenDiagnosticModes"
                :key="type.key"
                class="py-0 pt-md-2"
              >
                <v-radio :label="type.shortLabel" :value="type.key">
                  <template v-slot:label>
                    <span class="fr-text mr-2 mr-lg-8 grey--text text--darken-4">
                      {{ type.shortLabel }}
                    </span>
                  </template>
                </v-radio>
              </v-col>
            </v-row>
          </v-radio-group>
        </v-card>
        <DsfrTabsVue
          v-model="tab"
          :enableMobileView="$vuetify.breakpoint.smAndDown"
          mobileLabel="Mesure de la loi EGalim"
          :mobileSelectItems="mobileSelectItems"
          active-class="selected"
        >
          <template v-slot:tabs>
            <v-tab
              v-for="tabItem in tabHeaders"
              class="mx-1"
              :key="tabItem.text"
              :disabled="usesSatelliteDiagnosticForMeasure(tabItem)"
            >
              <v-icon small :class="`mr-1 ${tabTextClasses(tabItem)}`">{{ tabItem.icon }}</v-icon>
              <span :class="tabTextClasses(tabItem)">{{ tabItem.text }}</span>
            </v-tab>
          </template>
          <template v-slot:items>
            <v-tab-item class="my-4" v-for="(item, index) in tabHeaders" :key="`${index}-content`">
              <ProgressTab
                :measureId="item.urlSlug"
                :year="+year"
                :canteen="canteen"
                :diagnostic="diagnostic"
                :centralDiagnostic="centralDiagnostic"
                :centralKitchenDiagnosticMode="centralKitchenDiagnosticMode"
              />
              <v-row class="mt-6 align-center">
                <v-col v-if="previousTab(item)">
                  <p class="fr-text-sm mb-0">
                    <v-icon small color="primary" class="mr-1">$arrow-left-line</v-icon>
                    <router-link :to="{ params: { measure: previousTab(item).urlSlug } }">
                      {{ previousTab(item).title }}
                    </router-link>
                  </p>
                </v-col>
                <v-col class="text-right">
                  <p v-if="nextTab(item)" class="fr-text-sm mb-0">
                    <router-link :to="{ params: { measure: nextTab(item).urlSlug } }">
                      {{ nextTab(item).title }}
                    </router-link>
                    <v-icon small color="primary" class="ml-1">$arrow-right-line</v-icon>
                  </p>
                  <v-btn
                    v-else-if="hasActiveTeledeclaration"
                    outlined
                    small
                    color="primary"
                    class="fr-btn--tertiary px-2"
                    :disabled="true"
                  >
                    <v-icon small class="mr-2">$check-line</v-icon>
                    Données télédéclarées
                  </v-btn>
                  <v-btn
                    v-else-if="readyToTeledeclare && actionIsTeledeclare"
                    color="primary"
                    @click="showTeledeclarationPreview = true"
                    class="fr-text font-weight-medium"
                  >
                    Vérifier et télédéclarer mes données {{ diagnostic.year }}
                  </v-btn>
                </v-col>
              </v-row>
            </v-tab-item>
          </template>
        </DsfrTabsVue>
      </v-col>
    </v-row>
    <TeledeclarationPreview
      v-if="diagnostic"
      :diagnostic="diagnostic"
      :canteen="canteen"
      v-model="showTeledeclarationPreview"
      @teledeclare="submitTeledeclaration"
    />
  </div>
</template>

<script>
import BreadcrumbsNav from "@/components/BreadcrumbsNav"
import ProductionTypeTag from "@/components/ProductionTypeTag"
import ProgressTab from "./ProgressTab"
import DsfrTabsVue from "@/components/DsfrTabs"
import DsfrNativeSelect from "@/components/DsfrNativeSelect"
import DownloadLink from "@/components/DownloadLink"
import TeledeclarationPreview from "@/components/TeledeclarationPreview"
import TeledeclarationCancelDialog from "@/components/TeledeclarationCancelDialog"
import DataInfoBadge from "@/components/DataInfoBadge"
import KeyMeasureBadge from "@/components/KeyMeasureBadge"
import {
  customDiagnosticYears,
  diagnosticYears,
  timeAgo,
  lastYear,
  readyToTeledeclare,
  hasDiagnosticApproData,
  missingCanteenData,
  hasSatelliteInconsistency,
  actionIsTeledeclare,
} from "@/utils"
import keyMeasures from "@/data/key-measures.json"
import Constants from "@/constants"

export default {
  name: "MyProgress",
  components: {
    BreadcrumbsNav,
    ProductionTypeTag,
    ProgressTab,
    DsfrTabsVue,
    DsfrNativeSelect,
    DownloadLink,
    TeledeclarationPreview,
    TeledeclarationCancelDialog,
    DataInfoBadge,
    KeyMeasureBadge,
  },
  props: {
    canteenUrlComponent: {
      type: String,
    },
    year: {},
    measure: {},
  },
  data() {
    const establishmentId = "etablissement"
    return {
      tab: null,
      diagnostic: null,
      centralDiagnostic: null,
      canteen: null,
      canteenAction: null,
      years: diagnosticYears(),
      currentYear: lastYear() + 1,
      selectedYear: +this.year,
      centralKitchenDiagnosticModes: Constants.CentralKitchenDiagnosticModes,
      centralKitchenDiagnosticMode: null,
      cancelDialog: false,
      showTeledeclarationPreview: false,
      approId: "qualite-des-produits",
      establishmentId,
      inTeledeclarationCampaign: false,
      inCorrectionCampaign: false,
      campaignEndDate: null,
    }
  },
  computed: {
    tabHeaders() {
      const tabHeaders = []
      for (let i = 0; i < keyMeasures.length; i++) {
        const measure = keyMeasures[i]
        const item = {
          urlSlug: measure.id,
          text: measure.tabText,
          title: measure.title,
          icon: measure.mdiIcon,
          id: measure.id,
          to: { params: { measure: measure.id } },
        }
        tabHeaders.push(item)
      }
      tabHeaders.push({
        urlSlug: this.establishmentId,
        text: "Établissement",
        title: "Établissement",
        icon: "$building-fill",
        id: "etablissement",
        to: { params: { measure: this.establishmentId } },
      })
      return tabHeaders
    },
    mobileSelectItems() {
      return this.tabHeaders.map((x, index) => ({ text: x.text, value: index }))
    },
    actionIsTeledeclare() {
      return actionIsTeledeclare(this.canteenAction)
    },
    hasCancelledTeledeclaration() {
      // During the correction campaign, we allow only canteens with an existing teledeclaration to do corrections
      // BUT the backend does not return CANCELLED teledeclarations
      // instead we look at the canteen's action
      return this.actionIsTeledeclare
    },
    hasActiveTeledeclaration() {
      return this.diagnostic?.teledeclaration?.status === "SUBMITTED"
    },
    isCentralKitchen() {
      return this.canteen?.productionType === "central" || this.canteen?.productionType === "central_serving"
    },
    canteenPreviews() {
      return this.$store.state.userCanteenPreviews
    },
    readyToTeledeclare() {
      return readyToTeledeclare(this.canteen, this.diagnostic, this.$store.state.sectors)
    },
    declaringApproOnly() {
      return this.isCentralKitchen && this.centralKitchenDiagnosticMode === "APPRO"
    },
    activeTabHeaders() {
      if (this.declaringApproOnly) {
        return this.tabHeaders.filter((t) => t.urlSlug === this.approId || t.urlSlug === this.establishmentId)
      }
      return this.tabHeaders
    },
    missingApproDiagnostic() {
      if (this.isSatelliteWithApproCentralDiagnostic) return false
      return !this.diagnostic
    },
    missingApproData() {
      if (this.isSatelliteWithApproCentralDiagnostic) return false
      return !this.diagnostic || !hasDiagnosticApproData(this.diagnostic)
    },
    missingCanteenData() {
      return !this.canteen || missingCanteenData(this.canteen, this.$store.state.sectors)
    },
    hasSatelliteInconsistency() {
      return !this.canteen || hasSatelliteInconsistency(this.canteen)
    },
    missingDeclarationMode() {
      return this.isCentralKitchen && !this.diagnostic?.centralKitchenDiagnosticMode
    },
    isSatellite() {
      return this.canteen?.productionType === "site_cooked_elsewhere"
    },
    isSatelliteWithCompleteCentralDiagnostic() {
      return this.isSatellite && this.centralDiagnostic?.centralKitchenDiagnosticMode === "ALL"
    },
    isSatelliteWithApproCentralDiagnostic() {
      return this.isSatellite && this.centralDiagnostic?.centralKitchenDiagnosticMode === "APPRO"
    },
    isSatelliteWithCentralDiagnosticTeledeclared() {
      return this.centralDiagnostic.isTeledeclared
    },
    yearOptions() {
      return this.years.map((year) => ({ text: year, value: year }))
    },
  },
  methods: {
    fetchCampaignDates() {
      fetch(`/api/v1/campaignDates/${this.selectedYear}`)
        .then((response) => response.json())
        .then((response) => {
          this.inTeledeclarationCampaign = response.inTeledeclaration
          this.inCorrectionCampaign = response.inCorrection
          if (response.inTeledeclaration) this.campaignEndDate = new Date(response.teledeclarationEndDate)
          if (response.inCorrection) this.campaignEndDate = new Date(response.correctionEndDate)
        })
    },
    updateCanteen(newCanteen) {
      this.$set(this, "canteen", newCanteen)
      this.years = customDiagnosticYears(newCanteen.diagnostics)
    },
    fetchCanteen() {
      const id = this.canteenUrlComponent.split("--")[0]
      return this.$store
        .dispatch("fetchCanteen", { id })
        .then((canteen) => this.updateCanteen(canteen))
        .catch(() => {
          this.$store.dispatch("notify", {
            message: "Nous n'avons pas trouvé cette cantine",
            status: "error",
          })
          this.$router.push({ name: "ManagementPage" })
        })
    },
    fetchCanteenAction() {
      if (!this.canteen || !this.year) return
      fetch(`/api/v1/actionableCanteens/${this.canteen.id}/${this.year}`)
        .then((response) => {
          if (response.status < 200 || response.status >= 400) throw new Error(`Error encountered : ${response}`)
          return response.json()
        })
        .then((canteen) => {
          this.canteenAction = canteen.action
        })
    },
    assignDiagnostic() {
      if (!this.canteen) return
      const diag = this.canteen.diagnostics?.find((x) => +x.year === +this.year)
      this.$set(this, "diagnostic", diag)
      if (this.canteen.productionType === "site_cooked_elsewhere") {
        const centralDiag = this.canteen.centralKitchenDiagnostics?.find((x) => +x.year === +this.year)
        this.$set(this, "centralDiagnostic", centralDiag)
      }
      this.initialiseMode()
    },
    initialiseMode() {
      if (this.diagnostic) {
        this.centralKitchenDiagnosticMode = this.diagnostic.centralKitchenDiagnosticMode
      } else if (this.isCentralKitchen) {
        this.centralKitchenDiagnosticMode = this.centralKitchenDiagnosticMode || "ALL"
      } else {
        this.centralKitchenDiagnosticMode = null
      }
      this.chooseTabToDisplay()
    },
    chooseTabToDisplay() {
      const initialTab = this.tabHeaders.find((x) => x.urlSlug === this.measure)
      if (!initialTab) {
        this.$router.replace({
          name: this.$route.name,
          params: {
            canteenUrlComponent: this.canteenUrlComponent,
            year: this.year,
            measure: this.tabHeaders[0].urlSlug,
          },
        })
      } else if (this.declaringApproOnly && this.measure !== this.approId && this.measure !== "etablissement") {
        this.$router.replace({ name: "MyProgress", params: { measure: this.approId } })
      } else {
        this.tab = this.tabHeaders.indexOf(initialTab)
      }
    },
    usesSatelliteDiagnosticForMeasure(tabItem) {
      const tabAlwaysShown = tabItem.urlSlug === "qualite-des-produits" || tabItem.urlSlug === "etablissement"
      if (tabAlwaysShown) return false
      return this.declaringApproOnly
    },
    previousTab(tabItem) {
      const idx = this.activeTabHeaders.findIndex((t) => t.urlSlug === tabItem.urlSlug)
      return this.activeTabHeaders[idx - 1]
    },
    nextTab(tabItem) {
      const idx = this.activeTabHeaders.findIndex((t) => t.urlSlug === tabItem.urlSlug)
      return this.activeTabHeaders[idx + 1]
    },
    tabTextClasses(tabItem) {
      return this.usesSatelliteDiagnosticForMeasure(tabItem) ? "grey--text" : "black--text"
    },
    timeAgo,
    submitTeledeclaration() {
      return this.$store
        .dispatch("submitTeledeclaration", { id: this.diagnostic.id })
        .then((diagnostic) => {
          this.$store.dispatch("notify", {
            title: "Télédéclaration prise en compte",
            status: "success",
          })
          this.fetchCanteenAction()
          this.updateFromServer(diagnostic)
          window.scrollTo(0, 0)
        })
        .catch((e) => {
          this.$store.dispatch("notifyServerError", e)
        })
        .finally(() => {
          this.showTeledeclarationPreview = false
        })
    },
    cancelTeledeclaration() {
      if (!this.canteen || !this.diagnostic) return
      return this.$store
        .dispatch("cancelTeledeclaration", {
          canteenId: this.canteen.id,
          id: this.diagnostic.teledeclaration.id,
        })
        .then((diagnostic) => {
          this.$store.dispatch("notify", {
            title: "Votre télédéclaration a bien été annulée",
          })
          this.fetchCanteenAction()
          this.updateFromServer(diagnostic)
        })
        .catch((e) => this.$store.dispatch("notifyServerError", e))
        .finally(() => (this.cancelDialog = false))
    },
    updateFromServer(diagnostic) {
      const diagnosticIndex = this.canteen.diagnostics.findIndex((x) => x.id === diagnostic.id)
      if (diagnosticIndex > -1) {
        this.canteen.diagnostics.splice(diagnosticIndex, 1, diagnostic)
        this.assignDiagnostic()
      }
    },
    handleModeChange() {
      const mode = this.centralKitchenDiagnosticMode
      if (!mode || !this.isCentralKitchen || !this.canteen) return
      if (this.diagnostic?.id) {
        if (this.diagnostic.centralKitchenDiagnosticMode === mode) return
        this.diagnostic.centralKitchenDiagnosticMode = mode
        this.$store.dispatch("updateDiagnostic", {
          canteenId: this.canteen.id,
          id: this.diagnostic.id,
          payload: { centralKitchenDiagnosticMode: mode },
        })
      }
      this.chooseTabToDisplay()
    },
    startApproTunnel() {
      return this.$store
        .dispatch("createDiagnostic", {
          canteenId: this.canteen.id,
          payload: {
            year: this.year,
            creationSource: "TUNNEL",
            centralKitchenDiagnosticMode: this.centralKitchenDiagnosticMode,
          },
        })
        .then(() => {
          this.$router.push({
            name: "DiagnosticTunnel",
            params: {
              canteenUrlComponent: this.canteenUrlComponent,
              year: this.year,
              measureId: "qualite-des-produits",
            },
          })
        })
        .catch((e) => {
          this.$store.dispatch("notifyServerError", e)
        })
    },
  },
  watch: {
    canteenUrlComponent() {
      this.canteen = null
      this.fetchCanteen()
    },
    tab() {
      if (this.$route.params.measure !== this.tabHeaders[this.tab].urlSlug)
        this.$router.push({ params: { measure: this.tabHeaders[this.tab].urlSlug } })
    },
    year() {
      this.fetchCanteenAction()
      this.assignDiagnostic()
      this.fetchCampaignDates()
    },
    canteen() {
      this.fetchCanteenAction()
      this.assignDiagnostic()
      this.fetchCampaignDates()
    },
    $route() {
      this.chooseTabToDisplay()
    },
    selectedYear() {
      this.$router.push({ name: "MyProgress", params: { year: this.selectedYear } })
    },
  },
  beforeMount() {
    this.fetchCanteen()
  },
}
</script>

<style scoped>
.constrained {
  max-width: 1200px !important;
}
.v-list-item {
  font-weight: bold;
  border-radius: 0;
  min-height: 35px;
  margin-bottom: 16px !important;
}
.v-list-item.v-item--active {
  color: rgb(0, 0, 145);
  border-left: solid;
}
.v-list-item--link::before {
  background-color: transparent;
}
.v-list-item:focus {
  outline: 2px solid #3b87ff;
}
.v-tab--disabled {
  opacity: 1;
  background-color: #e5e5e5 !important;
  color: #929292 !important;
}
.close-icon {
  border-bottom: solid 1px;
}
.progress-list {
  padding-left: 0;
  list-style: none;
}
.progress-list__item:last-child {
  margin-bottom: 0.25rem !important;
}
</style>
