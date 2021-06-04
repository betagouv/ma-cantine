<template>
  <div>
    <v-card outlined tile class="d-flex pa-4 flex-wrap flex-md-nowrap justify-center">
      <v-btn exact :to="{ name: 'CanteenInfo' }" text small>
        Cantine
      </v-btn>

      <v-btn
        exact
        :to="{ name: 'PublishMeasurePage', params: { id: measure.id } }"
        text
        small
        v-for="measure in keyMeasures"
        :key="measure.id"
      >
        {{ measure.shortTitle }}
      </v-btn>

      <v-btn exact :to="{ name: 'SubmitPublicationPage' }" text small>
        Publication
      </v-btn>
    </v-card>

    <div id="router-view" class="pa-4 mt-8">
      <router-view :key="$route.fullPath" :routeProps="routeProps" />
    </div>
  </div>
</template>

<script>
import Constants from "@/constants"
import keyMeasures from "@/data/key-measures.json"

export default {
  data() {
    return {
      keyMeasures,
    }
  },
  methods: {},
  computed: {
    userCanteen() {
      return this.$store.state.userCanteens[0]
    },
    diagnostics() {
      return this.userCanteen.diagnostics
    },
    routeProps() {
      const canteenCopy = JSON.parse(JSON.stringify(this.userCanteen))
      const diagnosticsCopy = JSON.parse(JSON.stringify(this.diagnostics))
      const diagnostics = {
        previous:
          diagnosticsCopy.find((x) => x.year === 2019) ||
          Object.assign({}, Constants.DefaultDiagnostics, { year: 2019 }),
        latest:
          diagnosticsCopy.find((x) => x.year === 2020) ||
          Object.assign({}, Constants.DefaultDiagnostics, { year: 2020 }),
        provisionalYear1:
          diagnosticsCopy.find((x) => x.year === 2021) ||
          Object.assign({}, Constants.DefaultDiagnostics, { year: 2021 }),
        provisionalYear2:
          diagnosticsCopy.find((x) => x.year === 2022) ||
          Object.assign({}, Constants.DefaultDiagnostics, { year: 2022 }),
      }
      return this.$route.name === "PublishMeasurePage" ? diagnostics : canteenCopy
    },
  },
}
</script>
