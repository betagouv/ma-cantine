<template>
  <v-dialog
    persistent
    max-width="1000"
    :value="value"
    @input="value = $event.target.value"
    @click:outside="$emit('close')"
  >
    <v-card>
      <div class="mb-4 pa-4 d-flex" style="background-color: #F5F5F5">
        <v-spacer></v-spacer>
        <v-btn color="primary" outlined @click="$emit('close')">
          Fermer
        </v-btn>
      </div>
      <v-card-text>
        <CanteenPublication :canteen="canteen" />
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
import CanteenPublication from "@/components/CanteenPublication"

export default {
  name: "PublicationPreview",
  components: { CanteenPublication },
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
}
</script>
