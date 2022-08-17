<template>
  <v-card elevation="0" class="text-left">
    <v-card-title>
      <h1 class="font-weight-black text-h4 mb-4 mt-1">Mon compte</h1>
    </v-card-title>
    <v-card-subtitle class="mt-n1">Votre nom d'utilisateur : {{ userCopy.username }}</v-card-subtitle>
    <v-card-text>
      <v-form ref="form" v-model="formIsValid">
        <v-row>
          <v-col cols="12">
            <label for="photo" class="body-2 mt-2 text-left">Photo</label>
            <div>
              <v-avatar color="grey lighten-2" size="70" class="mr-4">
                <v-img :src="userCopy.avatar" v-if="userCopy.avatar"></v-img>
                <v-icon v-else>$account-circle-fill</v-icon>
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
              <input
                ref="uploader"
                class="d-none"
                type="file"
                accept="image/*"
                @change="onProfilePhotoChanged"
                id="photo"
              />
              <v-btn
                v-if="userCopy.avatar"
                text
                class="text-decoration-underline"
                color="red darken-2"
                small
                @click="changeProfileImage(undefined)"
              >
                <v-icon class="mr-1" small>mdi-delete-forever</v-icon>
                Supprimer
              </v-btn>
            </div>
          </v-col>
          <v-col cols="12" md="6">
            <DsfrTextField
              label="Prénom"
              class="mt-1"
              hide-details="auto"
              v-model="userCopy.firstName"
              :rules="[validators.required]"
              validate-on-blur
            />
          </v-col>
          <v-col cols="12" md="6">
            <DsfrTextField
              label="Nom"
              class="mt-1"
              hide-details="auto"
              v-model="userCopy.lastName"
              :rules="[validators.required]"
              validate-on-blur
            />
          </v-col>
          <v-col cols="12" md="6">
            <DsfrTextField
              label="Numéro téléphone"
              class="mt-1"
              hide-details="auto"
              v-model="userCopy.phoneNumber"
              :rules="[validators.isEmptyOrPhoneNumber]"
              validate-on-blur
            />
          </v-col>
          <v-col cols="12">
            <DsfrTextField
              label="Adresse email"
              class="mt-1"
              hide-details="auto"
              v-model="userCopy.email"
              :rules="[validators.email]"
              validate-on-blur
            />
          </v-col>
          <v-col cols="12" md="9">
            <label for="job" class="body-2 mt-2 text-left">Fonction</label>
            <DsfrSelect
              id="job"
              class="mt-1"
              v-model="userCopy.job"
              :items="jobOptions"
              :rules="[validators.required]"
              hide-details="auto"
              placeholder="Choisir une fonction"
            />
          </v-col>
          <v-col cols="12" v-if="showOtherJobField" class="my-0">
            <DsfrTextField
              label="Ma fonction"
              :rules="[validators.required]"
              v-model="userCopy.otherJobDescription"
              hide-details="auto"
            />
          </v-col>
          <v-col cols="12" md="9" v-if="!userCopy.hasMtmData">
            <label for="source" class="body-2 mt-2 text-left">Comment avez-vous connu ma-cantine ?</label>
            <DsfrSelect
              id="source"
              class="mt-1"
              v-model="userCopy.source"
              :items="sourceOptions"
              :rules="[validators.required]"
              hide-details="auto"
              placeholder="Choisir une option"
            />
          </v-col>
          <v-col cols="12" v-if="showOtherSourceField" class="my-0">
            <DsfrTextField
              label="Autre endroit"
              :rules="[validators.required]"
              v-model="userCopy.otherSourceDescription"
              hide-details="auto"
            />
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
import DsfrTextField from "@/components/DsfrTextField"
import DsfrSelect from "@/components/DsfrSelect"

export default {
  name: "AccountEditor",
  components: { DsfrTextField, DsfrSelect },
  data() {
    return {
      userCopy: {},
      formIsValid: true,
      avatarChanged: false,
      bypassLeaveWarning: false,
      jobOptions: Constants.Jobs,
      sourceOptions: Constants.UserSources,
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
    showOtherJobField() {
      return this.userCopy.job === "OTHER"
    },
    showOtherSourceField() {
      return this.userCopy.source === "OTHER"
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
