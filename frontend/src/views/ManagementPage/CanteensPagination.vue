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
      <v-col cols="12" sm="6" md="4" height="100%" class="d-flex flex-column">
        <v-card
          color="grey lighten-5"
          class="d-flex flex-column align-center justify-center"
          min-height="220"
          height="80%"
          :to="{ name: 'NewCanteen' }"
        >
          <v-icon size="100">mdi-plus</v-icon>
          <v-card-text class="font-weight-bold pt-0 text-center">
            Ajouter une cantine
          </v-card-text>
        </v-card>
        <v-spacer></v-spacer>
        <div class="d-flex mt-4 mb-2 align-center px-2">
          <v-divider></v-divider>
          <p class="mx-2 my-0 caption">ou</p>
          <v-divider></v-divider>
        </div>
        <v-spacer></v-spacer>
        <v-btn text color="primary" :to="{ name: 'DiagnosticsImporter' }">
          <v-icon class="mr-2">mdi-file-upload-outline</v-icon>
          Créer plusieurs cantines depuis un fichier
        </v-btn>
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
