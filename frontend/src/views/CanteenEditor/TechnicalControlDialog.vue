<template>
  <v-dialog v-model="dialogOpen" max-width="500">
    <v-card class="text-left pa-1">
      <v-card-title class="font-weight-bold">Vérification</v-card-title>
      <v-card-text class="grey--text text--darken-3">{{ bodyText }}</v-card-text>
      <v-divider></v-divider>

      <v-card-actions class="pa-3">
        <v-spacer></v-spacer>
        <v-btn outlined text @click="onCancel" class="mr-2">
          Non, revenir en arrière
        </v-btn>
        <v-btn outlined color="primary" text @click="onConfirm">
          Oui, sauvegarder ma cantine
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: "TechnicalControlDialog",
  props: ["bodyText", "value"],
  methods: {
    onCancel() {
      if (this.$matomo) {
        this.$matomo.trackEvent("canteen", "modification", "technical-control-cancel")
      }
      this.$emit("input", false)
    },
    onConfirm() {
      if (this.$matomo) {
        this.$matomo.trackEvent("canteen", "modification", "technical-control-save")
      }
      this.$emit("save")
    },
  },
  computed: {
    dialogOpen: {
      get() {
        return this.value
      },
      set(newValue) {
        this.$emit("input", newValue)
      },
    },
  },
}
</script>
