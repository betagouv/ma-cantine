<template>
  <v-card class="text-left">
    <v-card-title>
      <h1 class="fr-h6 mb-0">
        {{ title }}
      </h1>
    </v-card-title>

    <v-card-text>
      <DsfrAutocomplete
        :items="canteens"
        :value="selectedCanteenId"
        item-text="name"
        item-value="id"
        placeholder="Sélectionnez une cantine"
        hide-details
        @input="onInput"
      />
    </v-card-text>

    <v-divider aria-hidden="true" role="presentation"></v-divider>

    <v-card-actions class="pa-4">
      <v-spacer></v-spacer>
      <v-btn outlined text @click="$emit('cancel')">
        Annuler
      </v-btn>
      <v-btn color="primary" :disabled="!selectedCanteen" @click="onConfirm">
        Valider
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import DsfrAutocomplete from "@/components/DsfrAutocomplete"

export default {
  name: "SelectCanteenCard",
  components: { DsfrAutocomplete },
  props: {
    title: {
      type: String,
      required: true,
    },
    canteens: {
      type: Array,
      required: true,
    },
    defaultCanteenId: {
      type: [Number, String],
      required: false,
      default: null,
    },
  },
  data() {
    return {
      selectedCanteenId: this.defaultCanteenId,
    }
  },
  computed: {
    selectedCanteen() {
      return this.canteens.find((c) => c.id === this.selectedCanteenId) || null
    },
  },
  watch: {
    defaultCanteenId(newId) {
      this.selectedCanteenId = newId
    },
  },
  methods: {
    onInput(value) {
      this.selectedCanteenId = value
    },
    onConfirm() {
      if (!this.selectedCanteen) return
      this.$emit("select", this.selectedCanteen)
    },
  },
}
</script>
