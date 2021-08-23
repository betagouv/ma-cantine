<template>
  <div class="text-left pb-10">
    <h1 class="font-weight-black text-h4 my-4">
      Diagnostics
    </h1>
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
        <DiagnosticCard :diagnostic="diagnostic" class="fill-height" />
      </v-col>
    </v-row>
  </div>
</template>

<script>
import DiagnosticCard from "@/components/DiagnosticCard"

export default {
  name: "DiagnosticList",
  components: { DiagnosticCard },
  props: {
    originalCanteen: Object,
  },
  computed: {
    orderedDiagnostics() {
      return [...this.originalCanteen.diagnostics].sort((a, b) => (a.year > b.year ? -1 : 1))
    },
  },
  created() {
    document.title = `Diagnostics - ${this.originalCanteen.name} - ma-cantine.beta.gouv.fr`
  },
}
</script>
