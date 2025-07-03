<template>
  <v-dialog persistent max-width="1000" v-model="value" @click:outside="$emit('input', false)">
    <v-sheet class="pa-8 text-left">
      <h1 class="fr-h3">
        Créez votre cantine
      </h1>
      <p>
        Cliquez sur l'établissement qui correspond à votre cantine
      </p>
      <div class="mt-4">
        <v-card
          outlined
          v-for="organization in organizations"
          :key="organization.id"
          class="text-left mb-4"
          :to="{ name: 'GestionnaireCantineAjouter' }"
        >
          <v-card-title>
            <h2 class="fr-h6 mb-0">{{ organization.label }}</h2>
          </v-card-title>
          <v-card-text>
            <p class="mb-0">SIRET : {{ organization.siret }}</p>
          </v-card-text>
        </v-card>
        <v-divider aria-hidden="true" role="presentation" class="mb-4"></v-divider>
        <v-card outlined class="text-left mb-4" :to="{ name: 'GestionnaireCantineAjouter' }">
          <v-card-title><h2 class="fr-h6 mb-0">Créer un autre établissement</h2></v-card-title>
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
