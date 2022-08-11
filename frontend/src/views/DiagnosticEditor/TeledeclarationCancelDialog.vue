<template>
  <v-dialog v-model="isOpen" width="500">
    <template v-slot:activator="{ on, attrs }">
      <v-btn class="text-caption mb-4 px-0" x-small text plain v-bind="attrs" v-on="on">
        <v-icon x-small class="mr-1">mdi-close</v-icon>
        Annuler ma télédéclaration
      </v-btn>
    </template>

    <v-card class="text-left">
      <v-card-title class="font-weight-bold">
        Voulez-vous vraiment annuler votre télédéclaration pour l'année {{ diagnostic.year }} ?
      </v-card-title>

      <v-card-text>
        En l'annulant vous devrez soumettre à nouveau une télédéclaration pour {{ diagnostic.year }}
        conformément à l'article 24 de la loi EGAlim.
      </v-card-text>

      <v-divider></v-divider>

      <v-card-actions class="pa-4">
        <v-spacer></v-spacer>
        <v-btn outlined text @click="$emit('input', false)" class="mr-2">
          Non, revenir en arrière
        </v-btn>
        <v-btn outlined color="red darken-2" text @click="$emit('cancel')">
          Oui, annuler ma télédéclaration
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: "TeledeclarationCancelDialog",
  props: ["value", "diagnostic"],
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
