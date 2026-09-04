<template>
  <v-card color="grey lighten-5" class="fill-height my-10 d-flex flex-column" height="200" width="300" elevation="0">
    <v-spacer></v-spacer>
    <a :href="value" target="_blank" class="text-center">
      <v-icon color="primary" aria-label="Fichier PDF" role="img" aria-hidden="false" size="90" v-if="isPdf">
        mdi-file-pdf-box
      </v-icon>
      <v-icon color="primary" aria-label="Fichier" role="img" aria-hidden="false" size="90" v-else>
        mdi-file-outline
      </v-icon>
    </a>
    <div class="text-center">
      <v-btn text :href="value" target="_blank">
        <v-icon size="16" class="mr-2">mdi-eye-outline</v-icon>
        Voir le fichier
      </v-btn>

      <v-btn text @click="$emit('delete')">
        <v-icon size="16" class="mr-2">mdi-delete-outline</v-icon>
        Supprimer
      </v-btn>
    </div>
    <v-spacer></v-spacer>
  </v-card>
</template>

<script>
export default {
  name: "FilePreview",
  props: {
    subtitle: {
      type: String,
    },
    value: {
      type: String, // URL of the file
      required: true,
    },
    showRemoveButton: {
      default: true,
    },
  },
  computed: {
    isPdf() {
      return this.value.endsWith(".pdf")
    },
  },
  methods: {},
}
</script>
