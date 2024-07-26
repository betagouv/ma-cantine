<template>
  <div id="wasteactions-home">
    <div v-if="loading" class="mt-8">
      <v-progress-circular inderterminate></v-progress-circular>
    </div>
    <div v-if="!loading && wasteactions.length > 0">
      <h1>Explorez et mettez en avant vos actions de lutte contre le gaspillage</h1>
      <DsfrPagination class="my-6" v-model="page" :length="Math.ceil(wasteactionsCount / limit)" />
      <v-row class="cta-group pa-2 mt-2">
        <v-col vols="12" sm="6" md="4" v-for="wasteaction in wasteactions" :key="wasteaction.id">
          <WasteActionCard :wasteaction="wasteaction" />
        </v-col>
      </v-row>
      <DsfrPagination
        class="my-6"
        v-model="page"
        :length="Math.ceil(wasteactionsCount / limit)"
        v-if="$vuetify.breakpoint.smAndDown"
      />
    </div>
  </div>
</template>
<script>
import WasteActionCard from "./WasteActionCard.vue"
import DsfrPagination from "@/components/DsfrPagination.vue"

export default {
  name: "WasteActionsHome",
  components: { WasteActionCard, DsfrPagination },
  data() {
    return {
      limit: 6,
      page: null,
      tag: null,
      searchTerm: null,
      wasteactions: [],
      wasteactionsCount: null,
    }
  },
  computed: {
    loading() {
      return this.wasteactionsCount === null
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
          tag: this.tag,
          search: this.searchTerm,
          limit: this.limit,
        })
        .then((response) => {
          this.wasteactions = response.items
          this.wasteactionsCount = response.meta.total_count
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
