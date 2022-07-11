<template>
  <div>
    <v-row>
      <v-col cols="12">
        <h2 class="font-weight-black text-h5 mb-4">Foire aux questions</h2>
        <p>
          Consultez les résponses aux questions les plus fréquentes.
        </p>
        <v-btn outlined color="primary" large :to="{ name: 'FaqPage' }">
          <v-icon class="mr-2">mdi-help-circle</v-icon>
          Consulter la FAQ
        </v-btn>
      </v-col>
    </v-row>
  </div>
</template>
