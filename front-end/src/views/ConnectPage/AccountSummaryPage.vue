<template>
  <div>
    <h1>Mon compte</h1>
    <div class="container">
      <p>Adresse email du compte : {{ email }}.</p>
      <router-link :to="{ name: 'KeyMeasuresHome' }" class="primary action">Mon tableau de bord</router-link>
      <button class="secondary action" @click="logout">Me déconnecter</button>
    </div>
  </div>
</template>

<script>
import jwt from "jsonwebtoken";

export default {
  data() {
    return {
      jwt: localStorage.getItem('jwt'),
      token: this.$route.query.token,
    }
  },
  computed: {
    email() {
      return this.jwt ? jwt.decode(this.jwt).email : null;
    }
  },
  created() {
    this.checkToken();
    // TODO: display more info about account
  },
  methods: {
    async checkToken() {
      if(this.jwt) {
        // TODO: check token still valid
        // if no, send to login page with message & delete jwt
      } else {
        this.$router.replace({ name: 'SignUpPage' });
      }
    },
    logout() {
      localStorage.removeItem('jwt');
      this.$jwt.token = null;
      this.$router.push({ name: 'LandingPage' });
    }
  }
}
</script>
