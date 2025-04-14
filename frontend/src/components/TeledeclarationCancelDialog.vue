<template>
  <v-dialog v-model="isOpen" width="500">
    <slot v-for="(_, name) in $slots" :name="name" :slot="name" />
    <template v-for="(_, name) in $scopedSlots" :slot="name" slot-scope="slotData">
      <slot :name="name" v-bind="slotData" />
    </template>

    <v-card class="text-left">
      <v-card-title>
        <h1 class="fr-h5 mb-2">Voulez-vous corriger votre télédéclaration pour l'année {{ diagnostic.year }} ?</h1>
      </v-card-title>

      <v-card-text>
        <p class="mb-0">
          L’action de correction annule la télédéclaration déjà en place pour vous permettre de modifier les valeurs de
          votre choix. Les informations sont pré-remplis avec vos dernières données. Une fois corrigée, vous devez
          soumettre de nouveau votre télédéclaration conformément à l'arrêté du 14 septembre 2022.
        </p>
      </v-card-text>

      <v-divider aria-hidden="true" role="presentation"></v-divider>

      <v-card-actions class="pa-4">
        <v-spacer></v-spacer>
        <v-btn outlined text @click="$emit('input', false)" class="mr-2">
          Revenir en arrière
        </v-btn>
        <v-btn outlined color="red darken-2" text @click="$emit('cancel')">
          Annuler et corriger ma télédéclaration
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
