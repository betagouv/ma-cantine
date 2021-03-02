<template>
  <div id="poster-form-page">
    <h1>Générez votre affiche convives</h1>
    <div id="poster-generation">
      <form id="poster-form" @submit.prevent="submit">
        <h2>À propos de votre cantine</h2>
        <p>
          <label for="profession">Je suis </label>
          <select id="profession" v-model="form.profession" class="field">
            <option value="cheffe">Chef.fe de cuisine</option>
            <option value="elue">Élu.e</option>
            <option value="magasiniere">Magasinier.e</option>
            <option value="intendante">Intendant.e</option>
            <option value="autre">Autre</option>
          </select>
          dans <label for="school">la cantine </label>
          <input id="school" v-model="form.school" class="field" placeholder="nom de l'école" required>
          dans <label for="commune">le commune de </label>
          <input id="commune" v-model="form.commune" class="field" placeholder="Plouër-sur-Rance" required>.
        </p>
        <p>
          <label for="servings">Nous servons </label>
          <input id="servings"
            aria-describedby="repas"
            v-model="form.servings"
            inputmode="numeric"
            pattern="[0-9]*"
            placeholder="200"
            required
            @input="processNumber('servings')"
          >
          <span id="repas">repas par jour</span>.
        </p>
        <h2>À propos de vos achats</h2>
        <p>
          <label for="total">Sur l'année de 2020, les achats alimentaires (repas, collations et boissons) répresentent </label>
          <input id="total"
            v-model="form.total"
            class="currency-field"
            inputmode="decimal"
            placeholder="15 000,00"
            :pattern="pattern"
            aria-describedby="euros"
            required
            @input="processNumber('total')"
          >
          <span id="euros">euros HT</span>.
        </p>
        <p>
          Sur ce total,
          <input id="bio"
            v-model="form.bio"
            class="currency-field"
            inputmode="decimal"
            placeholder="3 000,00"
            :pattern="pattern"
            aria-describedby="euros"
            required
            @input="processNumber('bio')"
          >
          euros HT correspondaient à des <label for="bio">produits bio</label>,
          <input id="quality"
            v-model="form.quality"
            class="currency-field"
            inputmode="decimal"
            placeholder="2 000,00"
            :pattern="pattern"
            aria-describedby="euros"
            required
            @input="processNumber('quality')"
          >
          euros HT correspondaient à des <label for="quality">produits de qualité et durables (hors bio)</label> et 
          <input id="equitable"
            v-model="form.equitable"
            class="currency-field"
            inputmode="decimal"
            placeholder="100,00"
            :pattern="pattern"
            aria-describedby="euros"
            @input="processNumber('equitable')"
          >
          euros HT correspondaient à des <label for="equitable">produits issus du commerce équitable</label>.
        </p>
        <input type="submit" id="submit" value="Générer mon affiche">
      </form>
      <CanteenPoster v-bind="form" />
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
        pattern: "[0-9 ]*(,[0-9]{2})?"
      };
    },
    methods: {
      processNumber(key) {
        const numberKey = key + "Number";
        if(this.form[key]) {
          this.form[numberKey] = parseFloat(this.form[key].replaceAll(' ', '').replace(',', '.'));
        } else if(this.form[numberKey]) {
          delete this.form[numberKey];
        }
      },
      submit() {
        this.form["servingsNumber"] = parseInt(this.form["servings"], 10);

        const htmlPoster = document.getElementById('poster-contents');
        const pdfOptions = {
          filename:     'Affiche_convives_2020.pdf',
          image:        { type: 'jpeg', quality: 1 },
          html2canvas:  { scale: 2, dpi: 300, letterRendering: true },
          jsPDF:        { unit: 'in', format: 'a4', orientation: 'portrait' }
        };
        html2pdf().from(htmlPoster).set(pdfOptions).save();
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

  @media (max-width: 1200px) {
    #poster-generation {
      flex-direction: column;
    }
  }
</style>