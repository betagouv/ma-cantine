<template>
  <div>
    <v-card elevation="0" class="text-center text-md-left mb-14 mt-6">
      <v-row v-if="$vuetify.breakpoint.smAndDown">
        <v-col cols="12">
          <v-img max-height="120px" contain src="/static/images/LovingDoodle.png"></v-img>
        </v-col>
      </v-row>
      <v-row>
        <v-spacer></v-spacer>
        <v-col cols="3" v-if="$vuetify.breakpoint.mdAndUp">
          <div class="d-flex fill-height align-center">
            <v-img max-height="140px" contain src="/static/images/LovingDoodle.png"></v-img>
          </div>
        </v-col>
        <v-col cols="12" sm="10" md="7">
          <v-card-title class="pr-0">
            <h1 class="font-weight-black text-h5 text-sm-h4">
              Découvrez les initiatives prises par nos cantines pour une alimentation saine, de qualité, et plus
              durable.
            </h1>
          </v-card-title>
        </v-col>
        <v-spacer></v-spacer>
      </v-row>
    </v-card>
    <div v-if="loading">
      <v-progress-circular indeterminate></v-progress-circular>
    </div>

    <div v-else>
      <v-pagination class="my-6" v-model="page" :length="Math.ceil(publishedCanteenCount / limit)"></v-pagination>
      <v-progress-circular class="my-10" indeterminate v-if="!visibleCanteens"></v-progress-circular>
      <v-row v-else>
        <v-col v-for="canteen in visibleCanteens" :key="canteen.id" style="height: auto;" cols="12" md="6">
          <PublishedCanteenCard :canteen="canteen" />
        </v-col>
      </v-row>
      <v-pagination
        class="my-6"
        v-model="page"
        :length="Math.ceil(publishedCanteenCount / limit)"
        v-if="$vuetify.breakpoint.smAndDown"
      ></v-pagination>
    </div>
  </div>
</template>

<script>
import PublishedCanteenCard from "./PublishedCanteenCard"
export default {
  data() {
    return {
      limit: 6,
      page: null,
    }
  },
  components: { PublishedCanteenCard },
  computed: {
    publishedCanteens() {
      return this.$store.state.publishedCanteens
    },
    publishedCanteenCount() {
      return this.$store.state.publishedCanteenCount
    },
    visibleCanteens() {
      const canteenPage = this.$store.state.publishedCanteens.find((x) => x.offset === this.offset)
      return canteenPage ? canteenPage.results : null
    },
    loading() {
      return this.publishedCanteenCount === null
    },
    offset() {
      return (this.page - 1) * this.limit
    },
  },
  methods: {
    fetchCurrentPage() {
      return this.$store.dispatch("fetchPublishedCanteens", { offset: this.offset })
    },
  },
  watch: {
    page(newPage) {
      // The empty catch is the suggested error management here : https://github.com/vuejs/vue-router/issues/2872#issuecomment-519073998
      this.$router.push({ query: { page: newPage } }).catch(() => {})
      if (!this.visibleCanteens) this.fetchCurrentPage()
    },
    $route(newRoute) {
      this.page = newRoute.query.page ? parseInt(newRoute.query.page) : 1
    },
  },
  mounted() {
    this.page = this.$route.query.page ? parseInt(this.$route.query.page) : 1
  },
}
</script>
