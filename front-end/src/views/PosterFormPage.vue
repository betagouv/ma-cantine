<template>
  <div id="poster-form-page">
    <h1>Générez votre affichage convives</h1>
    <form id="poster-form">
      <h2>À propos de votre cantine</h2>
      <p>
        <label for="profession">Je suis </label> <input id="profession" v-model="form.profession" class="field" placeholder="chef.fe">
        dans <label for="school">la cantine du </label> <input id="school" v-model="form.school" class="field" placeholder="nom de l'école">
        dans <label for="commune">le commune de </label> <input id="commune" v-model="form.commune" class="field" placeholder="Plouër-sur-Rance">.
      </p>
      <p>
        <label for="servings">Nous servons </label>
        <input id="servings" v-model="form.servings" class="number-field" inputmode="numeric" pattern="[0-9]*" placeholder="200">
        enfants par jour.
      </p>
      <h2>À propos de vos achats</h2>
      <p>
        <label for="total">Sur l'année de 2020, les achats répresent </label>
        <input id="total" v-model="form.total" class="number-field" placeholder="1500.00" aria-describedby="euros">
        <span id="euros">euros HT</span>.
      </p>
      <p>
        Sur ce total,
         <input id="bio" v-model="form.bio" class="number-field" placeholder="300.00" aria-describedby="euros">
          euros HT correspondaient à des <label for="bio">produits bio</label>,
        <input id="quality" v-model="form.quality" class="number-field" placeholder="200.00" aria-describedby="euros">
         euros HT correspondaient à des <label for="quality">produits de qualité et durables (sauf bio)</label>
         et <input id="equitable" v-model="form.equitable" class="number-field" placeholder="100.00" aria-describedby="euros">
         euros HT correspondaient à des <label for="equitable">produits du commerce équitable</label>.
      </p>
      <input type="submit" id="submit" value="Générer mon affichage" @click.prevent="submit">
    </form>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        form: {}
      };
    },
    methods: {
      submit() {
        console.log(this.form);
      }
    }
  }
</script>

<style scoped lang="scss">
  #poster-form-page {
    padding: 2em;
    display: flex;
    flex-direction: column;
    align-items: center;
    max-width: 1000px;
    margin: auto;

    h1 {
      font-size: 48px;
      color: $green;
      margin: 1em 0em;
    }
  }

  #poster-form {
    text-align: left;

    input {
      border: none;
      border-bottom: 8px solid $light-orange;
      margin: 0.5em;
      font-size: 1.2em;
    }

    .number-field {
      width: 8em;
    }

    #submit {
      border: none;
      background: $orange;
      border-radius: 1em;
      padding: 0.5em;
      color: $white;
      float: right;
    }
  }
</style>