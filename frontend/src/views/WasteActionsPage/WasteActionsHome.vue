<template>
  <div id="wasteactions-home" class="text-left">
    <BreadcrumbsNav />
    <h1 class="fr-h1 mb-4">
      Lutter contre le gaspillage alimentaire
    </h1>
    <div v-if="loading" class="mt-8">
      <v-progress-circular indeterminate></v-progress-circular>
    </div>
    <div v-else-if="wasteActions.length > 0">
      <v-row class="pa-2 mt-2">
        <v-col vols="12" sm="6" md="4" v-for="wasteAction in wasteActions" :key="wasteAction.id">
          <WasteActionCard :wasteAction="wasteAction" />
        </v-col>
      </v-row>
      <DsfrPagination class="my-6" v-model="page" :length="Math.ceil(wasteActionsCount / limit)" />
    </div>
    <div v-else>
      <p>
        Contenu en cours de construction
      </p>
    </div>
  </div>
</template>
<script>
import WasteActionCard from "./WasteActionCard"
import DsfrPagination from "@/components/DsfrPagination"
import BreadcrumbsNav from "@/components/BreadcrumbsNav"

export default {
  name: "WasteActionsHome",
  components: { WasteActionCard, DsfrPagination, BreadcrumbsNav },
  data() {
    return {
      limit: 6,
      page: null,
      wasteActions: [],
      wasteActionsCount: null,
    }
  },
  computed: {
    loading() {
      return this.wasteActionsCount === null
    },
    offset() {
      return (this.page - 1) * this.limit
    },
  },

  methods: {
    fetchCurrentPage() {
      this.$store
        .dispatch("fetchWasteActions", {
          offset: this.offset,
          limit: this.limit,
        })
        .then((response) => {
          this.wasteActions = response.items
          this.wasteActionsCount = response.meta.totalCount
        })
        .catch(() => {
          this.$store.dispatch("notifyServerError")
        })
    },
    updateRoute() {
      let query = { page: this.page }
      // The empty catch is the suggested error management here : https://github.com/vuejs/vue-router/issues/2872#issuecomment-519073998
      if (this.$route.query.page) {
        this.$router.push({ query }).catch(() => {})
      } else {
        this.$router.replace({ query }).catch(() => {})
      }
    },
  },
  watch: {
    page() {
      this.updateRoute()
    },
    $route() {
      this.fetchCurrentPage()
    },
  },
  mounted() {
    this.page = this.$route.query.page ? parseInt(this.$route.query.page) : 1
    this.fetchCurrentPage()
  },
}
</script>
