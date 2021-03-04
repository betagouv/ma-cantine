<template>
  <div id="newsletter">
    <div class="newsletter-content">
      <div>
        <h3>Suivre les actualités du site ma cantine</h3>
        <p>Inscrivez-vous à la newsletter et recevez environ 1 email par mois.</p>
      </div>
      <form class="newsletter-form" @submit.prevent="submit">
        <label class="form-label" for="email">Votre adresse email</label>
        <div class="form-content">
          <input class="form-input" id="email" v-model="email" name="email" type="email" required>
          <button class="form-button" type="submit">Valider</button>
        </div>
      </form>
    </div>
    <img src="@/assets/appli-food.svg" class="newsletter-right-image">
  </div>
</template>

<script>
  export default {
    data() {
      return {
        email: '',
      };
    },
    methods: {
      async submit() {
        const requestOptions = {
          method: "POST",
          headers: { "Content-Type": "application/json", "api-key": process.env.VUE_APP_SENDINBLUE_API_KEY },
          body: JSON.stringify({
            email: this.email,
            listIds: [parseInt(process.env.VUE_APP_SENDINBLUE_LIST_ID)],
            updateEnabled: true,
          })
        };

        const response = await fetch("https://api.sendinblue.com/v3/contacts", requestOptions);

        if (response.status === 201 || response.status === 204) {
          this.email = null;
          alert("Vous êtes bien inscrit.e à la newsletter de ma cantine.")
        } else {
          const error = await response.json();
          console.log(error);
        }
      }
    }
  }
</script>

<style scoped lang="scss">
  #newsletter {
    display: flex;
    justify-content: space-around;
    font-size: 20px;
    height: 200px;
    padding: 50px;
    background-color: $light-yellow;
  }

  .newsletter-content {
    display: flex;
    flex-direction: column;
    text-align: left;
    justify-content: space-around;
  }

  .newsletter-form {
    display: flex;
    flex-direction: column;
  }

  .form-label {
    font-weight: bold;
  }

  .form-content {
    margin-top: 10px;
  }

  .form-input {
    height: 60px;
    width: 485px;
    font-size: 20px;
    padding-left: 15px;
    border-radius: 30px;
    border: none;
  }

  .form-button {
    height: 60px;
    width: 120px;
    margin-left: -45PX;
    background-color: $dark-yellow;
    font-weight: bold;
    font-size: 1em;
    cursor: pointer;
    border-radius: 30px;
    border: none;
  }

  @media (max-width: 920px) {
    .newsletter-right-image {
      display: none;
    }
  }

  @media (max-width: 700px) {
    #newsletter {
      height: 300px;
    }

    .newsletter-content {
      text-align: center;
    }

    .form-input {
      width: 98%;
      padding-left: 2%;
    }

    .form-button {
      margin-top: 10px;
      margin-left: 0;
    }
  }

  @media (max-width: 430px) {
    #newsletter {
      height: 350px;
    }
  }
</style>
