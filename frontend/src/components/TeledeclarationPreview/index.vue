<template>
  <v-dialog v-model="isOpen" max-width="900">
    <v-card>
      <!-- maybe make dialog fullscreen for xs (and s) ? -->
      <v-row align="center" class="pt-4 mx-0" v-if="diagnostics && diagnostics.length > 1">
        <v-col cols="6" sm="8" md="9" class="pb-1">
          <v-progress-linear :value="(idx / diagnostics.length) * 100" rounded height="6"></v-progress-linear>
        </v-col>
        <v-col class="text-right pb-1">
          <p class="caption my-0">{{ idx }} / {{ diagnostics.length }} diagnostics télédéclarés</p>
        </v-col>
      </v-row>
      <SingleView :canteen="canteenForTD" :diagnostic="diagnosticForTD" @teledeclare="teledeclare" @close="close" />
    </v-card>
  </v-dialog>
</template>

<script>
import SingleView from "./SingleView"

export default {
  components: { SingleView },
  props: {
    value: {
      required: true,
    },
    diagnostic: Object,
    canteen: Object,
    diagnostics: Array,
  },
  data() {
    return {
      idx: 0,
    }
  },
  computed: {
    isOpen: {
      get() {
        return this.value && this.canteenForTD
      },
      set(newValue) {
        this.$emit("input", newValue)
      },
    },
    canteenForTD() {
      return this.canteen || this.diagnosticForTD?.canteen
    },
    diagnosticForTD() {
      if (this.diagnostics) return this.diagnostics[this.idx]
      return this.diagnostic
    },
  },
  methods: {
    teledeclare() {
      const keepDialog = !this.diagnostics || this.idx + 1 < this.diagnostics.length
      this.$emit("teledeclare", this.diagnosticForTD, keepDialog)
      this.idx++
    },
    close() {
      this.$emit("input", false)
    },
  },
}
</script>
