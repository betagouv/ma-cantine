<template>
  <v-card outlined class="mt-4" v-if="comments">
    <v-alert class="mb-0 pa-2" color="secondary" colored-border border="left">
      <v-card-title class="pt-0 pb-1">
        <h3 class="font-weight-bold text-h6 grey--text text--darken-3">
          Le gestionnaire dit ...
        </h3>
      </v-card-title>
      <v-card-text class="pb-0 text-left grey--text text--darken-3">
        {{ comments }}
      </v-card-text>
    </v-alert>
  </v-card>
</template>

<script>
export default {
  name: "PublicationComment",
  props: {
    comments: {
      type: String,
      required: false,
    },
  },
}
</script>
