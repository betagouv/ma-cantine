<template>
  <div v-if="jwt">
    <p>La connexion est reussi.</p>
    <p>Adresse email du compte : {{ email }}.</p>
  </div>
  <div v-else-if="token">
    <p>Votre demande est en cours de vérification...</p>
  </div>
  <div v-else>
    <h1>Se connecter</h1>
    <div id="forms">
      <form id="login" @submit.prevent="submitLogin">
        <h2>Connexion</h2>
        <label for="login-email">Email</label>
        <input id="login-email" v-model="loginEmail" type="email" required>
        <input type="submit" class="submit" value="Connectez-moi">
      </form>
      <form id="sign-up" @submit.prevent="submitSignUp">
        <h2>Inscription</h2>
        <label for="sign-up-email">Email</label>
        <input id="sign-up-email" v-model="user.email" type="email" required>
        <label for="name-first">Prénom</label>
        <input id="name-first" v-model="user.firstName" required>
        <label for="name-last">Nom</label>
        <input id="name-last" v-model="user.lastName" required>
        <label for="canteen">Nom de la cantine</label>
        <input id="canteen" v-model="canteen.name" required>
        <label for="city">Ville / commune</label>
        <input id="city" v-model="canteen.city" required>
        <label for="sector">Secteur</label>
        <select id="sector" v-model="canteen.sector" required>
          <option v-for="(title, id) in sectors" :key="id" :value="id">{{ title }}</option>
        </select>
        <input type="submit" class="submit" value="Inscrivez-moi">
      </form>
    </div>
    <p>Si vous avez des difficultés de connexion, contactez nous par email : <a href="mailto:contact@egalim.beta.gouv.fr">contact@egalim.beta.gouv.fr</a></p>
  </div>
</template>

<script>
import jwt from "jsonwebtoken";
import sectors from "@/data/sector-tags";
import { flattenedDiagnostics } from "@/data/KeyMeasures";

var post = function(apiUrl, url, json) {
  return fetch(`${apiUrl}/${url}`, {
    method: "POST",
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(json)
  });
};

var DEFAULT_SECTOR = "scolaire";

export default {
  data() {
    return {
      jwt: null,
      token: this.$route.query.token,
      loginEmail: null,
      user: {},
      canteen: {
        sector: DEFAULT_SECTOR
      },
      loginUrl: (process.env.VUE_APP_SITE_URL || "http://localhost:8080") + this.$route.path + "?token=",
      sectors
    }
  },
  computed: {
    email() {
      return jwt.decode(this.jwt).email;
    }
  },
  created() {
    this.checkToken();
  },
  methods: {
    async submitLogin() {
      post(this.$api_url, 'login', {
        email: this.loginEmail,
        loginUrl: this.loginUrl
      });
      alert("Merci, vous allez recevoir un email pour vous connecter.");
      this.loginEmail = null;
    },
    async submitSignUp() {
      const response = await post(this.$api_url, 'sign-up', {
        user: this.user,
        canteen: this.canteen,
        loginUrl: this.loginUrl
      });

      if (response.status === 200) {
        this.user = {};
        this.canteen = { sector: DEFAULT_SECTOR };
        alert("Merci, vous allez recevoir un email pour vous connecter.")
      } else {
        const error = await response.json();
        console.log(error);
        alert("Une erreur est survenue, vous pouvez nous contacter directement à contact@egalim.beta.gouv.fr")
      }
    },
    checkToken() {
      const localJwt = localStorage.getItem('jwt');
      if(localJwt) {
        this.jwt = localJwt;
      } else if(this.token) {
        const errorMessage = "Une erreur est survenue, essayez de connecter à nouveau ou contactez nous directement à contact@egalim.beta.gouv.fr";
        // TODO: this works for new sign ups, but want to provide the option to users on log in whether to overwrite data or not
        post(this.$api_url, 'complete-login', {
          token: this.token,
          diagnostics: flattenedDiagnostics
        }).then(response => {
            if(response.status === 200) {
              response.json()
                .then(json => {
                  this.jwt = json.jwt;
                  localStorage.setItem('jwt', json.jwt);
                  this.$router.replace({ name: 'KeyMeasuresHome' });
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

  h1 {
    font-weight: bold;
    font-size: 48px;
    color: $green;
  }

  #forms {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
  }

  form {
    display: flex;
    flex-direction: column;
    width: 35em;
    margin: 2em;

    label {
      text-align: left;
      margin-top: 15px;
    }

    input, select {
      margin-top: 10px;
      border: none;
      font-size: 1.2em;
      padding: 5px;
      background-color: $light-orange;
    }

    .submit {
      max-width: 30em;
      font-size: 1.2em;
      margin: auto;
      margin-top: 2em;
      border: none;
      background: $orange;
      border-radius: 1em;
      padding: 0.5em;
      color: $white;
      font-weight: bold;
      cursor: pointer;
    }
  }
</style>