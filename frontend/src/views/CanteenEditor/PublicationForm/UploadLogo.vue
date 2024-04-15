<template>
  <div style="position: relative">
    <button class="d-block rounded-circle logo-container mr-6" @click="onLogoUploadClick">
      <div>
        <input ref="uploader" class="d-none" type="file" accept="image/*" @change="onLogoChanged" id="logo" />
      </div>
      <div class="fill-height d-flex align-center justify-center rounded-circle" style="overflow: hidden;">
        <v-img v-if="logo" contain :src="logo"></v-img>
        <div v-else>
          <v-icon color="primary">$add-line</v-icon>
          <p class="mb-0 fr-text-sm font-weight-bold primary--text">Ajouter un logo</p>
        </div>
      </div>
    </button>
    <div v-if="logo" style="position: absolute; top: -6px; right: 14px;">
      <v-btn fab small @click.stop.prevent="changeLogo(null)" style="border: solid 2px #DDDDDD;">
        <v-icon aria-label="Supprimer logo" aria-hidden="false" color="red">$delete-line</v-icon>
      </v-btn>
    </div>
  </div>
</template>

<script>
import { toBase64 } from "@/utils"

export default {
  name: "UploadLogo",
  props: {
    canteen: {
      type: Object,
    },
  },

  methods: {
    onLogoChanged(e) {
      this.changeLogo(e.target.files[0])
    },
    changeLogo(file) {
      if (!file) {
        this.canteen.logo = null
        return
      }
      toBase64(file, (base64) => {
        this.$set(this.canteen, "logo", base64)
      })
    },
    onLogoUploadClick() {
      this.$refs.uploader.click()
    },
    saveLogo() {
      this.$store
        .dispatch("updateCanteen", {
          id: this.canteen.id,
          payload: { logo: this.canteen.logo },
        })
        .then(() => {
          this.$store.dispatch("notify", {
            title: "Le logo a été mis à jour",
            status: "success",
          })
        })
        .catch((e) => {
          this.$store.dispatch("notifyServerError", e)
        })
    },
  },
  computed: {
    logo() {
      return this.canteen.logo
    },
  },
  watch: {
    logo() {
      this.saveLogo()
      this.$emit("logoChanged", this.logo)
    },
  },
}
</script>

<style scoped>
.logo-container {
  aspect-ratio: 1 / 1;
  min-width: 124px;
  width: 124px;
  background-color: #f5f5fe;
  border: solid 2px #dddddd;
}
</style>
