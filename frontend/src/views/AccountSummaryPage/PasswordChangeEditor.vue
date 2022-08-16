<template>
  <v-card elevation="0" class="text-left">
    <v-card-title>
      <h1 class="font-weight-black text-h4 mb-4 mt-1">Changer mon mot de passe</h1>
    </v-card-title>

    <v-card-text>
      <v-form ref="form" v-model="formIsValid">
        <v-row>
          <v-col cols="12">
            <DsfrTextField
              label="Mot de passe actuel"
              type="password"
              :rules="[validators.required]"
              hide-details="auto"
              v-model="oldPassword"
              placeholder="Entrez votre mot de passe actuel"
            />
          </v-col>
          <v-col cols="12">
            <DsfrTextField
              label="Nouveau mot de passe"
              type="password"
              :rules="[validators.required]"
              hide-details="auto"
              v-model="newPassword"
              placeholder="Entrez votre nouveau mot de passe"
            />
          </v-col>
          <v-col cols="12">
            <DsfrTextField
              label="Confirmation de nouveau mot de passe"
              type="password"
              hide-details="auto"
              v-model="newPasswordConfirmation"
              :rules="[validators.matchPassword]"
              validate-on-blur
              placeholder="Confirmez votre nouveau mot de passe"
            />
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
import DsfrTextField from "@/components/DsfrTextField"

export default {
  name: "PasswordChangeEditor",
  components: { DsfrTextField },
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
