<template>
  <v-card outlined class="mt-4" v-if="comments">
    <v-alert class="mb-0 pa-2" color="indigo" colored-border border="left">
      <v-card-title class="pt-0 pb-1">
        <h3 class="font-weight-bold body-1 grey--text text--darken-3">
          Un petit mot du gestionnaire
        </h3>
      </v-card-title>
      <v-card-text class="pb-0 text-left grey--text text--darken-3 comments">
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

<style scoped>
.comments {
  white-space: pre-line;
}
</style>
