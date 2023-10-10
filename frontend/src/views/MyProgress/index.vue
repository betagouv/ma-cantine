<template>
  <div class="text-left">
    <BreadcrumbsNav :links="[{ to: { name: 'DashboardManager' }, title: canteen ? canteen.name : 'Dashboard' }]" />
    <h1 class="mb-10 fr-h2" v-if="canteen">{{ canteen.name }}</h1>
    <v-row>
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
        <DsfrTabsVue
          v-model="tab"
          :enableMobileView="$vuetify.breakpoint.smAndDown"
          mobileLabel="Volet de la loi EGAlim"
          :mobileSelectItems="mobileSelectItems"
          active-class="selected"
        >
          <template v-slot:tabs>
            <v-tab v-for="tabItem in tabHeaders" class="mx-1" :key="tabItem.text">
              <v-icon small class="mr-1">{{ tabItem.icon }}</v-icon>
              {{ tabItem.text }}
            </v-tab>
          </template>
          <template v-slot:items>
            <v-tab-item class="my-4" v-for="(item, index) in tabItems" :key="`${index}-content`">
              <component :is="item" :diagnostic="diagnostic" />
            </v-tab-item>
          </template>
        </DsfrTabsVue>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import BreadcrumbsNav from "@/components/BreadcrumbsNav.vue"
import DsfrTabsVue from "@/components/DsfrTabs"
import ApproProgress from "./ApproProgress"
import DiversificationProgress from "./DiversificationProgress"
import Inforogress from "./InfoProgress"
import PlasticProgress from "./PlasticProgress"
import WasteProgress from "./WasteProgress"
import CanteenProgress from "./CanteenProgress"
import DsfrSelect from "@/components/DsfrSelect"
import { diagnosticYears } from "@/utils"
import keyMeasures from "@/data/key-measures.json"

export default {
  name: "MyProgress",
  components: {
    BreadcrumbsNav,
    DsfrTabsVue,
    ApproProgress,
    DiversificationProgress,
    Inforogress,
    PlasticProgress,
    WasteProgress,
    CanteenProgress,
    DsfrSelect,
  },
  data() {
    return {
      tab: null,
      diagnostic: null,
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
      tabItems: [ApproProgress, WasteProgress, DiversificationProgress, PlasticProgress, Inforogress, CanteenProgress],
      canteen: null,
      years: diagnosticYears().map((x) => x.toString()),
    }
  },
  props: {
    canteenUrlComponent: {
      type: String,
    },
    year: {
      required: true,
    },
    measure: {
      required: true,
    },
  },
  computed: {
    mobileSelectItems() {
      return this.tabHeaders.map((x, index) => ({ text: x.text, value: index }))
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
        .then(this.assignDiagnostic)
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
    },
  },
  watch: {
    canteenUrlComponent() {
      this.canteen = null
      this.fetchCanteen()
    },
    tab() {
      if (this.$route.params.measure !== this.tabHeaders[this.tab].urlSlug)
        this.$router.replace({ params: { measure: this.tabHeaders[this.tab].urlSlug } })
    },
    year() {
      this.assignDiagnostic()
    },
    canteen() {
      this.assignDiagnostic()
    },
  },
  beforeMount() {
    this.fetchCanteen()
    const initialTab = this.tabHeaders.find((x) => x.urlSlug === this.measure)
    if (!initialTab) {
      this.$router.replace({
        name: this.$route.name,
        params: { canteenUrlComponent: this.canteenUrlComponent, year: this.year, measure: this.tabHeaders[0].urlSlug },
      })
      this.tab = 0
    } else this.tab = this.tabHeaders.indexOf(initialTab)
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
</style>
