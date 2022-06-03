<template>
  <v-card elevation="0" class="text-left">
    <v-card-title>
      <h1 class="font-weight-black text-h4 mb-4 mt-1">Changer mon mot de passe</h1>
    </v-card-title>

    <v-card-text>
      <v-form ref="form" v-model="formIsValid">
        <v-row>
          <v-col cols="12">
            <label for="actual" class="body-2 mb-1 mt-2 text-left">Mot de passe actuel</label>
            <v-text-field
              id="actual"
              type="password"
              :rules="[validators.required]"
              hide-details="auto"
              solo
              v-model="oldPassword"
              placeholder="Entrez votre mot de passe actuel"
            ></v-text-field>
          </v-col>
          <v-col cols="12">
            <label for="new" class="body-2 mb-1 mt-2 text-left">Nouveau mot de passe</label>
            <v-text-field
              id="new"
              type="password"
              :rules="[validators.required]"
              hide-details="auto"
              solo
              v-model="newPassword"
              placeholder="Entrez votre nouveau mot de passe"
            ></v-text-field>
          </v-col>
          <v-col cols="12">
            <label for="confirm" class="body-2 mb-1 mt-2 text-left">
              Confirmation de nouveau mot de passe
            </label>
            <v-text-field
              id="confirm"
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
        Valider
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
