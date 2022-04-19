<template>
  <div>
    <!-- TODO: make this page nicer -->
    <h1>Login</h1>
    <v-form ref="form" v-model="formIsValid">
      <v-row>
        <v-col cols="12">
          <p class="body-2 mb-1 mt-2 text-left">Username</p>
          <v-text-field hide-details="auto" solo v-model="username" :rules="[validators.required]"></v-text-field>
        </v-col>
        <v-col cols="12">
          <p class="body-2 mb-1 mt-2 text-left">Mot de passe</p>
          <v-text-field hide-details="auto" solo v-model="password" :rules="[validators.required]"></v-text-field>
        </v-col>
      </v-row>
      <v-btn x-large color="primary" @click="login">
        Login
      </v-btn>
    </v-form>
    <!-- TODO: links to magic link login (/envoyer-email-conexion), reset password (/reinitialisation-mot-de-passe), register (/creer-mon-compte) -->
  </div>
</template>

<script>
import validators from "@/validators"

export default {
  data() {
    return {
      username: "",
      password: "",
      validators,
      formIsValid: true,
    }
  },
  methods: {
    login() {
      this.$refs.form.validate()
      if (!this.formIsValid) {
        return
      }
      const payload = { login: this.username, password: this.password }
      return this.$store
        .dispatch("loginUser", { payload })
        .then(() => {
          this.$router.push({ name: "ManagementPage" })
        })
        .catch((e) => {
          // deal with the 403 that is given for bad password or bad username
          // response.json().detail = "Login or password invalid."
          // or bad CSRF, also 403
          // response.json().detail = "CSRF Failed: CSRF token from the 'X-Csrftoken' HTTP header incorrect."
          // error message
          console.log("e", e)
        })
    },
  },
}
</script>
