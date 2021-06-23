<template>
  <v-dialog persistent max-width="1000" v-model="value" @click:outside="$emit('close')">
    <v-card>
      <div class="mb-4 pa-4 d-flex" style="background-color: #F5F5F5">
        <v-spacer></v-spacer>
        <v-btn color="primary" outlined @click="$emit('close')">
          Fermer
        </v-btn>
      </div>
      <v-card-text>
        <CanteenDashboard :diagnostics="diagnostics" />
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
import CanteenDashboard from "@/components/CanteenDashboard"
import Constants from "@/constants"

export default {
  name: "PublicationPreview",
  components: { CanteenDashboard },
  props: {
    canteen: {
      type: Object,
      required: true,
    },
    value: {
      type: Boolean,
      required: true,
    },
  },
  computed: {
    diagnostics() {
      const diagnostics = this.canteen.diagnostics
      return {
        previous:
          diagnostics.find((x) => x.year === 2019) || Object.assign({}, Constants.DefaultDiagnostics, { year: 2019 }),
        latest:
          diagnostics.find((x) => x.year === 2020) || Object.assign({}, Constants.DefaultDiagnostics, { year: 2020 }),
        provisionalYear1:
          diagnostics.find((x) => x.year === 2021) || Object.assign({}, Constants.DefaultDiagnostics, { year: 2021 }),
        provisionalYear2:
          diagnostics.find((x) => x.year === 2022) || Object.assign({}, Constants.DefaultDiagnostics, { year: 2022 }),
      }
    },
  },
}
</script>
