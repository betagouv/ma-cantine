<template>
  <v-dialog v-model="isOpen" width="500">
    <template v-slot:activator="{ on, attrs }">
      <v-btn color="red darken-2" outlined v-bind="attrs" v-on="on">
        <v-icon small class="mr-2">mdi-alert</v-icon>
        Supprimer cette cantine
      </v-btn>
    </template>

    <v-card class="text-left">
      <v-card-title class="font-weight-bold">Voulez-vous vraiment supprimer « {{ canteen.name }} » ?</v-card-title>

      <v-card-text>
        Vous perdrez les données de cette cantine ainsi que celles des diagnostics associés.
      </v-card-text>

      <v-divider></v-divider>

      <v-card-actions class="pa-4">
        <v-spacer></v-spacer>
        <v-btn outlined text @click="$emit('input', false)" class="mr-2">
          Non, revenir en arrière
        </v-btn>
        <v-btn outlined color="red darken-2" text @click="$emit('delete')">
          Oui, supprimer ma cantine
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: "DeletionDialog",
  props: ["value", "canteen"],
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
