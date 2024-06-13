<template>
  <v-row>
    <v-col v-for="image in imageArray.slice(start, end)" :key="image.image" class="d-flex child-flex" cols="12" sm="4">
      <v-card flat class="fill-height" style="overflow: hidden;">
        <v-img
          :src="image.image"
          contain
          aspect-ratio="1.4"
          height="216"
          style="overflow: hidden;"
          class="image-card"
        ></v-img>
        <div style="position: absolute; top: 4px; right: 4px;">
          <v-btn
            fab
            small
            @click.stop.prevent="deleteImage(image)"
            style="border: solid 2px #DDDDDD;"
            title="Supprimer"
          >
            <v-icon color="red">$delete-line</v-icon>
          </v-btn>
        </div>
        <DsfrTextarea
          v-model="image.altText"
          label="Description pour les personnes malvoyantes"
          hintText="Optionnel - Si l'image contient du texte, pensez à le répéter ici. Ce ne sera pas visible en légende."
          class="mt-2"
          rows="3"
          labelClasses="body-2 mt-4 mb-2"
          @focus="prepareAltEdit(image)"
          @blur="saveAlt(image)"
        />
      </v-card>
    </v-col>

    <v-col v-if="imageArray.length < end" cols="12" sm="4">
      <v-card class="fill-height drag-and-drop image-card" height="216">
        <label
          class="d-flex flex-column align-center justify-center"
          :for="uniqueId + '_image-input'"
          style="width: 100%; height: 100%; cursor: pointer;"
        >
          <v-icon class="align-center mb-2 primary--text" lg>$image-add-fill</v-icon>
          <p class="fr-text-sm text-center primary--text mb-0">Ajouter une image</p>
        </label>
        <input
          :id="uniqueId + '_image-input'"
          accept="image/*"
          type="file"
          style="position: absolute; opacity: 0; width: 0.1px; height: 0.1px; overflow: hidden; z-index: -1;"
          @change="addImage"
        />
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import DsfrTextarea from "@/components/DsfrTextarea"

export default {
  name: "ImagesField",
  props: {
    canteen: {
      type: Object,
      required: true,
    },
    start: {
      type: Number,
      default: 0,
    },
    end: {
      type: Number,
      default: 3,
    },
  },
  data() {
    return {
      imageArray: this.canteen.images,
    }
  },
  components: { DsfrTextarea },
  computed: {
    uniqueId() {
      return this.uid
    },
  },
  methods: {
    toBase64(file, success, error) {
      const reader = new FileReader()
      reader.readAsDataURL(file)
      reader.onload = function() {
        success(reader.result)
      }
      if (error) reader.onerror = error
    },
    deleteImage(image) {
      this.imageArray = this.imageArray.filter((x) => x.image !== image.image)
      this.saveImages("delete")
    },
    addImage(e) {
      if (!e) return
      const file = e.target.files[0]

      this.toBase64(file, (base64) => {
        if (this.imageArray.some((x) => x.image === base64)) {
          // this only stops the same image being added twice in the same session
          // if you save and come back it is still possible to add the same image because x.image
          // becomes the link to that image, and not the base64 rendering of it
          this.$store.dispatch("notify", { message: "L'image est déjà ajoutée" })
          return
        }

        this.imageArray = this.imageArray.concat({
          image: base64,
        })
        this.saveImages("add")
      })
    },
    prepareAltEdit(image) {
      image._oldAlt = image.altText
    },
    saveAlt(image) {
      if (!image._oldAlt && !image.altText) return
      if (image._oldAlt !== image.altText) this.saveImages("alt")
    },
    saveImages(action) {
      this.$store
        .dispatch("updateCanteen", {
          id: this.canteen.id,
          payload: { images: this.imageArray },
        })
        .then(() => {
          const message = {
            add: "L'image a été ajoutée",
            delete: "L'image est supprimée",
            modify: "L'image a été modifiée",
            alt: "Le texte a été mis à jour",
          }[action]
          this.$store.dispatch("notify", {
            title: message,
            status: "success",
          })
        })
        .catch((e) => {
          this.$store.dispatch("notifyServerError", e)
        })
    },
  },
}
</script>

<style scoped>
.image-card {
  background-color: #f5f5fe;
  border: solid 1px #dddddd;
}
</style>
