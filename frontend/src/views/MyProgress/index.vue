<template>
  <div class="text-left">
    <BreadcrumbsNav />
    <h1 class="mb-10 fr-h2" v-if="canteen">{{ canteen.name }}</h1>
    <v-row>
      <v-col cols="12" sm="3" md="2" style="border-right: 1px solid #DDD;">
        <h2 class="fr-h5">Ma progression</h2>
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
        <DsfrTabsVue :tabs="tabHeaders" active-class="selected">
          <template v-slot:tabs>
            <v-tab v-for="tab in tabHeaders" class="mx-1" :key="tab.text">
              <v-icon small class="mr-1">{{ tab.icon }}</v-icon>
              {{ tab.text }}
            </v-tab>
          </template>
          <template v-slot:items>
            <v-tab-item class="my-4" v-for="(item, index) in tabItems" :key="`${index}-content`">
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
        { text: "Appro.", icon: "mdi-food-apple" },
        { text: "Gaspillage", icon: "mdi-offer" },
        { text: "Protéines végétales", icon: "$leaf-fill" },
        { text: "Substit. plastiques", icon: "mdi-weather-windy" },
        { text: "Info. convives", icon: "mdi-bullhorn" },
        { text: "Établissement", icon: "$building-fill" },
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
