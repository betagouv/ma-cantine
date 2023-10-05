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
            <v-tab v-for="tab in tabHeaders" :key="`${tab}-header`">{{ tab }}</v-tab>
          </template>
          <template v-slot:items>
            <v-tab-item v-for="tab in tabHeaders" :key="`${tab}-content`">
              <v-card>
                <v-card-text>Hello {{ tab }}</v-card-text>
              </v-card>
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

export default {
  name: "MyProgress",
  components: { BreadcrumbsNav, DsfrTabsVue },
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
