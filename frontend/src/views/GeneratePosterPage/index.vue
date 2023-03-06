<template>
  <div id="content" class="text-left">
    <BreadcrumbsNav />
    <h1 class="font-weight-black mb-6">
      Générez votre affiche
      <br />
      «&nbsp;information des convives&nbsp;»
    </h1>
    <p v-if="!hasCanteens && isAuthenticated" class="mt-0">
      Remplissez le formulaire ci-dessous ou
      <router-link :to="{ name: 'NewCanteen' }">créez votre cantine</router-link>
      pour que vos données soient automatiquement renseignées.
      <v-divider class="mt-4"></v-divider>
    </p>
    <p class="text-body-2">
      En remplissant ce formulaire, vous pourrez générer un PDF à afficher ou à envoyer par mail à vos convives pour les
      informer sur la part de produits de qualité et durables et de la part des produits issus de projets alimentaires
      territoriaux entrant dans la composition des repas servis dans votre restaurant. Cette information est obtenue à
      partir de vos données annuelles d’achat.
    </p>
    <router-link
      :to="{ name: 'KeyMeasurePage', params: { id: 'information-des-usagers' } }"
      class="text-decoration-underline primary--text text-body-2"
    >
      En savoir plus sur la mesure
    </router-link>

    <div v-if="isAuthenticated && hasCanteens">
      <v-form ref="form" v-model="formIsValid" id="poster-form" @submit.prevent class="mb-4">
        <v-row class="px-4 mt-2" align="end">
          <v-col cols="12" sm="6" md="7" class="my-0 my-sm-4 pl-0">
            <DsfrAutocomplete
              hide-details
              :items="userCanteens"
              label="Choisissez la cantine"
              v-model="selectedCanteenId"
              @change="onCanteenAutocompleteChange"
              item-text="name"
              item-value="id"
              no-data-text="Pas de résultats"
            />
          </v-col>
          <v-col class="my-0 my-sm-4 px-0 px-sm-4 d-flex justify-space-between">
            <v-btn large color="primary" @click="submit" :disabled="!selectedCanteenId || loadingCanteenData">
              Générer mon affiche
            </v-btn>
          </v-col>
        </v-row>
        <v-row class="mt-2">
          <v-col cols="12">
            <DsfrTextarea
              v-model="customText"
              label="Plus de détail (facultatif)"
              counter
              :rules="[(v) => !v || v.length <= 915 || '915 caractères maximum']"
            />
          </v-col>
        </v-row>

        <v-row class="px-4">
          <v-checkbox v-model="showPatData">
            <template v-slot:label>
              <span class="body-2 grey--text text--darken-3">
                Certains de mes produit proviennent d'un PAT en {{ publicationYear }}
              </span>
            </template>
          </v-checkbox>
        </v-row>

        <v-row v-if="showPatData" class="d-block px-4 mt-2">
          <DsfrTextField
            label="Part de produits provenant d'un PAT"
            style="max-width: 400px;"
            append-icon="mdi-percent"
            validate-on-blur
            v-model.number="patPercentage"
            :rules="[validators.isPercentageOrEmpty]"
          />

          <DsfrTextField label="Nom du PAT" v-model="patName" hide-details />
          <v-btn
            x-large
            color="primary"
            @click="submit"
            :disabled="!selectedCanteenId || loadingCanteenData"
            class="my-8"
          >
            Générer mon affiche
          </v-btn>
        </v-row>
      </v-form>

      <v-row>
        <v-col cols="12" md="7" class="text-body-2 mb-2">
          Pour mettre à jour ces données, rendez-vous sur
          <router-link :to="{ name: 'ManagementPage' }" class="text-decoration-underline primary--text text-body-2">
            mes cantines
          </router-link>
          .
        </v-col>
      </v-row>
      <div id="poster-preview" class="poster-sizing mb-8">
        <div class="loading-overlay poster-sizing" v-if="loadingCanteenData">
          <v-progress-circular indeterminate style="position: absolute; left: 50%; top: 15%"></v-progress-circular>
        </div>
        <CanteenPoster
          id="canteen-poster"
          :canteen="selectedCanteen"
          :diagnostic="currentDiagnostic"
          :previousDiagnostic="previousDiagnostic"
          :customText="customText"
          :patPercentage="showPatData ? patPercentage : null"
          :patName="showPatData ? patName : null"
        />
      </div>
    </div>
    <div id="poster-form-page" v-else>
      <div id="poster-generation">
        <v-form ref="form" v-model="formIsValid" id="poster-form" @submit.prevent>
          <h2 class="mb-4">À propos de votre cantine</h2>
          <p>
            <DsfrTextField
              label="Je représente la cantine"
              v-model="form.canteen.name"
              placeholder="nom de l'établissement"
              hide-details="auto"
              :rules="[validators.required]"
              class="my-4"
            />
            dans
            <label for="commune">la commune de</label>
            <DsfrAutocomplete
              id="commune"
              v-model="form.canteen.city"
              placeholder="nom de la commune"
              :loading="loadingCommunes"
              :items="communes"
              :search-input.sync="search"
              auto-select-first
              cache-items
              hide-details="auto"
              :rules="[validators.required]"
              class="my-4"
              no-data-text="Pas de résultats"
            />
          </p>
          <p>
            <DsfrTextField
              label="Nous servons"
              v-model.number="form.canteen.dailyMealCount"
              :rules="[validators.greaterThanZero]"
              placeholder="200"
              class="my-4"
              suffix="repas par jour"
              hide-details="auto"
            />
          </p>
          <h2 class="mb-4">À propos de vos achats</h2>
          <p>
            <DsfrTextField
              :label="
                `Sur l'année de ${form.diagnostic.year}, les achats alimentaires (repas, collations et boissons)
              répresentent`
              "
              id="total"
              v-model.number="form.diagnostic.valueTotalHt"
              :rules="[validators.greaterThanZero, validators.decimalPlaces(2)]"
              placeholder="15000"
              suffix="euros HT"
              class="my-4"
              hide-details="auto"
              validate-on-blur
            />
          </p>
          <p>
            Sur ce total,
            <DsfrTextField
              id="bio"
              v-model.number="form.diagnostic.valueBioHt"
              :rules="[validators.greaterThanZero, validators.decimalPlaces(2)]"
              placeholder="3000"
              suffix="euros HT"
              class="my-4"
              hide-details="auto"
              validate-on-blur
            />
            correspondaient à des
            <label for="bio">produits bio</label>
            ,
            <DsfrTextField
              id="sustainable"
              v-model.number="form.diagnostic.valueSustainableHt"
              :rules="[validators.greaterThanZero, validators.decimalPlaces(2)]"
              placeholder="2000"
              suffix="euros HT"
              class="my-4"
              hide-details="auto"
              validate-on-blur
            />
            correspondaient à des
            <label for="sustainable">produits de qualité et durables (hors bio)</label>
            .
          </p>
          <label for="pat-percent">Part de produits provenant d'un PAT</label>
          <DsfrTextField
            id="pat-percent"
            append-icon="mdi-percent"
            placeholder="30"
            hide-details="auto"
            class="my-4"
            validate-on-blur
            v-model="form.patPercentage"
            :rules="[validators.isPercentageOrEmpty]"
          />

          <label for="pat-name">Nom du PAT</label>
          <DsfrTextField
            id="pat-name"
            class="my-4"
            placeholder="Mon PAT"
            hide-details="auto"
            validate-on-blur
            v-model="form.patName"
          />
          <v-btn x-large class="my-4" color="primary" @click="submit">Générer mon affiche</v-btn>
          <p class="caption" v-if="!isAuthenticated">
            Pour ajouter une photo à l'affiche et accéder à d'autres fonctionnalités,
            <a href="/creer-mon-compte">créez un compte</a>
          </p>
        </v-form>
        <div id="poster-preview" class="ml-8 poster-sizing">
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
import { lastYear, normaliseText } from "@/utils"
import BreadcrumbsNav from "@/components/BreadcrumbsNav"
import DsfrTextField from "@/components/DsfrTextField"
import DsfrAutocomplete from "@/components/DsfrAutocomplete"
import DsfrTextarea from "@/components/DsfrTextarea"

