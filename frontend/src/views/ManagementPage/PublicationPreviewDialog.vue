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
        <CanteenDashboard :diagnostics="diagnostics" :canteen="canteen" />
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
import CanteenDashboard from "@/components/CanteenDashboard"
import { diagnosticsMap } from "@/utils"

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
      return diagnosticsMap(this.canteen.diagnostics)
    },
  },
}
</script>
