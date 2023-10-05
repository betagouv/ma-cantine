<template>
  <div class="text-left">
    <BreadcrumbsNav />
    <h1 class="mb-10 fr-h2" v-if="canteen">{{ canteen.name }}</h1>
    <v-row>
      <v-col cols="12" sm="3" md="2" style="border-right: 1px solid #DDD;">
        <div>Ma progression</div>
        <nav aria-label="Année du diagnostic" v-if="canteen">
          <v-list nav class="text-left">
            <v-list-item-group>
              <v-list-item v-for="year in years" :key="year">
                <v-list-item-title>{{ year }}</v-list-item-title>
              </v-list-item>
            </v-list-item-group>
          </v-list>
        </nav>
      </v-col>
      <v-col cols="12" sm="9" md="10">
        <DsfrTabsVue fixed-tabs :tabs="tabHeaders">
          <template v-slot:tabs>
            <v-tab v-for="tab in tabHeaders" :key="tab">{{ tab }}</v-tab>
          </template>
          <template v-slot:items>
            <v-tab-item v-for="(item, index) in tabItems" :key="`${index}-content`">
              <component :is="item" />
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
  },
  data() {
    return {
      tabHeaders: [
        "Appro.",
        "Gaspillage",
        "Protéines végétales",
        "Substit. plastiques",
        "Info. convives",
        "Établissement",
      ],
      tabItems: [ApproProgress, WasteProgress, DiversificationProgress, PlasticProgress, Inforogress, CanteenProgress],
      canteen: null,
      years: [2021, 2022, 2023, 2024],
    }
  },
  props: {
    canteenUrlComponent: {
      type: String,
      required: false,
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
  },
  watch: {
    canteenUrlComponent() {
      this.canteen = null
      this.fetchCanteen()
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
</style>
