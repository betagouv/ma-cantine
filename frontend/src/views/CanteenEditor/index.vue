<template>
  <div class="mt-n2">
    <v-row class="mt-2" v-if="isNewCanteen || canteen">
      <v-col cols="12" sm="4" md="3" v-if="showNavigation">
        <CanteenNavigation :canteen="canteen" />
      </v-col>
      <v-col v-else cols="12" class="py-0">
        <BreadcrumbsNav :links="breadcrumbLinks" />
      </v-col>
      <v-col
        cols="12"
        :sm="showNavigation ? 8 : 12"
        :md="showNavigation ? 9 : 12"
        :class="showNavigation ? '' : 'pt-0'"
      >
        <router-view @updateCanteen="updateCanteen" :originalCanteen="canteen" :year="year"></router-view>
      </v-col>
    </v-row>
    <v-container v-else>
      <v-progress-circular indeterminate style="position: absolute; left: 50%; top: 50%"></v-progress-circular>
    </v-container>
  </div>
</template>

<script>
import CanteenNavigation from "@/components/CanteenNavigation"
import BreadcrumbsNav from "@/components/BreadcrumbsNav"

export default {
  name: "CanteenEditor",
  components: { CanteenNavigation, BreadcrumbsNav },
  data() {
    return {
      canteen: null,
    }
  },
  props: {
    canteenUrlComponent: {
      type: String,
      required: false,
    },
    year: {
      required: false,
    },
  },
  computed: {
    isNewCanteen() {
      return !this.canteenUrlComponent
    },
    showNavigation() {
      return !this.isNewCanteen && !window.ENABLE_DASHBOARD
    },
    breadcrumbLinks() {
      if (this.isNewCanteen) return []
      return [{ to: { name: "DashboardManager" }, title: this.canteen.name }]
    },
  },
  methods: {
    updateCanteen(newCanteen) {
      this.$set(this, "canteen", newCanteen)
    },
    fetchCanteenIfNeeded() {
      if (this.isNewCanteen || this.canteen) return

      const id = this.canteenUrlComponent.split("--")[0]
      return this.$store
        .dispatch("fetchCanteen", { id })
        .then((canteen) => (this.canteen = canteen))
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
      this.fetchCanteenIfNeeded()
    },
  },
  beforeUpdate() {
    this.fetchCanteenIfNeeded()
  },
  beforeMount() {
    this.fetchCanteenIfNeeded()
  },
}
</script>

<style scoped>
/* for pages with left hand navigation we can make the width bigger */
.constrained {
  max-width: 1200px !important;
}
</style>
