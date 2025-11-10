<template>
  <div>
    <div v-if="isNewCanteen || canteen">
      <BreadcrumbsNav :links="breadcrumbLinks" />
      <router-view @updateCanteen="updateCanteen" :originalCanteen="canteen" :year="year"></router-view>
    </div>
    <v-container v-else>
      <v-progress-circular indeterminate style="position: absolute; left: 50%; top: 50%"></v-progress-circular>
    </v-container>
  </div>
</template>

<script>
import BreadcrumbsNav from "@/components/BreadcrumbsNav"

export default {
  name: "CanteenEditor",
  components: { BreadcrumbsNav },
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
    breadcrumbLinks() {
      if (this.isNewCanteen) return [{ to: { name: "GestionnaireTableauDeBord" } }]
      return [
        { to: { name: "GestionnaireTableauDeBord" } },
        { to: { name: "DashboardManager" }, title: this.canteen.name },
      ]
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
          this.$router.push({ name: "GestionnaireTableauDeBord" }).then(() => {
            this.$store.dispatch("notify", {
              message: "Nous n'avons pas trouvé cette cantine",
              status: "error",
            })
          })
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
