<template>
  <div v-if="jwt">
    <p>La connexion est reussi</p>
  </div>
  <div v-else-if="token">
    <p>Votre demande est en cours de vérification...</p>
  </div>
  <div v-else>
    <h1>Connecter</h1>
    <form id="login" @submit.prevent="submitLogin">
      <h2>Connexion</h2>
      <label for="email">Email : </label>
      <input id="email" v-model="loginEmail" type="email" required>
      <input type="submit" value="Connecter-moi">
    </form>
    <form id="sign-up" @submit.prevent="submitSignUp">
      <h2>M'inscrire</h2>
      <label for="email">Email : </label>
      <input id="email" v-model="user.email" type="email" required>
      <label for="name-first">Prénom : </label>
      <input id="name-first" v-model="user.firstName" required>
      <label for="name-last">Nom : </label>
      <input id="name-last" v-model="user.lastName" required>
      <label for="canteen">Nom de la cantine : </label>
      <input id="canteen" v-model="canteen.name" required>
      <label for="city">Ville / commune : </label>
      <input id="city" v-model="canteen.city" required>
      <label for="sector">Sector : </label>
      <!-- TODO: make sector limited list matching back-end -->
      <input id="sector" v-model="canteen.sector" required>
      <input type="submit" value="Inscrivez-moi">
    </form>
  </div>
</template>

<script>
var post = function(apiUrl, url, json) {
  return fetch(`${apiUrl}/${url}`, {
    method: "POST",
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(json)
  });
};

export default {
  data() {
    return {
      jwt: null,
      token: this.$route.query.token,
      loginEmail: null,
      user: {},
      canteen: {}
    }
  },
  created() {
    this.checkToken();
  },
  methods: {
    async submitLogin() {
      post(this.$api_url, 'login', { email: this.loginEmail });
      alert("Merci, si vous avez un compte vous recevriez un email.");
      this.loginEmail = null;
    },
    async submitSignUp() {
      const response = await post(this.$api_url, 'sign-up', {
        user: this.user,
        canteen: this.canteen
      });

      if (response.status === 201) {
        this.user = {};
        this.canteen = {};
        alert("Merci, vous recevrez un email bientôt pour connecter.")
      } else {
        const error = await response.json();
        console.log(error);
        alert("Une erreur est survenue, vous pouvez nous contacter directement à contact@egalim.beta.gouv.fr")
      }
    },
    checkToken() {
      if(this.token) {
        const errorMessage = "Une erreur est survenue, essayez de connecter à nouveau ou contactez nous directement à contact@egalim.beta.gouv.fr";
        fetch(`${this.$api_url}/complete-login?token=${encodeURIComponent(this.token)}`)
          .then(response => {
            console.log("Response: ", response);
            if(response.status === 200) {
              response.json()
                .then(json => {
                  console.log(json);
                  this.jwt = json.jwt;
                })
                .catch(error => {
                  console.log("JWT parsing error: ", error);
                });
            } else {
              alert(errorMessage)
              this.token = null;
            }
          }).catch(error => {
            console.log("Error: ", error)
            alert(errorMessage)
            this.token = null;
          });
      }
    }
  }
}
</script>

<style lang="scss" scoped>
 div {
   padding: 2em;
 }
</style>