<template>
  <div>
    <v-pagination
      v-if="showPagination"
      class="my-6"
      v-model="page"
      :length="Math.ceil(diagnostics.length / limit)"
    ></v-pagination>

    <div v-for="(item, index) in visibleDiagnostics" :key="item.diagnostic.id">
      <v-divider class="my-8" v-if="item.prependDivider && index != 0"></v-divider>
      <v-row>
        <v-col cols="12">
          <DiagnosticCard :diagnostic="item.diagnostic" :class="{ 'fill-height': $vuetify.breakpoint.mdAndUp }" />
        </v-col>
      </v-row>
    </div>
  </div>
</template>
<script>
import DiagnosticCard from "@/components/DiagnosticCard"
export default {
  name: "DiagnosticsPagination",
  components: { DiagnosticCard },
  props: {
    canteens: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      limit: 6,
      page: null,
    }
  },
  computed: {
    showPagination() {
      return this.diagnostics.length > this.limit
    },
    visibleDiagnostics() {
      const start = (this.page - 1) * this.limit
      const end = start + this.limit
      return this.diagnostics.slice(start, end)
    },
    diagnostics() {
      return this.canteens.flatMap((canteen) => {
        return canteen.diagnostics
          .sort((diag1, diag2) => diag2.year - diag1.year)
          .map((diagnostic, diagnosticIndex) => {
            return { diagnostic, prependDivider: diagnosticIndex === 0 }
          })
      })
    },
  },
  watch: {
    page(newPage) {
      // The empty catch is the suggested error management here : https://github.com/vuejs/vue-router/issues/2872#issuecomment-519073998
      this.$router.push({ query: { ...this.$route.query, ...{ diagnosticPage: newPage } } }).catch(() => {})
    },
    $route(newRoute) {
      this.page = newRoute.query.diagnosticPage ? parseInt(newRoute.query.diagnosticPage) : 1
    },
  },
  mounted() {
    this.page = this.$route.query.diagnosticPage ? parseInt(this.$route.query.diagnosticPage) : 1
  },
}
</script>
