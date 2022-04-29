<template>
  <v-card elevation="0" class="text-left">
    <v-card-title class="text-h5 font-weight-black">Mon compte</v-card-title>
    <v-card-subtitle class="mt-n1">Votre nom d'utilisateur : {{ userCopy.username }}</v-card-subtitle>
    <v-card-text>
      <v-form ref="form" v-model="formIsValid">
        <v-row>
          <v-col cols="12">
            <p class="body-2 mb-1 mt-2 text-left">Photo</p>
            <div>
              <v-avatar color="grey lighten-2" size="70" class="mr-4">
                <v-img :src="userCopy.avatar" v-if="userCopy.avatar"></v-img>
                <v-icon v-else>mdi-account</v-icon>
              </v-avatar>
              <v-btn
                text
                small
                class="mx-1 text-decoration-underline"
                color="primary"
                @click="onProfilePhotoUploadClick"
              >
                <v-icon class="mr-1" small>mdi-image</v-icon>
                Choisir une photo
              </v-btn>
              <input ref="uploader" class="d-none" type="file" accept="image/*" @change="onProfilePhotoChanged" />
              <v-btn
                v-if="userCopy.avatar"
                text
                class="text-decoration-underline"
                color="red"
                small
                @click="changeProfileImage(undefined)"
              >
                <v-icon class="mr-1" small>mdi-delete-forever</v-icon>
                Supprimer
              </v-btn>
            </div>
          </v-col>
          <v-col cols="12" md="6">
            <p class="body-2 mb-1 mt-2 text-left">Prénom</p>
            <v-text-field
              hide-details="auto"
              solo
              v-model="userCopy.firstName"
              :rules="[validators.required]"
              validate-on-blur
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="6">
            <p class="body-2 mb-1 mt-2 text-left">Nom</p>
            <v-text-field
              hide-details="auto"
              solo
              v-model="userCopy.lastName"
              :rules="[validators.required]"
              validate-on-blur
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="6">
            <p class="body-2 mb-1 mt-2 text-left">Numéro téléphone</p>
            <v-text-field
              hide-details="auto"
              solo
              v-model="userCopy.phoneNumber"
              :rules="[validators.isEmptyOrPhoneNumber]"
              validate-on-blur
            ></v-text-field>
          </v-col>
          <v-col cols="12">
            <p class="body-2 mb-1 mt-2 text-left">Adresse email</p>
            <v-text-field
              hide-details="auto"
              solo
              v-model="userCopy.email"
              :rules="[validators.email]"
              validate-on-blur
            ></v-text-field>
          </v-col>
        </v-row>
      </v-form>
    </v-card-text>
    <v-card-actions class="pa-4">
      <v-spacer></v-spacer>
      <v-btn x-large color="primary" @click="updateProfile" :loading="loading">
        Valider
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import validators from "@/validators"
import Constants from "@/constants"
import { toBase64, getObjectDiff } from "@/utils"

export default {
  name: "AccountEditor",
  data() {
    return {
      userCopy: {},
      formIsValid: true,
      avatarChanged: false,
      bypassLeaveWarning: false,
    }
  },
  computed: {
    validators() {
      return validators
    },
    hasChanged() {
      const diff = getObjectDiff(this.$store.state.loggedUser, this.userCopy)
      return Object.keys(diff).length > 0
    },
    loading() {
      return this.$store.state.userLoadingStatus === Constants.LoadingStatus.LOADING
    },
  },
  methods: {
    updateProfile() {
      this.$refs.form.validate()

      if (!this.formIsValid) {
        this.$store.dispatch("notifyRequiredFieldsError")
        return
      }

      const payload = getObjectDiff(this.$store.state.loggedUser, this.userCopy)
      const emailChanged = "email" in payload
      const message = `Votre profil a bien été mis à jour${
        emailChanged ? ". Vous recevrez un email pour confirmer votre nouvelle adresse." : "."
      }`
      this.$store
        .dispatch("updateProfile", { payload })
        .then(() => {
          this.bypassLeaveWarning = true
          this.$store.dispatch("notify", {
            title: "Mise à jour prise en compte",
            message,
            status: "success",
          })
          this.$router.push({ name: "ManagementPage" })
        })
        .catch((e) => {
          this.$store.dispatch("notifyServerError", e)
        })
    },
    onProfilePhotoUploadClick() {
      this.$refs.uploader.click()
    },
    onProfilePhotoChanged(e) {
      this.changeProfileImage(e.target.files[0])
    },
    changeProfileImage(file) {
      if (!file) {
        this.userCopy.avatar = null
        return
      }
      toBase64(file, (base64) => {
        this.$set(this.userCopy, "avatar", base64)
      })
    },
    handleUnload(e) {
      if (this.hasChanged && !this.bypassLeaveWarning) {
        e.preventDefault()
        e.returnValue = "Voulez-vous vraiment quitter cette page ? Votre profil n'a pas été sauvegardé."
      } else {
        delete e["returnValue"]
      }
    },
  },
  beforeMount() {
    const user = this.$store.state.loggedUser
    this.userCopy = JSON.parse(JSON.stringify(user))
  },
  created() {
    window.addEventListener("beforeunload", this.handleUnload)
  },
  beforeDestroy() {
    window.removeEventListener("beforeunload", this.handleUnload)
  },
}
</script>

<style scoped>
fieldset {
  border: none;
}
</style>
