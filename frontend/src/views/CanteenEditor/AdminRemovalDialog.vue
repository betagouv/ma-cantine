<template>
  <v-dialog v-model="isOpen" width="500">
    <template v-slot:activator="{ on, attrs }">
      <v-btn color="red" x-small fab outlined v-bind="attrs" v-on="on">
        <v-icon aria-hidden="false" title="Enlever">$delete-fill</v-icon>
      </v-btn>
    </template>

    <v-card class="text-left">
      <v-card-title>
        <h1 class="fr-h5 mb-2">Voulez-vous enlever {{ manager.email }} de la liste de gestionnaires ?</h1>
      </v-card-title>

      <v-card-text>
        <p class="mb-0">
          <span v-if="manager.firstName || manager.lastName">{{ manager.firstName }} {{ manager.lastName }}</span>
          <span v-else>Cette personne</span>
          n'aura plus accès à cette cantine et ne sera plus en mesure d'en apporter des modifications ni de créer des
          diagnostics.
        </p>
      </v-card-text>

      <v-divider aria-hidden="true" role="presentation"></v-divider>

      <v-card-actions class="pa-4">
        <v-spacer></v-spacer>
        <v-btn outlined text @click="$emit('input', false)" class="mr-2">
          Non, revenir en arrière
        </v-btn>
        <v-btn outlined color="red darken-2" text @click="$emit('delete')">
          Oui, enlever {{ manager.firstName }} {{ manager.lastName }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: "AdminRemovalDialog",
  props: ["value", "manager"],
  computed: {
    isOpen: {
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
