<template>
  <v-dialog persistent max-width="1000" v-model="value" @click:outside="$emit('input', false)">
    <v-sheet class="pa-8 text-left">
      <h2 class="font-weight-black">
        Créez votre cantine
      </h2>
      <p>
        Cliquez sur l'établissement qui correspond à votre cantine
      </p>
      <div class="mt-4">
        <v-card outlined v-for="organization in organizations" :key="organization.id" class="text-left mb-4">
          <v-card-title>{{ organization.label }}</v-card-title>
          <v-card-text>SIRET : {{ organization.siret }}</v-card-text>
        </v-card>
        <v-divider class="mb-4"></v-divider>
        <v-card outlined class="text-left mb-4">
          <v-card-title>Créer un autre établissement</v-card-title>
        </v-card>
      </div>
      <div class="d-flex">
        <v-spacer />
        <v-btn color="primary" @click="$emit('input', false)">Fermer</v-btn>
      </div>
    </v-sheet>
  </v-dialog>
</template>

<script>
export default {
  name: "CanteenCreationDialog",
  props: {
    value: {
      type: Boolean,
      required: true,
    },
    organizations: {
      type: Array,
      required: true,
    },
  },
}
</script>
