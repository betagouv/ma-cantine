<template>
  <v-card color="grey lighten-5" class="fill-height my-10" height="300" width="300" elevation="0">
    <label
      class="d-flex flex-column align-center justify-center drop-area"
      for="csv-file-upload"
      style="cursor: pointer;"
      v-if="!hasFile"
      @dragover="onFileInputDragover"
      @dragleave="isDragging = false"
      @drop.prevent="onFileInputDrop"
    >
      <v-icon color="primary" size="90" v-if="isDragging">mdi-chevron-triple-down</v-icon>
      <v-icon color="primary" size="70" v-else>mdi-file-upload-outline</v-icon>
      <v-card-text class="font-weight-bold mt-2 pb-0 text-center text-body-2">
        <span v-if="isDragging">Déposez votre fichier</span>
        <span v-else>Choisissez un fichier ou glissez-le ici</span>
      </v-card-text>
      <v-card-subtitle v-if="!isDragging" class="text-center pt-2 text-caption">
        {{ subtitle }}
      </v-card-subtitle>
    </label>
    <v-file-input
      :disabled="hasFile"
      @change="onFileInputChange"
      id="csv-file-upload"
      :accept="acceptTypes.join(', ')"
      type="file"
      style="position: absolute; opacity: 0; width: 0.1px; height: 0.1px; overflow: hidden; z-index: -1;"
    />
    <div v-if="hasFile" class="d-flex flex-column align-center justify-center drop-area">
      <v-card-text class="font-weight-bold mt-3 mb-1 text-center text-body-2">
        <v-icon small class="mt-n1" color="primary">mdi-file-document-outline</v-icon>
        {{ value.name }}
      </v-card-text>

      <v-btn large color="primary" @click.stop="upload">Valider</v-btn>
      <v-btn large class="text-decoration-underline mt-5" text @click.stop="clearFile">
        Choisir un autre fichier
      </v-btn>
    </div>
  </v-card>
</template>

<script>
export default {
  name: "FileDrop",
  data() {
    return {
      isDragging: false,
    }
  },
  props: {
    acceptTypes: {
      type: Array,
    },
    subtitle: {
      required: true,
      type: String,
    },
    value: {
      type: File,
    },
  },
  computed: {
    hasFile() {
      return !!this.value
    },
  },
  methods: {
    onFileInputDragover(e) {
      const isCsv = this.acceptTypes.includes(e.dataTransfer?.items[0].type)
      if (isCsv) {
        e.preventDefault()
        this.isDragging = true
      }
    },
    onFileInputDrop(e) {
      const file = e.dataTransfer?.files[0]
      this.isDragging = false
      this.$emit("input", file)
    },
    onFileInputChange(file) {
      this.$emit("input", file)
    },
    clearFile() {
      this.$emit("input", null)
    },
    upload() {
      this.$emit("upload")
    },
  },
}
</script>

<style scoped>
.drop-area {
  width: 100%;
  height: 100%;
  border: 4px dashed #aaa;
  border-radius: 10px;
}
</style>
