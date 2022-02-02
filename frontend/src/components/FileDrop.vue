<template>
  <v-card
    color="grey lighten-5"
    class="fill-height my-10"
    height="300"
    width="300"
    elevation="0"
    :tabindex="hasFile ? undefined : 0"
    @keydown.enter="openFileChooser"
  >
    <label
      class="d-flex flex-column align-center justify-center drop-area"
      :for="uploadId"
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
      <v-card-subtitle v-if="!isDragging && subtitle" class="text-center pt-2 text-caption">
        {{ subtitle }}
      </v-card-subtitle>
    </label>
    <div v-if="hasFile" class="d-flex flex-column align-center justify-center drop-area">
      <v-card-text class="font-weight-bold mt-3 mb-1 text-center text-body-2">
        <v-icon small class="mt-n1" color="primary">mdi-file-document-outline</v-icon>
        {{ value.name }}
      </v-card-text>

      <v-btn large color="primary" @click.stop="upload" :disabled="disabled" v-if="showUploadButton">
        {{ submitText }}
      </v-btn>
      <v-btn large class="text-decoration-underline mt-5" text @click.stop="clearFile" :disabled="disabled">
        Choisir un autre fichier
      </v-btn>
    </div>
    <input
      class="visually-hidden"
      :disabled="hasFile"
      :ref="uploadId"
      @change="onFileInputChange"
      :id="uploadId"
      :accept="acceptTypes.join(', ')"
      type="file"
    />
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
      type: String,
    },
    maxSize: {
      required: false,
    },
    value: {
      type: File,
    },
    showUploadButton: {
      default: true,
    },
    disabled: Boolean,
    uploadId: {
      default: "csv-file-upload",
    },
    submitText: {
      default: "Valider",
    },
  },
  computed: {
    hasFile() {
      return !!this.value
    },
  },
  methods: {
    onFileInputDragover(e) {
      if (this.disabled) return
      const isCsv = this.acceptTypes.includes(e.dataTransfer?.items[0].type)
      if (isCsv) {
        e.preventDefault()
        this.isDragging = true
      }
    },
    onFileInputDrop(e) {
      if (this.disabled) return
      const file = e.dataTransfer?.files[0]
      this.isDragging = false
      if (this.sizeIsValid(file)) this.$emit("input", file)
      else this.clearFile()
    },
    onFileInputChange(e) {
      if (this.disabled) return
      const file = e.target.files[0]
      if (this.sizeIsValid(file)) this.$emit("input", file)
      else this.clearFile()
    },
    clearFile() {
      if (this.disabled) return
      this.$emit("input", null)
    },
    upload() {
      if (this.disabled) return
      this.$emit("upload")
    },
    openFileChooser() {
      if (this.disabled) return
      if (!this.hasFile) this.$refs["csv-file-upload"].click()
    },
    sizeIsValid(file) {
      if (!this.maxSize) return true
      const sizeIsValid = parseInt(file.size) < this.maxSize
      if (!sizeIsValid) window.alert("Ce fichier est trop grand, merci d'utiliser un fichier de moins de 10Mo")
      return sizeIsValid
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
.visually-hidden {
  clip: rect(0 0 0 0);
  clip-path: inset(50%);
  height: 1px;
  overflow: hidden;
  position: absolute;
  white-space: nowrap;
  width: 1px;
}
.v-card:focus {
  background-color: #f0f0f0 !important;
}
</style>
