<template>
  <v-row>
    <!-- TODO: decide what to do with canteens that already have more than 3 images, if they exist (check they do first) -->
    <!-- there are 80 canteens with >3 images -->
    <!-- TODO: show three add image squares -->
    <!-- TODO: mobile view -->
    <!-- TODO: when there is an image uploaded, add modify option to be like logo field -->
    <!-- TODO: how to label upload field(s) to be accessible? How to label delete and modify buttons when have multiple images?-->
    <!-- TODO: focus management for keyboard nav -->
    <v-col v-for="image in imageArray.slice(0, 3)" :key="image.image" class="d-flex child-flex" cols="12" sm="6" md="4">
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
          label="Description de l'image"
          hint="Si l'image contient de l'information pertinente, pensez à ajouter une description pour les personnes malvoyantes"
          class="mt-2"
          rows="3"
          labelClasses="body-2 mt-4 mb-2"
          @blur="saveAlt(image)"
        />
      </v-card>
    </v-col>

    <v-col v-if="imageArray.length < 3" cols="12" sm="6" md="4">
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
    saveAlt() {
      // TODO: only save (or only show save message) if alt text has changed
      this.saveImages("alt")
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
