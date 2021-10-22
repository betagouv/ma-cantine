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
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="6">
            <p class="body-2 mb-1 mt-2 text-left">Nom</p>
            <v-text-field
              hide-details="auto"
              solo
              v-model="userCopy.lastName"
              :rules="[validators.required]"
            ></v-text-field>
          </v-col>
          <v-col cols="12">
            <p class="body-2 mb-1 mt-2 text-left">Adresse email</p>
            <v-text-field hide-details="auto" solo v-model="userCopy.email" :rules="[validators.email]"></v-text-field>
          </v-col>
        </v-row>

        <v-row>
          <fieldset class="mt-3 mb-4">
            <legend class="body-2 ma-3 text-left">LAW_AWARENESS_DESCRIPTION</legend>

            <v-checkbox
              hide-details="auto"
              class="ml-8 mb-3 mt-0"
              v-model="userCopy.lawAwareness"
              :multiple="true"
              v-for="choice in lawAwarenessChoices"
              :key="choice.value"
              :value="choice.value"
              :label="choice.label"
              :readonly="readonly"
              :disabled="readonly"
            />
          </fieldset>
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
      lawAwarenessChoices: [
        {
          value: "NONE",
          label: "Je n’ai pas une connaissance détaillée de l’article 24 de la loi EGAlim",
        },
        {
          value: "AIMS_DEADLINES",
          label: "Je connais les objectifs et les échéances",
        },
        {
          value: "ELIGIBLE_LABELS",
          label: "Je connais la liste des labels éligibles et mentions valorisantes",
        },
        {
          value: "MY_LABELS",
          label:
            "J’ai accès aux informations ou mon prestataire me fournit les informations sur les labels éligibles et mentions valorisantes concernant mes achats",
        },
        {
          value: "SYSTEM",
          label:
            "J’ai un système de saisie formalisé (SI, Excel, papier) permettant de calculer et reporter le montant annuel de mes achats répondants aux exigences de l’article 24 de la loi EGALIM (N/A en gestion concédée)",
        },
        {
          value: "TAKEN_STOCK",
          label: "J’ai réalisé un état des lieux précis de mes approvisionnements",
        },
        {
          value: "OPTION_DIAGNOSTIC",
          label:
            "J’ai réalisé un diagnostic de l’offre (disponibilité et caractéristiques de l’offre des différents fournisseurs sur l’ensemble des catégories d’achats)",
        },
        {
          value: "ACTION_PLAN",
          label:
            "J’ai établi un plan d’actions pour tendre vers les objectifs de la loi EGALim, définissant notamment : le niveau d’ambition global et par catégories d’achats; les échéances de renouvellement de contrat avec clauses EGALim; le phasage de la progression des indicateurs EGAlim",
        },
        {
          value: "QUALITY_ACHIEVED",
          label:
            "J'ai atteint les objectifs de l’article 24 de la loi EGAlim de porter la part de produits de qualité et durables à 50% dont au moins 20% de produits issus de l'agriculture biologique",
        },
      ],
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
        .catch(() => {
          this.$store.dispatch("notifyServerError")
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
