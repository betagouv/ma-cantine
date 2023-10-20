<template>
  <div class="text-left">
    <BreadcrumbsNav :links="[{ to: { name: 'DashboardManager' }, title: canteen ? canteen.name : 'Dashboard' }]" />
    <h1 class="mb-10 fr-h2" v-if="canteen">{{ canteen.name }}</h1>
    <v-row v-if="canteen">
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
            </v-tab-item>
          </template>
        </DsfrTabsVue>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import BreadcrumbsNav from "@/components/BreadcrumbsNav"
import ProgressTab from "./ProgressTab"
import DsfrTabsVue from "@/components/DsfrTabs"
import DsfrSelect from "@/components/DsfrSelect"
import { diagnosticYears } from "@/utils"
import keyMeasures from "@/data/key-measures.json"
import Constants from "@/constants"

export default {
  name: "MyProgress",
  components: {
    BreadcrumbsNav,
    ProgressTab,
    DsfrTabsVue,
    DsfrSelect,
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
          icon: x.mdiIcon,
          to: { params: { measure: x.id } },
        })),
        ...[
          {
            urlSlug: "etablissement",
            text: "Établissement",
            icon: "$building-fill",
            to: { params: { measure: "etablissement" } },
          },
        ],
      ],
      canteen: null,
      years: diagnosticYears().map((x) => x.toString()),
      centralKitchenDiagnosticModes: Constants.CentralKitchenDiagnosticModes,
      centralKitchenDiagnosticMode: null,
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
  opacity: 100%;
  background-color: #e5e5e5 !important;
  color: #929292 !important;
}
</style>
