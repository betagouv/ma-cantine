<template>
  <form id="publish-form" @submit.prevent="submit">
    <h2>Devenir béta-testeur</h2>
    <p>
      Nous sommes en version de test et cherchons continuellement à améliorer la plateforme.
      Pour cela nous cherchons des cantines prêtes à nous accompagner en devenant béta-testeur.
      Si vous souhaitez y participer merci de nous communiquer vos informations ci-dessous.
    </p>
    <label for="school" class="publish-label">Nom de votre cantine</label>
    <input id="school" class="publish-input" v-model="form.school" required>
    <label for="city" class="publish-label">Ville / commune</label>
    <input id="city" class="publish-input" v-model="form.city" required>
    <label for="email" class="publish-label">Votre email</label>
    <input id="email" class="publish-input" v-model="form.email" type="email" required>
    <label for="phone" class="publish-label" type="tel">Numéro de téléphone (optionnel)</label>
    <input id="phone" class="publish-input" v-model="form.phone">
    <label for="message" class="publish-label">Message (optionnel)</label>
    <textarea id="message" class="publish-input" v-model="form.message" />
    <input type="submit" id="submit" value="Je participe">
  </form>
</template>

<script>
export default {
    data() {
      return {
        form: {},
      };
    },
    methods: {
      async submit() {
        const response = await fetch(`${this.$api_url}/subscribe-beta-tester`, {
          method: "POST",
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.form)
        });

        if (response.status === 201) {
          this.form = {};
          alert("Merci de vôtre intérêt pour ma cantine, nous reviendrons vers vous dans les plus brefs délais.")
        } else {
          const error = await response.json();
          console.log(error);
          alert("Une erreur est survenue, vous pouvez nous contacter directement à contact@egalim.beta.gouv.fr")
        }
      },
    },
  }
</script>

<style scoped lang="scss">
  #publish-form {
    display: flex;
    flex-direction: column;
    width: 90%;
    margin: 50px auto;

    .publish-label {
      text-align: left;
      margin-top: 15px;
    }

    .publish-input {
      margin-top: 10px;
      border: none;
      border-bottom: 6px solid $light-orange;
      font-size: 1.2em;
      padding: 5px;
      background-color: $light-orange;
    }

    .publish-input:required {
      border-bottom-color: $orange;
    }

    .publish-input:required:invalid {
      outline: none;
      box-shadow: none;
    }

    .publish-input:required:valid {
      border-bottom-color: $light-orange;
    }

    #message {
      height: 100px;
    }

    #submit {
      width: 150px;
      font-size: 1.2em;
      margin: auto;
      margin-top: 30px;
      border: none;
      background: $orange;
      border-radius: 1em;
      padding: 0.5em;
      color: $white;
      float: right;
      font-weight: bold;
      cursor: pointer;
    }
  }
</style>
