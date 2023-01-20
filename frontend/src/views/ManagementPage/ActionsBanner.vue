<template>
  <v-card outlined class="mb-4">
    <v-card-text class="pb-0 grey--text text--darken-4">
      Cliquez ci-dessous pour regarder l'état de toutes vos cantines et les actions à faire pour chacune.
    </v-card-text>
    <v-card-text class="">
      <v-btn :to="{ name: 'PendingActions' }" color="primary">Mes actions</v-btn>
    </v-card-text>
  </v-card>
</template>
