<template>
  <div id="poster-form-page">
    <h1>Générez votre affichage convives</h1>
    <div id="poster-generation">
      <form id="poster-form" @submit.prevent="submit">
        <h2>À propos de votre cantine</h2>
        <p>
          <label for="profession">Je suis </label>
          <input id="profession" v-model="form.profession" class="field" placeholder="chef.fe">
          dans <label for="school">la cantine du </label>
          <input id="school" v-model="form.school" class="field" placeholder="nom de l'école" required>
          dans <label for="commune">le commune de </label>
          <input id="commune" v-model="form.commune" class="field" placeholder="Plouër-sur-Rance">.
        </p>
        <p>
          <label for="servings">Nous servons </label>
          <input id="servings"
            v-model="form.servings"
            class="number-field"
            inputmode="numeric"
            pattern="[0-9]*"
            placeholder="200"
            required
            @keydown="processNumber('servings')"
          >
          enfants par jour.
        </p>
        <h2>À propos de vos achats</h2>
        <p>
          <label for="total">Sur l'année de 2020, les achats répresent </label>
          <input id="total"
            v-model="form.total"
            class="number-field"
            inputmode="decimal"
            placeholder="1500,00"
            :pattern="pattern"
            aria-describedby="euros"
            required
            @keydown="processNumber('total')"
          >
          <span id="euros">euros HT</span>.
        </p>
        <p>
          Sur ce total,
          <input id="bio"
            v-model="form.bio"
            class="number-field"
            inputmode="decimal"
            placeholder="300,00"
            :pattern="pattern"
            aria-describedby="euros"
            required
            @keydown="processNumber('bio')"
          >
          euros HT correspondaient à des <label for="bio">produits bio</label>,
          <input id="quality"
            v-model="form.quality"
            class="number-field"
            inputmode="decimal"
            placeholder="200,00"
            :pattern="pattern"
            aria-describedby="euros"
            required
            @keydown="processNumber('quality')"
          >
          euros HT correspondaient à des <label for="quality">produits de qualité et durables (sauf bio)</label> et 
          <input id="equitable"
            v-model="form.equitable"
            class="number-field"
            inputmode="decimal"
            placeholder="100,00"
            :pattern="pattern"
            aria-describedby="euros"
            required
            @keydown="processNumber('equitable')"
          >
          euros HT correspondaient à des <label for="equitable">produits du commerce équitable</label>.
        </p>
        <input type="submit" id="submit" value="Générer mon affichage">
      </form>
      <CanteenPoster v-bind="form" />
    </div>
  </div>
</template>

<script>
  import CanteenPoster from './CanteenPoster';
  import jsPDF from 'jspdf';
  import html2canvas from 'html2canvas';

  export default {
    components: {
      CanteenPoster
    },
    data() {
      return {
        form: {},
        pattern: "[0-9]*(,[0-9]{2})?"
      };
    },
    methods: {
      processNumber(key) {
        if(this.form[key]) {
          this.form[key + "Number"] = parseFloat(this.form[key].replace(',', '.'));
        }
      },
      submit() {
        this.form["servingsNumber"] = parseInt(this.form["servings"], 10);
        ["total", "bio", "quality", "equitable"].forEach(key => {
          this.form[key + "Number"] = parseFloat(this.form[key].replace(',', '.'))
        });
        const filename = "affichage.pdf";
        let doc = new jsPDF('p', 'pt', 'a4');

        html2canvas(document.querySelector("#poster-contents")).then(canvas => {
          const imgData = canvas.toDataURL('image/jpeg');
          console.log('Report Image URL: '+imgData);

          doc.addImage(imgData, 'JPEG', 5, 0, 580, 830);
          doc.save(filename);
        });
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

    input {
      border: none;
      border-bottom: 8px solid $light-orange;
      margin: 0.5em;
      font-size: 1.2em;
    }

    input:required:invalid {
      outline: none;
      box-shadow: none;
    }

    .number-field {
      width: 7em;
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