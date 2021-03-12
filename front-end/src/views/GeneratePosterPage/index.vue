<template>
  <div id="poster-form-page">
    <h1>Générez votre affiche convives</h1>
    <p class="poster-presentation">
      En remplissant ce formulaire, vous pourrez générer un PDF à afficher ou à envoyer par mail à vos convives.
      Cette affiche présente vos données d'achats à vos convives comme demandé
      par une sous-mesure de la loi EGAlim.
    </p>
    <router-link :to="{ name: 'KeyMeasurePage', params: { id: 'information-des-usagers' } }">
      En savoir plus sur la mesure
    </router-link>
    <div id="poster-generation">
      <form id="poster-form" @submit.prevent="submit">
        <h2>À propos de votre cantine</h2>
        <p>
          Je représente <label for="school">la cantine</label>
          <input id="school" v-model="form.school" class="field" placeholder="nom de l'établissement" required>
          dans <label for="commune">la commune de </label>
          <input id="commune"
            v-model="form.commune"
            class="field"
            placeholder="nom de la commune"
            required
            type="search"
            @input="search"
            list="communes"
          >
          <datalist id="communes">
            <option v-for="commune in communes" :value="commune.properties.label" :key="commune.properties.id">
              {{ commune.properties.label }} ({{ commune.properties.context }})
            </option>
          </datalist>
          .
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
          <input id="sustainable"
            v-model.number="form.sustainable"
            class="currency-field"
            type="number"
            min="0"
            placeholder="2000"
            aria-describedby="euros"
            required
          >
          euros HT correspondaient à des <label for="sustainable">produits de qualité et durables (hors bio)</label> et
          <input id="fair-trade"
            v-model.number="form.fairTrade"
            class="currency-field"
            type="number"
            min="0"
            placeholder="100"
            aria-describedby="euros"
          >
          euros HT correspondaient à des <label for="fair-trade">produits issus du commerce équitable</label>.
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
        communes: []
      };
    },
    methods: {
      async search() {
        if(!this.form.commune) {
          this.communes = [];
          return;
        }
        const queryUrl = "https://api-adresse.data.gouv.fr/search/?q="+this.form.commune+"&type=municipality&autocomplete=1";
        const response = await fetch(queryUrl);
        this.communes = (await response.json()).features;
      },
      submit() {
        //this fix an issue where the beginning of the pdf is blank depending on the scroll position
        window.scrollTo({ top: 0 });

        const htmlPoster = document.getElementById('canteen-poster');
        const pdfOptions = {
          filename:     'Affiche_convives_2020.pdf',
          image:        { type: 'jpeg', sustainable: 1 },
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

    .poster-presentation {
      max-width: 1170px;
    }
  }

  #poster-generation {
    display: flex;
    margin-top: 50px;
  }

  #poster-form {
    text-align: left;

    p {
      line-height: 50px;
      margin: 0;
    }

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
