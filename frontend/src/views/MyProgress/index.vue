<template>
  <div class="text-left">
    <BreadcrumbsNav
      :links="[
        { to: { name: 'ManagementPage' } },
        { to: { name: 'DashboardManager' }, title: canteen ? canteen.name : 'Dashboard' },
      ]"
    />
    <v-row>
      <v-col cols="12" md="10">
        <ProductionTypeTag v-if="canteen" :canteen="canteen" class="mt-n2" />
        <h1 class="fr-h3 mt-1 mb-2" v-if="canteen">{{ canteen.name }}</h1>
        <v-row v-if="canteenPreviews.length > 1">
          <v-col>
            <v-btn outlined color="primary" class="fr-btn--tertiary" :to="{ name: 'ManagementPage' }">
              Changer d'établissement
            </v-btn>
          </v-col>
        </v-row>
      </v-col>
      <v-col cols="12" sm="5" md="2">
        <DsfrNativeSelect label="Année" v-model="selectedYear" :items="yearOptions" />
      </v-col>
    </v-row>
    <v-row v-if="canteen" class="mt-5 mt-md-10">
      <v-col cols="12" sm="9" md="3" lg="2" style="border-left: 1px solid #DDD;" class="fr-text-sm order-md-last pr-0">
        <h2 class="fr-h5 mb-2">Télédéclaration</h2>
        <div v-if="hasActiveTeledeclaration">
          <DataInfoBadge class="my-2" :hasActiveTeledeclaration="true" />
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
          <p v-if="inTeledeclarationCampaign">
            En cas d'erreur, vous pouvez annuler votre télédéclaration et modifier vos données
            <span v-if="campaignEndDate">
              jusqu’au
              {{ campaignEndDate.toLocaleString("fr-FR", { month: "long", day: "numeric", year: "numeric" }) }}.
            </span>
            <span v-else>
              jusqu’à la fin de la campagne.
            </span>
          </p>
          <TeledeclarationCancelDialog
            v-model="cancelDialog"
            v-if="inTeledeclarationCampaign"
            @cancel="cancelTeledeclaration"
            :diagnostic="diagnostic"
          >
            <template v-slot:activator="{ on, attrs }">
              <v-btn outlined small color="primary" class="fr-btn--tertiary px-2" v-on="on" v-bind="attrs">
                Annuler ma télédéclaration
              </v-btn>
            </template>
          </TeledeclarationCancelDialog>
        </div>
        <div v-else-if="isSatelliteWithCompleteCentralDiagnostic">
          <p>Votre cuisine centrale va faire le bilan pour votre établissement.</p>
        </div>
        <div v-else-if="inTeledeclarationCampaign">
          <div v-if="isSatelliteWithApproCentralDiagnostic">
            <p>Votre cuisine centrale va déclarer les données d'approvisionnement pour votre établissement.</p>
            <p>Pour aller plus loin, vous pouvez télédéclarer les autres volets du bilan.</p>
            <v-btn v-if="readyToTeledeclare" outlined color="primary" @click="showTeledeclarationPreview = true">
              Télédéclarer
            </v-btn>
          </div>
          <div v-else-if="readyToTeledeclare">
            <DataInfoBadge class="my-2" :readyToTeledeclare="true" />
            <div v-if="hasFinishedMeasureTunnel">
              <p>Votre bilan est complet !</p>
              <v-btn color="primary" @click="showTeledeclarationPreview = true">Télédéclarer</v-btn>
            </div>
            <div v-else>
              <p>Vous pouvez télédéclarer dès maintenant.</p>
              <p v-if="!isCentralKitchen || diagnostic.centralKitchenDiagnosticMode !== 'APPRO'">
                Pour aller plus loin, vous pouvez également compléter les autres volets du bilan.
              </p>
              <v-btn outlined color="primary" @click="showTeledeclarationPreview = true">
                Télédéclarer
              </v-btn>
            </div>
          </div>
          <div v-else>
            <DataInfoBadge class="my-2" :missingData="true" />
            <p>Pour télédéclarer, veuillez :</p>
            <ul>
              <li v-if="missingApproDiagnostic" class="mb-2">
                <router-link
                  custom
                  :to="{
                    name: 'DiagnosticTunnel',
                    params: {
                      canteenUrlComponent: this.canteenUrlComponent,
                      year: year,
                      measureId: 'qualite-des-produits',
                    },
                  }"
                  v-slot="{ href }"
                >
                  <a @click.stop.prevent="startApproTunnel" :href="href">Rentrer mes données d'approvisionnement</a>
                </router-link>
              </li>
              <li v-else-if="missingApproData" class="mb-2">
                <router-link
                  :to="{
                    name: 'DiagnosticTunnel',
                    params: {
                      canteenUrlComponent: this.canteenUrlComponent,
                      year: year,
                      measureId: 'qualite-des-produits',
                    },
                  }"
                >
                  Compléter le volet d’approvisionnement
                </router-link>
              </li>
              <li v-if="missingCanteenData" class="mb-2">
                <router-link
                  :to="{
                    name: 'CanteenForm',
                    params: { canteenUrlComponent: this.canteenUrlComponent },
                    query: { valider: true },
                  }"
                >
                  Compléter les données de votre établissement
                </router-link>
              </li>
              <li v-if="hasSatelliteInconsistency" class="mb-2">
                <router-link
                  :to="{
                    name: 'SatelliteManagement',
                    params: { canteenUrlComponent: $store.getters.getCanteenUrlComponent(canteen) },
                  }"
                >
                  Mettre à jour vos satellites
                </router-link>
              </li>
              <li v-if="missingDeclarationMode" class="mb-2">
                Choisir comment les données sont saisis pour vos satellites
              </li>
            </ul>
          </div>
        </div>
        <div v-else-if="+year >= currentYear">
          <DataInfoBadge class="my-2" :currentYear="+year === currentYear" />
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
          mobileLabel="Mesure de la loi EGAlim"
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
                    v-else-if="readyToTeledeclare"
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
import {
  customDiagnosticYears,
  diagnosticYears,
  timeAgo,
  lastYear,
  readyToTeledeclare,
  hasDiagnosticApproData,
  missingCanteenData,
  hasSatelliteInconsistency,
  hasFinishedMeasureTunnel,
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
      tabHeaders: [
        ...keyMeasures.map((x) => ({
          urlSlug: x.id,
          text: x.tabText,
          title: x.title,
          icon: x.mdiIcon,
          to: { params: { measure: x.id } },
        })),
        ...[
          {
            urlSlug: establishmentId,
            text: "Établissement",
            title: "Établissement",
            icon: "$building-fill",
            to: { params: { measure: establishmentId } },
          },
        ],
      ],
      canteen: null,
      years: diagnosticYears(),
      currentYear: lastYear() + 1,
      selectedYear: +this.year,
      centralKitchenDiagnosticModes: Constants.CentralKitchenDiagnosticModes,
      centralKitchenDiagnosticMode: null,
      cancelDialog: false,
      campaignEndDate: window.TELEDECLARATION_END_DATE ? new Date(window.TELEDECLARATION_END_DATE) : null,
      showTeledeclarationPreview: false,
      approId: "qualite-des-produits",
      establishmentId,
    }
  },
  computed: {
    mobileSelectItems() {
      return this.tabHeaders.map((x, index) => ({ text: x.text, value: index }))
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
    inTeledeclarationCampaign() {
      return window.ENABLE_TELEDECLARATION && +this.year === lastYear()
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
      return this.isCentralKitchen && !this.diagnostic.centralKitchenDiagnosticMode
    },
    hasFinishedMeasureTunnel() {
      return this.diagnostic && hasFinishedMeasureTunnel(this.diagnostic)
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
    yearOptions() {
      return this.years.map((year) => ({ text: year, value: year }))
    },
  },
  methods: {
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
      this.assignDiagnostic()
    },
    canteen() {
      this.assignDiagnostic()
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
</style>
