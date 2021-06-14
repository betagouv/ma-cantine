<template>
  <div>
    <v-row>
      <v-spacer></v-spacer>
      <v-col cols="12" sm="10" md="8">
        <h1 class="font-weight-black my-6">
          Générez votre affiche convives
        </h1>
        <p class="text-body-2">
          En remplissant ce formulaire, vous pourrez générer un PDF à afficher ou à envoyer par mail à vos convives.
          Cette affiche présente vos données d'achats à vos convives comme demandé par une sous-mesure de la loi EGAlim.
        </p>
        <v-btn
          color="primary"
          class="text-decoration-underline"
          text
          :to="{ name: 'KeyMeasurePage', params: { id: 'information-des-usagers' } }"
        >
          En savoir plus sur la mesure
        </v-btn>
      </v-col>
      <v-spacer></v-spacer>
    </v-row>

    <div id="poster-form-page">
      <p class="poster-presentation"></p>
      <div id="poster-generation">
        <v-form ref="form" v-model="formIsValid" id="poster-form" @submit.prevent class="text-left">
          <h2 class="mb-4">À propos de votre cantine</h2>
          <p>
            Je représente
            <label for="canteen-name">la cantine</label>
            <v-text-field
              id="canteen-name"
              v-model="form.canteen.name"
              placeholder="nom de l'établissement"
              hide-details="auto"
              :rules="[validators.notEmpty]"
              solo
              class="my-4"
            ></v-text-field>
            dans
            <label for="commune">la commune de</label>
            <v-autocomplete
              id="commune"
              v-model="form.canteen.city"
              placeholder="nom de la commune"
              :loading="loadingCommunes"
              :items="communes"
              :search-input.sync="search"
              auto-select-first
              cache-items
              hide-details="auto"
              :rules="[validators.notEmpty]"
              solo
              class="my-4"
            ></v-autocomplete>
          </p>
          <p>
            <label for="servings">Nous servons</label>
            <v-text-field
              id="servings"
              v-model.number="form.canteen.dailyMealCount"
              type="number"
              :rules="[validators.greaterThanZero]"
              placeholder="200"
              solo
              class="my-4"
              suffix="repas par jour"
              hide-details="auto"
            />
          </p>
          <h2 class="mb-4">À propos de vos achats</h2>
          <p>
            <label for="total">
              Sur l'année de 2020, les achats alimentaires (repas, collations et boissons) répresentent
            </label>
            <v-text-field
              id="total"
              v-model.number="form.diagnostic.valueTotalHt"
              type="number"
              :rules="[validators.greaterThanZero]"
              placeholder="15000"
              suffix="euros HT"
              solo
              class="my-4"
              hide-details="auto"
              validate-on-blur
            />
          </p>
          <p>
            Sur ce total,
            <v-text-field
              id="bio"
              v-model.number="form.diagnostic.valueBioHt"
              type="number"
              :rules="[validators.greaterThanZero]"
              placeholder="3000"
              suffix="euros HT"
              solo
              class="my-4"
              hide-details="auto"
              validate-on-blur
            />
            correspondaient à des
            <label for="bio">produits bio</label>
            et
            <v-text-field
              id="sustainable"
              v-model.number="form.diagnostic.valueSustainableHt"
              type="number"
              :rules="[validators.greaterThanZero]"
              placeholder="2000"
              suffix="euros HT"
              solo
              class="my-4"
              hide-details="auto"
              validate-on-blur
            />
            correspondaient à des
            <label for="sustainable">produits de qualité et durables (hors bio)</label>
            .
          </p>
          <v-btn x-large color="primary" @click="submit">Générer mon affiche</v-btn>
        </v-form>
        <div id="poster-preview">
          <CanteenPoster v-bind="form" id="canteen-poster" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Constants from "@/constants"
import CanteenPoster from "./CanteenPoster"
import html2pdf from "html2pdf.js"
import validators from "@/validators"

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
      loadingCommunes: false,
      search: null,
      formIsValid: true,
    }
  },
  computed: {
    validators() {
      return validators
    },
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
  beforeMount() {
    this.form.diagnostic = JSON.parse(JSON.stringify(this.initialDiagnostic))
    this.form.canteen = JSON.parse(JSON.stringify(this.userCanteen)) || {}
    // initialise autocomplete options so existing city is seen as valid input and displayed
    if (this.form.canteen.city) {
      this.communes = [this.form.canteen.city]
    }
  },
  watch: {
    search(val) {
      return val && val !== this.form.canteen.city && this.queryCommunes(val)
    },
  },
  methods: {
    queryCommunes(val) {
      this.loadingCommunes = true
      const queryUrl = "https://api-adresse.data.gouv.fr/search/?q=" + val + "&type=municipality&autocomplete=1"
      return fetch(queryUrl)
        .then((response) => response.json())
        .then((response) => {
          const communes = response.features
          this.communes = communes.map((commune) => `${commune.properties.label}`)
          this.loadingCommunes = false
        })
        .catch((error) => {
          console.log(error)
        })
    },
    async submit() {
      this.$refs.form.validate()
      if (!this.formIsValid) {
        window.alert("Merci de vérifier les champs en rouge et réessayer")
        return
      }
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
  display: flex;
  flex-direction: column;
  align-items: center;
  max-width: 1500px !important;
  margin: auto;
}

#poster-generation {
  display: flex;
  margin-top: 50px;
  width: 1200px;
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
    width: auto;
  }
}

@media (max-width: 210mm) {
  #poster-preview {
    display: none;
  }
}
</style>
