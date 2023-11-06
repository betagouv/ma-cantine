<template>
  <div class="text-left">
    <BreadcrumbsNav :links="[{ to: { name: 'DashboardManager' }, title: canteen ? canteen.name : 'Dashboard' }]" />
    <ProductionTypeTag v-if="canteen" :canteen="canteen" class="mt-n2" />
    <h1 class="fr-h3 my-2" v-if="canteen">{{ canteen.name }}</h1>
    <v-row v-if="canteenPreviews.length > 1">
      <v-col>
        <v-btn outlined color="primary" class="fr-btn--tertiary" :to="{ name: 'ManagementPage' }">
          Changer d'établissement
        </v-btn>
      </v-col>
    </v-row>
    <v-row v-if="canteen" class="mt-10">
      <v-col cols="12" sm="3" md="2" style="border-right: 1px solid #DDD;">
        <h2 class="fr-h5">Ma progression</h2>
        <nav aria-label="Année du diagnostic" v-if="canteen && $vuetify.breakpoint.smAndUp">
          <v-list nav class="text-left">
            <v-list-item-group>
              <v-list-item
                :ripple="false"
                :to="{ name: 'MyProgress', params: { year } }"
                v-for="year in years"
                :key="year"
              >
                <v-list-item-title>{{ year }}</v-list-item-title>
              </v-list-item>
            </v-list-item-group>
          </v-list>
        </nav>
        <DsfrSelect hide-details label="Année" :items="years" v-model="year" v-else-if="canteen" />
      </v-col>
      <v-col cols="12" sm="9" md="10">
        <v-card v-if="hasActiveTeledeclaration" class="pa-6 mb-4 mr-1" style="background: #f6f6f6">
          <p class="fr-text-sm font-weight-bold mb-0">
            Votre bilan 2023 a bien été télédéclaré et ne peut plus être modifié.
          </p>
          <p class="fr-text-sm">
            Votre bilan a été télédéclaré
            <b>{{ timeAgo(diagnostic.teledeclaration.creationDate, true) }}.</b>
            <span v-if="inTeledeclarationCampaign">
              En cas d'erreur, vous pouvez annuler votre télédéclaration et modifier vos données
              <span v-if="campaignEndDate">
                jusqu’au
                {{ campaignEndDate.toLocaleString("fr-FR", { month: "long", day: "numeric", year: "numeric" }) }}.
              </span>
              <span v-else>
                jusqu’à la fin de la campagne.
              </span>
            </span>
            <span v-else>
              En cas d'erreur, veuillez
              <router-link :to="{ name: 'ContactPage' }" class="grey--text text--darken-4">nous contacter</router-link>
              .
            </span>
          </p>
          <v-card-actions class="px-0 pt-0 pb-0 align-start d-block d-md-flex">
            <div>
              <DownloadLink
                :href="`/api/v1/teledeclaration/${diagnostic.teledeclaration.id}/document.pdf`"
                label="Télécharger le justificatif"
                sizeStr="60 Ko"
                target="_blank"
                class="mb-0 mr-4"
              />
            </div>
            <div class="mt-4 mt-md-0">
              <TeledeclarationCancelDialog
                v-model="cancelDialog"
                v-if="inTeledeclarationCampaign"
                @cancel="cancelTeledeclaration"
                :diagnostic="diagnostic"
              >
                <template v-slot:activator="{ on, attrs }">
                  <a class="ml-0 ml-md-4 text-decoration-underline" v-on="on" v-bind="attrs">
                    Annuler ma télédéclaration
                    <v-icon color="primary" size="1rem" class="ml-0 mb-1 close-icon">
                      $close-line
                    </v-icon>
                  </a>
                </template>
              </TeledeclarationCancelDialog>
            </div>
          </v-card-actions>
        </v-card>
        <v-card
          v-else-if="readyToTeledeclare"
          class="pa-6 mb-4 mr-1 fr-text grey--text text--darken-3 text-center cta-block"
        >
          <p class="mb-0">
            Votre bilan {{ diagnostic.year }} est complet ! Merci d’avoir pris le temps de saisir vos données !
          </p>
          <p>
            Vérifiez-les une dernière fois et télédéclarez-les pour participer au bilan statistique national
            obligatoire.
          </p>
          <v-card-actions class="px-0 pt-0 pb-0 justify-center">
            <v-btn color="primary" @click="showTeledeclarationPreview = true" class="fr-text font-weight-medium">
              Vérifier et télédéclarer mes données {{ diagnostic.year }}
            </v-btn>
          </v-card-actions>
        </v-card>
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
              />
              <v-row class="mt-6">
                <v-col v-if="index > 0">
                  <p class="fr-text-sm">
                    <v-icon small color="primary" class="mr-1">$arrow-left-line</v-icon>
                    <router-link :to="{ params: { measure: tabHeaders[index - 1].urlSlug } }">
                      {{ tabHeaders[index - 1].title }}
                    </router-link>
                  </p>
                </v-col>
                <v-col v-if="index < tabHeaders.length - 1" class="text-right">
                  <p class="fr-text-sm">
                    <router-link :to="{ params: { measure: tabHeaders[index + 1].urlSlug } }">
                      {{ tabHeaders[index + 1].title }}
                    </router-link>
                    <v-icon small color="primary" class="ml-1">$arrow-right-line</v-icon>
                  </p>
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
import DsfrSelect from "@/components/DsfrSelect"
import DownloadLink from "@/components/DownloadLink"
import TeledeclarationPreview from "@/components/TeledeclarationPreview"
import TeledeclarationCancelDialog from "@/components/TeledeclarationCancelDialog"
import { diagnosticYears, timeAgo, lastYear, hasDiagnosticApproData } from "@/utils"
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
  data() {
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
            urlSlug: "etablissement",
            text: "Établissement",
            title: "Établissement",
            icon: "$building-fill",
            to: { params: { measure: "etablissement" } },
          },
        ],
      ],
      canteen: null,
      years: diagnosticYears().map((x) => x.toString()),
      centralKitchenDiagnosticModes: Constants.CentralKitchenDiagnosticModes,
      centralKitchenDiagnosticMode: null,
      cancelDialog: false,
      campaignEndDate: window.TELEDECLARATION_END_DATE ? new Date(window.TELEDECLARATION_END_DATE) : null,
      showTeledeclarationPreview: false,
    }
  },
  props: {
    canteenUrlComponent: {
      type: String,
    },
    year: {},
    measure: {},
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
      return this.diagnostic && this.inTeledeclarationCampaign && hasDiagnosticApproData(this.diagnostic)
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
      this.$set(
        this,
        "diagnostic",
        this.canteen?.diagnostics?.find((x) => +x.year === +this.year)
      )
      if (this.canteen?.productionType === "site_cooked_elsewhere") {
        this.$set(
          this,
          "centralDiagnostic",
          this.canteen?.centralKitchenDiagnostics?.find((x) => +x.year === +this.year)
        )
      }
      this.centralKitchenDiagnosticMode = this.diagnostic?.centralKitchenDiagnosticMode
      this.initialiseTab()
    },
    initialiseTab() {
      const initialTab = this.tabHeaders.find((x) => x.urlSlug === this.measure)
      const approId = "qualite-des-produits"
      if (!initialTab) {
        this.$router.replace({
          name: this.$route.name,
          params: {
            canteenUrlComponent: this.canteenUrlComponent,
            year: this.year,
            measure: this.tabHeaders[0].urlSlug,
          },
        })
      } else if (
        this.centralKitchenDiagnosticMode === "APPRO" &&
        this.measure !== approId &&
        this.measure !== "etablissement"
      ) {
        this.$router.replace({ name: "MyProgress", params: { measure: approId } })
      } else {
        this.tab = this.tabHeaders.indexOf(initialTab)
      }
    },
    usesSatelliteDiagnosticForMeasure(tabItem) {
      const tabAlwaysShown = tabItem.urlSlug === "qualite-des-produits" || tabItem.urlSlug === "etablissement"
      if (tabAlwaysShown) return false
      return this.isCentralKitchen && this.centralKitchenDiagnosticMode === "APPRO"
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
      this.initialiseTab()
    },
    centralKitchenDiagnosticMode(newMode) {
      if (!this.isCentralKitchen || !this.canteen) return
      if (!this.diagnostic || !this.diagnostic.id) return
      if (!newMode || this.diagnostic.centralKitchenDiagnosticMode === newMode) return
      this.diagnostic.centralKitchenDiagnosticMode = newMode
      this.$store.dispatch("updateDiagnostic", {
        canteenId: this.canteen.id,
        id: this.diagnostic.id,
        payload: { centralKitchenDiagnosticMode: newMode },
      })
      this.initialiseTab()
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
.cta-block {
  background: #f5f5fe;
  backdrop-filter: blur(7px);
  border: 1.5px dashed #000091;
  border-radius: 5px;
  color: #3a3a3a;
}
</style>
