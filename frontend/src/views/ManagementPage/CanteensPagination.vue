<template>
  <div>
    <v-pagination
      v-if="showPagination"
      class="my-6"
      v-model="page"
      :length="Math.ceil(canteens.length / limit)"
    ></v-pagination>
    <v-row>
      <v-col cols="12" sm="6" md="4" height="100%" v-for="canteen in visibleCanteens" :key="`canteen-${canteen.id}`">
        <CanteenCard :canteen="canteen" class="fill-height" />
      </v-col>
      <v-col cols="12" sm="6" md="4" height="100%">
        <v-card
          color="grey lighten-5"
          class="fill-height d-flex flex-column align-center justify-center"
          min-height="280"
          :to="{ name: 'NewCanteen' }"
        >
          <v-icon size="100">mdi-plus</v-icon>
          <v-card-text class="font-weight-bold pt-0 text-center">
            Ajouter une cantine
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import CanteenCard from "./CanteenCard"

export default {
  name: "CanteensPagination",
  components: { CanteenCard },
  props: {
    canteens: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      limit: 5,
      page: null,
    }
  },
  computed: {
    showPagination() {
      return this.canteens.length > this.limit
    },
    visibleCanteens() {
      const start = (this.page - 1) * this.limit
      const end = start + this.limit
      return this.canteens.slice(start, end)
    },
  },
  watch: {
    page(newPage) {
      // The empty catch is the suggested error management here : https://github.com/vuejs/vue-router/issues/2872#issuecomment-519073998
      this.$router.push({ query: { ...this.$route.query, ...{ cantinePage: newPage } } }).catch(() => {})
    },
    $route(newRoute) {
      this.page = newRoute.query.cantinePage ? parseInt(newRoute.query.cantinePage) : 1
    },
  },
  mounted() {
    this.page = this.$route.query.cantinePage ? parseInt(this.$route.query.cantinePage) : 1
  },
}
</script>
