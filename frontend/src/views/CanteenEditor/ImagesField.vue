<template>
  <v-row>
    <v-col v-for="image in imageArray" :key="image.image" class="d-flex child-flex" cols="12" sm="6" md="4">
      <v-card flat class="fill-height" style="overflow: hidden;">
        <v-img :src="image.image" contain aspect-ratio="1.4" style="overflow: hidden;" class="grey lighten-2"></v-img>
        <div style="position: absolute; top: 10px; left: 10px;">
          <v-btn fab small @click="deleteImage(image.image)">
            <v-icon aria-label="Supprimer" aria-hidden="false" color="red">$delete-line</v-icon>
          </v-btn>
        </div>
      </v-card>
    </v-col>

    <v-col cols="12" sm="6" md="4">
      <v-card class="fill-height" color="grey lighten-5" min-height="170">
        <label
          class="d-flex flex-column align-center justify-center"
          :for="uniqueId + '_image-input'"
          style="width: 100%; height: 100%; cursor: pointer;"
        >
          <v-icon class="align-center mb-2" lg>mdi-camera</v-icon>
          <div class="body-2 text-center font-weight-bold grey--text text--darken-2">Ajoutez une image</div>
        </label>
        <input
          :id="uniqueId + '_image-input'"
          multiple="multiple"
          accept="image/*"
          type="file"
          style="position: absolute; opacity: 0; width: 0.1px; height: 0.1px; overflow: hidden; z-index: -1;"
        />
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: "ImagesField",
  props: {
    imageArray: {
      type: Array,
      required: true,
    },
  },
  computed: {
    uniqueId() {
      return this.uid
    },
  },
  methods: {
    emitChange() {
      this.$emit("change", this.imageArray)
    },
    deleteImage(image) {
      this.$emit(
        "update:imageArray",
        this.imageArray.filter((x) => x.image !== image)
      )
      this.emitChange()
    },
    toBase64(file, success, error) {
      const reader = new FileReader()
      reader.readAsDataURL(file)
      reader.onload = function() {
        success(reader.result)
      }
      if (error) reader.onerror = error
    },
    addImages(e) {
      if (!e) return
      const files = e.target.files
      this.emitChange()

      for (let i = 0; i < files.length; i++) {
        const file = files[i]
        this.toBase64(file, (base64) => {
          if (this.imageArray.some((x) => x.image === base64)) return

          this.$emit(
            "update:imageArray",
            this.imageArray.concat({
              image: base64,
            })
          )
        })
      }
    },
  },
  mounted() {
    if (this.$el) {
      const domElement = this.$el.querySelector("#" + this.uniqueId + "_image-input")
      domElement.addEventListener("change", this.addImages)
    }
  },
  beforeDestroy() {
    this.$el.querySelector("#" + this.uniqueId + "_image-input").removeEventListener("change", this.addImages)
  },
}
</script>