export default {
  components: {
    CanteenPoster,
    BreadcrumbsNav,
    DsfrTextField,
    DsfrAutocomplete,
    DsfrTextarea,
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
      selectedCanteenId: undefined,
      publicationYear: lastYear(),
      loadingCanteenData: false,
      fetchedCanteens: {},
      selectedCanteen: {},
      customText: null,
      showPatData: false,
      patPercentage: null,
      patName: null,
    }
  },
  computed: {
    validators() {
      return validators
    },
    userCanteens() {
      const canteens = this.$store.state.userCanteenPreviews
      return canteens.sort((a, b) => {
        return normaliseText(a.name) > normaliseText(b.name) ? 1 : 0
      })
    },
    userCanteen() {
      return this.userCanteens.length > 0 ? this.userCanteens[0] : {}
    },
    initialDiagnostic() {
      let diagnostics = this.isAuthenticated ? this.serverDiagnostics : this.localDiagnostics
      return (
        diagnostics.find((x) => x.year === this.publicationYear) ||
        Object.assign({}, Constants.DefaultDiagnostics, { year: this.publicationYear })
      )
    },
    serverDiagnostics() {
      return this.userCanteen.diagnostics || []
    },
    localDiagnostics() {
      return this.$store.getters.getLocalDiagnostics()
    },
    isAuthenticated() {
      return !!this.$store.state.loggedUser
    },
    usesCentralKitchenDiagnostics() {
      return (
        this.selectedCanteen?.productionType === "site_cooked_elsewhere" &&
        this.selectedCanteen?.centralKitchenDiagnostics?.length > 0
      )
    },
    diagnosticSet() {
      if (!this.selectedCanteen) return null
      return this.usesCentralKitchenDiagnostics
        ? this.selectedCanteen.centralKitchenDiagnostics
        : this.selectedCanteen.diagnostics
    },
    currentDiagnostic() {
      return this.diagnosticSet?.find((x) => x.year === this.publicationYear) || {}
    },
    previousDiagnostic() {
      return this.diagnosticSet?.find((x) => x.year === this.publicationYear - 1) || {}
    },
    hasCanteens() {
      return !!this.$store.state.userCanteenPreviews && this.$store.state.userCanteenPreviews.length > 0
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
        this.$store.dispatch("notifyRequiredFieldsError")
        return
      }

      if (!this.selectedCanteenId) {
        this.saveDiagnostic()
        this.saveCanteen()
      }

      // this fixes an issue where the beginning of the pdf is blank depending on the scroll position
      window.scrollTo({ top: 0 })

      if (this.$matomo) {
        this.$matomo.trackEvent("form", "submit", "poster-generator")
      }

      const htmlPoster = document.getElementById("canteen-poster")
      const canteenName = this.selectedCanteen.name || this.form.canteen.name
      const pdfOptions = {
        filename: `Affiche_convives_${canteenName.replaceAll(" ", "_")}_${this.form.diagnostic.year}.pdf`,
        image: { type: "jpeg", quality: 1 },
        html2canvas: { scale: 2, dpi: 300, letterRendering: true, useCORS: true },
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
    onCanteenAutocompleteChange() {
      if (!this.selectedCanteenId) {
        this.selectedCanteen = {}
        return
      }
      if (this.fetchedCanteens[this.selectedCanteenId]) {
        this.selectedCanteen = this.fetchedCanteens[this.selectedCanteenId]
        return
      }
      this.loadingCanteenData = true
      this.$store
        .dispatch("fetchCanteen", { id: this.selectedCanteenId })
        .then((response) => {
          this.fetchedCanteens[response.id] = response
          this.selectedCanteen = response
        })
        .catch(() => {
          this.$store.dispatch("notify", {
            message: "Nous n'avons pas trouvé cette cantine",
            status: "error",
          })
        })
        .finally(() => (this.loadingCanteenData = false))
    },
  },
}
</script>

<style scoped lang="scss">
#content {
  width: 210mm;
}

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

.poster-sizing {
  width: 210mm;
  min-width: 210mm;
  height: 296mm;
  min-height: 296mm;
}

#poster-preview {
  border: 1px solid $ma-cantine-grey;
  position: relative;
}

.loading-overlay {
  background: #b0aeae4f;
  position: absolute;
}

@media (max-width: 1200px) {
  #poster-generation {
    flex-direction: column;
    width: auto;
  }
}

@media (max-width: 210mm) {
  #content {
    width: 100%;
  }

  #poster-preview {
    display: none;
  }
}
</style>
