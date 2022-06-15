<template>
  <div class="text-left pb-10">
    <h1 class="font-weight-black text-h4 my-4">
      Diagnostics
    </h1>
    <div v-if="orderedDiagnostics.length">
      <v-btn
        text
        color="primary"
        class="mt-2 mb-8 ml-n4"
        :to="{
          name: 'NewDiagnosticForCanteen',
          params: { canteenUrlComponent: $store.getters.getCanteenUrlComponent(originalCanteen) },
        }"
      >
        <v-icon class="mr-2">mdi-plus</v-icon>
        Ajouter un diagnostic
      </v-btn>
      <v-row>
        <v-col cols="12" v-for="diagnostic in orderedDiagnostics" :key="`diagnostic-${diagnostic.id}`">
          <DiagnosticCard :diagnostic="diagnostic" :canteen="originalCanteen" class="fill-height" />
        </v-col>
      </v-row>
      <PageSatisfaction class="mt-16" />
    </div>
    <div v-else>
      <DiagnosticIntroduction class="body-2"></DiagnosticIntroduction>
      <v-btn
        color="primary"
        class="mt-4"
        x-large
        :to="{
          name: 'NewDiagnosticForCanteen',
          params: { canteenUrlComponent: $store.getters.getCanteenUrlComponent(originalCanteen) },
        }"
      >
        Ajouter un diagnostic
      </v-btn>
    </div>
  </div>
</template>

<script>
import DiagnosticCard from "@/components/DiagnosticCard"
import PageSatisfaction from "@/components/PageSatisfaction"
import DiagnosticIntroduction from "@/components/DiagnosticIntroduction"

export default {
  name: "DiagnosticList",
  components: { DiagnosticCard, DiagnosticIntroduction, PageSatisfaction },
  props: {
    originalCanteen: Object,
  },
  computed: {
    orderedDiagnostics() {
      return [...this.originalCanteen.diagnostics].sort((a, b) => (a.year > b.year ? -1 : 1))
    },
  },
  created() {
    document.title = `Diagnostics - ${this.originalCanteen.name} - ${this.$store.state.pageTitleSuffix}`
  },
}
</script>
