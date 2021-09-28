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
          <DiagnosticCard :diagnostic="diagnostic" class="fill-height" />
        </v-col>
      </v-row>
    </div>
    <div v-else>
      <p class="body-2">
        Vous pouvez créer des diagnostics par année pour decouvrir les atouts ainsi que les points d'amélioration de
        votre cantine en relation des mesures de la loi EGAlim. Après creation, vos diagnostics vous permettront à
        publier vos données en repondant
        <router-link
          :to="{ name: 'KeyMeasurePage', params: { id: 'information-des-usagers' } }"
          class="text-decoration-underline primary--text"
        >
          la mesure d'information
        </router-link>
        .
      </p>
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
