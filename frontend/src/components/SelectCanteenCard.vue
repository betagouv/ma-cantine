<template>
  <v-card class="text-left">
    <v-card-title>
      <h1 class="fr-h6 mb-0">
        {{ title }}
      </h1>
    </v-card-title>

    <v-card-text>
      <DsfrCombobox
        :items="canteens"
        item-text="name"
        item-value="id"
        :filter="canteenAutocomplete"
        placeholder="Sélectionnez une cantine"
        hide-details
        @input="onSelect"
      />
    </v-card-text>

    <v-divider aria-hidden="true" role="presentation"></v-divider>

    <v-card-actions class="pa-4">
      <v-spacer></v-spacer>
      <v-btn outlined text @click="$emit('cancel')">
        Annuler
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import { normaliseText } from "@/utils"
import DsfrCombobox from "@/components/DsfrCombobox"

export default {
  name: "SelectCanteenCard",
  components: { DsfrCombobox },
  props: {
    title: {
      type: String,
      required: true,
    },
    canteens: {
      type: Array,
      required: true,
    },
  },
  methods: {
    canteenAutocomplete(item, queryText) {
      if (!queryText) return true
      const normalizedQuery = normaliseText(queryText).toLocaleLowerCase()
      const normalizedItemText = normaliseText(item.name).toLocaleLowerCase()
      return normalizedItemText.includes(normalizedQuery)
    },
    onSelect(value) {
      const canteen = this.canteens.find((c) => c.id === value)
      if (!canteen) return
      this.$emit("select", canteen)
    },
  },
}
</script>
