<template>
  <div style="position: relative; display: inline-block;">
    <button
      class="d-block rounded-circle logo-container mr-6"
      @click="onLogoUploadClick"
      :title="logo ? 'Modifier le logo' : undefined"
    >
      <img v-if="logo" :src="logo" class="logo" alt="" />
      <v-icon v-if="!logo" color="primary">$add-line</v-icon>
      <span v-if="!logo" class="mb-0 fr-text-sm font-weight-bold primary--text d-block">Ajouter un logo</span>
    </button>
    <div v-if="logo" style="position: absolute; top: -6px; right: 14px;">
      <v-btn
        fab
        small
        @click.stop.prevent="changeLogo(null)"
        style="border: solid 2px #DDDDDD;"
        title="Supprimer le logo"
      >
        <v-icon color="red">$delete-line</v-icon>
      </v-btn>
    </div>
    <input ref="uploader" class="d-none" type="file" accept="image/*" @change="onLogoChanged" id="logo" />
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
  overflow: hidden;
}
.logo {
  object-fit: contain;
  max-height: 100%;
  max-width: 100%;
  height: 100%;
  width: 100%;
}
</style>
