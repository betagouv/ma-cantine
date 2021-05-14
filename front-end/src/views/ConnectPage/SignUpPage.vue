<template>
  <div>
    <h1>Créer mon compte</h1>
    <form id="sign-up" class="container" @submit.prevent="submitSignUp">
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
      <input type="submit" class="primary action" value="Inscrivez-moi">
    </form>
    <div id="alt-choice" class="container">
      <p>Déjà un compte ?</p>
      <router-link :to="{ name: 'LoginPage' }" class="secondary action">M'identifier</router-link>
    </div>
  </div>
</template>

<script>
import sectors from "@/data/sector-tags";
import { signUp } from "@/data/submit-actions.js";

var DEFAULT_SECTOR = "scolaire";

export default {
  data() {
    return {
      user: {},
      canteen: {
        sector: DEFAULT_SECTOR
      },
      sectors
    }
  },
  created() {
    this.checkToken();
  },
  methods: {
    async submitSignUp() {
      const response = await signUp(this.user, this.canteen);

      if(response.status === 200) {
        this.user = {};
        this.canteen = { sector: DEFAULT_SECTOR };
        alert("Merci, vous allez recevoir un email pour vous connecter.")
      } else {
        const error = await response.json();
        console.log(error);
        alert("Une erreur est survenue, vous pouvez nous contacter directement à contact@egalim.beta.gouv.fr")
      }
    },
    async checkToken() {
      if(localStorage.getItem('jwt')) {
        this.$router.replace({ name: 'AccountSummaryPage' });
      }
    }
  }
}
</script>
