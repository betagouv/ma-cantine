<template>
  <div id="poster-form-page">
    <h1>Générez votre affiche convives</h1>
    <p class="poster-presentation">
      En remplissant ce formulaire, vous pourrez générer un PDF à afficher ou à envoyer par mail à vos convives. Cette
      affiche présente vos données d'achats à vos convives comme demandé par une sous-mesure de la loi EGAlim.
    </p>
    <router-link :to="{ name: 'KeyMeasurePage', params: { id: 'information-des-usagers' } }">
      En savoir plus sur la mesure
    </router-link>
    <div id="poster-generation">
      <form id="poster-form" @submit.prevent="submit">
        <h2>À propos de votre cantine</h2>
        <p>
          Je représente
          <label for="canteen-name">la cantine</label>
          <input
            id="canteen-name"
            v-model="form.canteen.name"
            class="field"
            placeholder="nom de l'établissement"
            required
          />
          dans
          <label for="commune">la commune de</label>
          <input
            id="commune"
            v-model="form.canteen.city"
            class="field"
            placeholder="nom de la commune"
            required
            type="search"
            @input="search"
            list="communes"
          />
          <datalist id="communes">
            <option v-for="commune in communes" :value="commune.properties.label" :key="commune.properties.id">
              {{ commune.properties.label }} ({{ commune.properties.context }})
            </option>
          </datalist>
          .
        </p>
        <p>
          <label for="servings">Nous servons</label>
          <input
            id="servings"
            aria-describedby="repas"
            v-model.number="form.canteen.dailyMealCount"
            type="number"
            min="0"
            placeholder="200"
            required
          />
          <span id="repas">repas par jour</span>
          .
        </p>
        <h2>À propos de vos achats</h2>
        <p>
          <label for="total">
            Sur l'année de 2020, les achats alimentaires (repas, collations et boissons) répresentent
          </label>
          <input
            id="total"
            v-model.number="form.diagnostic.valueTotalHt"
            class="currency-field"
            type="number"
            min="0"
            placeholder="15000"
            aria-describedby="euros"
            required
          />
          <span id="euros">euros HT</span>
          .
        </p>
        <p>
          Sur ce total,
          <input
            id="bio"
            v-model.number="form.diagnostic.valueBioHt"
            class="currency-field"
            type="number"
            min="0"
            placeholder="3000"
            aria-describedby="euros"
            required
          />
          euros HT correspondaient à des
          <label for="bio">produits bio</label>
          et
          <input
            id="sustainable"
            v-model.number="form.diagnostic.valueSustainableHt"
            class="currency-field"
            type="number"
            min="0"
            placeholder="2000"
            aria-describedby="euros"
            required
          />
          euros HT correspondaient à des
          <label for="sustainable">produits de qualité et durables (hors bio)</label>
          .
        </p>
        <input type="submit" id="submit" value="Générer mon affiche" />
      </form>
      <div id="poster-preview">
        <CanteenPoster v-bind="form" id="canteen-poster" />
      </div>
    </div>
  </div>
</template>

<script>
import Constants from "@/constants"
import CanteenPoster from "./CanteenPoster"
import html2pdf from "html2pdf.js"

export default {
  components: {
    CanteenPoster,
  },
  data() {
    return {
      form: {
        diagnostic: {},
        canteen: {},
      },
      communes: [],
    }
  },
  computed: {
    userCanteen() {
      return this.$store.state.userCanteens.length > 0 ? this.$store.state.userCanteens[0] : null
    },
    initialDiagnostic() {
      let diagnostics = this.isAuthenticated ? this.serverDiagnostics : this.localDiagnostics
      return diagnostics.find((x) => x.year === 2020) || Object.assign({}, Constants.DefaultDiagnostics, { year: 2020 })
    },
    serverDiagnostics() {
      return this.userCanteen.diagnostics
    },
    localDiagnostics() {
      return this.$store.getters.getLocalDiagnostics()
    },
    isAuthenticated() {
      return !!this.$store.state.loggedUser
    },
  },
  async mounted() {
    this.form.diagnostic = JSON.parse(JSON.stringify(this.initialDiagnostic))
    this.form.canteen = JSON.parse(JSON.stringify(this.userCanteen)) || {}
  },
  methods: {
    async search() {
      if (!this.form.commune) {
        this.communes = []
        return
      }
      const queryUrl =
        "https://api-adresse.data.gouv.fr/search/?q=" + this.form.commune + "&type=municipality&autocomplete=1"
      const response = await fetch(queryUrl)
      this.communes = (await response.json()).features
    },
    async submit() {
      //this fix an issue where the beginning of the pdf is blank depending on the scroll position
      window.scrollTo({ top: 0 })

      this.saveDiagnostic()
      this.saveCanteen()

      const htmlPoster = document.getElementById("canteen-poster")
      const pdfOptions = {
        filename: "Affiche_convives_2020.pdf",
        image: { type: "jpeg", quality: 1 },
        html2canvas: { scale: 2, dpi: 300, letterRendering: true },
        jsPDF: { unit: "in", format: "a4", orientation: "portrait" },
      }
      return html2pdf()
        .from(htmlPoster)
        .set(pdfOptions)
        .save()
    },
    saveDiagnostic() {
      if (this.isAuthenticated) {
        this.saveInServer()
      } else {
        this.saveInLocalStorage()
      }
    },
    saveInServer() {
      let saveOperation

      if (this.form.diagnostic.id) {
        saveOperation = this.$store.dispatch("updateDiagnostic", {
          canteenId: this.userCanteen.id,
          id: this.form.diagnostic.id,
          payload: this.form.diagnostic,
        })
      } else {
        saveOperation = this.$store.dispatch("createDiagnostic", {
          canteenId: this.userCanteen.id,
          payload: this.form.diagnostic,
        })
      }

      return saveOperation
    },
    saveInLocalStorage() {
      this.$store.dispatch("saveLocalStorageDiagnostic", this.form.diagnostic)
    },
    saveCanteen() {
      if (this.isAuthenticated) {
        return this.$store.dispatch("updateCanteen", {
          id: this.userCanteen.id,
          payload: this.form.canteen,
        })
      }
    },
  },
}
</script>

<style scoped lang="scss">
#poster-form-page {
  padding: 2em;
  display: flex;
  flex-direction: column;
  align-items: center;
  max-width: 1500px !important;
  margin: auto;

  h1 {
    font-size: 48px;
    color: $ma-cantine-green;
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

  input,
  select {
    border: none;
    border-bottom: 6px solid $ma-cantine-light-orange;
    margin: 0.5em;
    font-size: 1.2em;
  }

  input:required {
    border-bottom-color: $ma-cantine-orange;
  }

  input:required:invalid {
    outline: none;
    box-shadow: none;
  }

  input:required:valid {
    border-bottom-color: $ma-cantine-light-orange;
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
    background: $ma-cantine-orange;
    border-radius: 1em;
    padding: 0.5em;
    color: $ma-cantine-white;
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
  border: 1px solid $ma-cantine-grey;
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
