<template>
  <div class="text-left">
    <BreadcrumbsNav :links="[{ to: { name: 'DashboardManager' }, title: canteen ? canteen.name : 'Dashboard' }]" />
    <v-row>
      <v-col cols="12" md="9">
        <ProductionTypeTag v-if="canteen" :canteen="canteen" class="mt-n2" />
        <!-- TODO: put Ma progression text up here -->
        <h1 class="fr-h3 my-2" v-if="canteen">{{ canteen.name }}</h1>
        <v-row v-if="canteenPreviews.length > 1">
          <v-col>
            <v-btn outlined color="primary" class="fr-btn--tertiary" :to="{ name: 'ManagementPage' }">
              Changer d'établissement
            </v-btn>
          </v-col>
        </v-row>
      </v-col>
      <v-col cols="12" md="3">
        <!-- TODO: should this be a nav element? -->
        <p class="body-2 my-2" for="yearSelect">Année</p>
        <DsfrSelect
          ref="yearSelect"
          v-model="selectedYear"
          :items="years"
          hide-details="auto"
          placeholder="Année du diagnostic"
        />
        <!-- TODO: a little indicator of whether this is the current year/provisional, the TD year, or other -->
      </v-col>
    </v-row>
    <v-row v-if="canteen" class="mt-10">
      <v-col cols="12" sm="9" md="10">
        <v-card v-if="isCentralKitchen" class="pa-6 mb-4 mr-1" style="background: #f5f5fe">
          <fieldset class="fr-text">
            <legend class="font-weight-bold">
              Pour mes cantines satellites, je saisis :
            </legend>
            <v-radio-group
              v-model="centralKitchenDiagnosticMode"
              :readonly="hasActiveTeledeclaration"
              :disabled="hasActiveTeledeclaration"
              class="py-0"
              hide-details
              row
              @change="handleModeChange"
            >
              <v-radio
                v-for="type in centralKitchenDiagnosticModes"
                :key="type.key"
                :label="type.shortLabel"
                :value="type.key"
              >
                <template v-slot:label>
                  <span class="fr-text mr-2 mr-lg-8 grey--text text--darken-4">
                    {{ type.shortLabel }}
                  </span>
                </template>
              </v-radio>
            </v-radio-group>
          </fieldset>
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
      <v-col cols="9" sm="3" md="2" style="border-left: 1px solid #DDD;">
        <h2 class="fr-h5 mb-2">Télédéclaration</h2>
        <div v-if="hasActiveTeledeclaration" class="fr-text-sm">
          <p class="font-weight-bold mb-0">Votre bilan {{ diagnostic.year }} a bien été télédéclaré.</p>
          <p>
            Votre bilan a été télédéclaré
            <b>{{ timeAgo(diagnostic.teledeclaration.creationDate, true) }}.</b>
          </p>
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
          <p v-else>
            En cas d'erreur, veuillez
            <router-link :to="{ name: 'ContactPage' }" class="grey--text text--darken-4">nous contacter</router-link>
            .
          </p>
          <DownloadLink
            :href="`/api/v1/teledeclaration/${diagnostic.teledeclaration.id}/document.pdf`"
            label="Télécharger le justificatif"
            sizeStr="60 Ko"
            target="_blank"
            class="mr-4"
          />
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
        <!-- is teledeclared -->
        <!-- satellites who are being declared for -->
        <!-- Year > lastYear -->
        <!-- year < lastYear -->
        <!-- year === lastYear -->
        <!-- completion status of each tab? If started with tunnel -->
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
import DsfrSelect from "@/components/DsfrSelect"
import DownloadLink from "@/components/DownloadLink"
import TeledeclarationPreview from "@/components/TeledeclarationPreview"
import TeledeclarationCancelDialog from "@/components/TeledeclarationCancelDialog"
import { diagnosticYears, timeAgo, lastYear, readyToTeledeclare } from "@/utils"
import keyMeasures from "@/data/key-measures.json"
import Constants from "@/constants"

export default {
  name: "MyProgress",
  components: {
    BreadcrumbsNav,
    ProductionTypeTag,
    ProgressTab,
    DsfrTabsVue,
    DsfrSelect,
    DownloadLink,
    TeledeclarationPreview,
    TeledeclarationCancelDialog,
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
      return readyToTeledeclare(this.canteen, this.diagnostic)
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
  },
  methods: {
    updateCanteen(newCanteen) {
      this.$set(this, "canteen", newCanteen)
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
