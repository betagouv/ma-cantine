<template>
  <v-card elevation="0" class="text-left">
    <v-card-title class="text-h5 font-weight-black">Changer mon mot de passe</v-card-title>

    <v-card-text>
      <v-form ref="form" v-model="formIsValid">
        <v-row>
          <v-col cols="12">
            <p class="body-2 mb-1 mt-2 text-left">Mot de passe actuel</p>
            <v-text-field
              type="password"
              :rules="[validators.notEmpty]"
              hide-details="auto"
              solo
              v-model="oldPassword"
              placeholder="Entrez votre mot de passe actuel"
            ></v-text-field>
          </v-col>
          <v-col cols="12">
            <p class="body-2 mb-1 mt-2 text-left">Nouveau mot de passe</p>
            <v-text-field
              type="password"
              :rules="[validators.notEmpty]"
              hide-details="auto"
              solo
              v-model="newPassword"
              placeholder="Entrez votre nouveau mot de passe"
            ></v-text-field>
          </v-col>
          <v-col cols="12">
            <p class="body-2 mb-1 mt-2 text-left">
              Confirmation de nouveau mot de passe
            </p>
            <v-text-field
              type="password"
              hide-details="auto"
              solo
              v-model="newPasswordConfirmation"
              :rules="[validators.matchPassword]"
              validate-on-blur
              placeholder="Confirmez votre nouveau mot de passe"
            ></v-text-field>
          </v-col>
        </v-row>
      </v-form>
    </v-card-text>
    <v-card-actions class="pa-4">
      <v-spacer></v-spacer>
      <v-btn x-large color="primary" @click="changePassword">
        Enregistrer
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import validators from "@/validators"

export default {
  name: "PasswordChangeEditor",
  data() {
    return {
      oldPassword: "",
      newPassword: "",
      newPasswordConfirmation: "",
      formIsValid: true,
    }
  },
  computed: {
    validators() {
      const self = this
      return {
        ...validators,
        matchPassword: () => {
          const errorMessage = "Les deux mots de passe ne correspondent pas."
          return self.newPassword === self.newPasswordConfirmation ? true : errorMessage
        },
      }
    },
  },
  methods: {
    changePassword() {
      if (!this.$refs.form.validate()) {
        this.$store.dispatch("notifyRequiredFieldsError")
        return
      }

      const payload = {
        old_password: this.oldPassword,
        new_password_1: this.newPassword,
        new_password_2: this.newPasswordConfirmation,
      }

      this.$store
        .dispatch("changePassword", { payload })
        .then(() => {
          this.$store.dispatch("notify", {
            title: "Mise à jour prise en compte",
            message: "Votre mot de passe a bien été mis à jour",
            status: "success",
          })
          this.$router.push({ name: "ManagementPage" })
        })
        .catch((e) => {
          this.$store.dispatch("notify", {
            title: "Erreur",
            message: e.message || "Une erreur est survenue",
            status: "error",
          })
        })
    },
  },
}
</script>
