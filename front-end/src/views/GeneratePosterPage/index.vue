<template>
  <div id="poster-form-page">
    <h1>Générez votre affiche convives</h1>
    <div id="poster-generation">
      <form id="poster-form" @submit.prevent="submit">
        <h2>À propos de votre cantine</h2>
        <p>
          Je représente <label for="school">la cantine</label>
          <input id="school" v-model="form.school" class="field" placeholder="nom de l'école" required>
          dans <label for="commune">le commune de </label>
          <input id="commune" v-model="form.commune" class="field" placeholder="Plouër-sur-Rance" required>.
        </p>
        <p>
          <label for="servings">Nous servons </label>
          <input id="servings"
            aria-describedby="repas"
            v-model.number="form.servings"
            type="number"
            min="0"
            placeholder="200"
            required
          >
          <span id="repas">repas par jour</span>.
        </p>
        <h2>À propos de vos achats</h2>
        <p>
          <label for="total">Sur l'année de 2020, les achats alimentaires (repas, collations et boissons) répresentent </label>
          <input id="total"
            v-model.number="form.total"
            class="currency-field"
            type="number"
            min="0"
            placeholder="15000"
            aria-describedby="euros"
            required
          >
          <span id="euros">euros HT</span>.
        </p>
        <p>
          Sur ce total,
          <input id="bio"
            v-model.number="form.bio"
            class="currency-field"
            type="number"
            min="0"
            placeholder="3000"
            aria-describedby="euros"
            required
          >
          euros HT correspondaient à des <label for="bio">produits bio</label>,
          <input id="quality"
            v-model.number="form.quality"
            class="currency-field"
            type="number"
            min="0"
            placeholder="2000"
            aria-describedby="euros"
            required
          >
          euros HT correspondaient à des <label for="quality">produits de qualité et durables (hors bio)</label> et 
          <input id="equitable"
            v-model.number="form.equitable"
            class="currency-field"
            type="number"
            min="0"
            placeholder="100"
            aria-describedby="euros"
          >
          euros HT correspondaient à des <label for="equitable">produits issus du commerce équitable</label>.
        </p>
        <input type="submit" id="submit" value="Générer mon affiche">
      </form>
      <div id="poster-preview">
        <CanteenPoster v-bind="form" id="canteen-poster" />
      </div>
    </div>
  </div>
</template>

<script>
  import CanteenPoster from './CanteenPoster';
  import html2pdf from 'html2pdf.js';

  export default {
    components: {
      CanteenPoster
    },
    data() {
      return {
        form: {},
      };
    },
    methods: {
      submit() {
        const htmlPoster = document.getElementById('canteen-poster');
        const pdfOptions = {
          filename:     'Affiche_convives_2020.pdf',
          image:        { type: 'jpeg', quality: 1 },
          html2canvas:  { scale: 2, dpi: 300, letterRendering: true },
          jsPDF:        { unit: 'in', format: 'a4', orientation: 'portrait' }
        };
        return html2pdf().from(htmlPoster).set(pdfOptions).save();
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
    max-width: 1700px;
    margin: auto;

    h1 {
      font-size: 48px;
      color: $green;
      margin: 1em 0em;
    }
  }

  #poster-generation {
    display: flex;
  }

  #poster-form {
    text-align: left;

    input, select {
      border: none;
      border-bottom: 6px solid $light-orange;
      margin: 0.5em;
      font-size: 1.2em;
    }

    input:required {
      border-bottom-color: $orange;
    }

    input:required:invalid {
      outline: none;
      box-shadow: none;
    }

    input:required:valid {
      border-bottom-color: $light-orange;
    }

    #servings {
      width: 3em;
    }

    #total {
      width: 6.5em;
    }

    .currency-field {
      width: 5em;
    }

    #submit {
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

  #poster-preview {
    width: 210mm;
    min-width: 210mm;
    height: 296mm;
    min-height: 296mm;
    margin-left: 2em;
    border: 1px solid $grey;
  }

  @media (max-width: 1200px) {
    #poster-generation {
      flex-direction: column;
    }
  }

  @media (max-width: 210mm) {
    #poster-preview {
      display: none;
    }
  }
</style>