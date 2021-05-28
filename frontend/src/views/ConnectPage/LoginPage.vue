<template>
  <div v-if="token">
    <p>Votre demande est en cours de vérification...</p>
  </div>
  <div v-else>
    <h1>Se connecter</h1>
    <form id="login" class="container" @submit.prevent="submitLogin">
      <label for="login-email">Email</label>
      <input id="login-email" v-model="loginEmail" type="email" required />
      <input type="submit" class="primary action" value="Connectez-moi" />
    </form>
    <div id="alt-choice" class="container">
      <p>Pas encore de compte ?</p>
      <router-link :to="{ name: 'SignUpPage' }" class="secondary action">Créer un compte</router-link>
    </div>
  </div>
</template>

<script>
import { getLocalDiagnostics, deleteLocalDiagnostics } from "@/data/KeyMeasures"
import { login, completeLogin } from "@/data/submit-actions.js"

export default {
  data() {
    return {
      token: this.$route.query.token,
      loginEmail: null,
    }
  },
  created() {
    this.checkToken()
  },
  methods: {
    submitLogin() {
      login(this.loginEmail)
      alert("Merci, vous allez recevoir un email pour vous connecter.")
      this.loginEmail = null
    },
    async checkToken() {
      if (localStorage.getItem("jwt")) {
        this.$router.replace({ name: "AccountSummaryPage" })
      } else if (this.token) {
        // TODO: this works for new sign ups, but want to provide the option to users on log in whether to overwrite data or not
        // currently this overwrites db data if local data is present
        const diagnostics = getLocalDiagnostics()

        const response = await completeLogin(this.token, diagnostics)

        if (response.status === 200) {
          const json = await response.json()
          localStorage.setItem("jwt", json.jwt)
          this.$jwt.token = json.jwt
          deleteLocalDiagnostics()
          this.$router.replace({ name: "KeyMeasuresHome" })
        } else {
          this.token = null
          alert(
            "Une erreur est survenue, essayez de vous connecter à nouveau ou contactez nous directement à contact@egalim.beta.gouv.fr"
          )
        }
      }
    },
  },
}
</script>
