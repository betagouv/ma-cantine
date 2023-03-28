<template>
  <div class="text-left">
    <h1 class="font-weight-black text-h4 my-4">
      Générer mon affiche
    </h1>
    <p class="body-1">
      Créez un PDF à afficher ou à envoyer par mail à vos convives pour les informer sur vos initiatives et la
      composition des repas servis dans votre restaurant.
    </p>

    <v-form ref="form" v-model="formIsValid" id="poster-form" @submit.prevent class="mb-4">
      <v-row class="mt-2">
        <v-col cols="12" class="pb-0">
          <DsfrTextarea
            v-model="customText"
            label="Plus de détail (facultatif)"
            counter
            :rules="[(v) => !v || v.length <= 700 || '700 caractères maximum']"
          />
        </v-col>
      </v-row>

      <v-row class="px-4 mt-0">
        <v-checkbox v-model="showPatData">
          <template v-slot:label>
            <span class="body-2 grey--text text--darken-3">
              Certains de mes produit proviennent d'un PAT en {{ publicationYear }}
            </span>
          </template>
        </v-checkbox>
      </v-row>

      <v-row v-if="showPatData" class="d-block px-4 mt-2">
        <v-col cols="12" md="8">
          <DsfrTextField
            label="Part de produits provenant d'un PAT"
            style="max-width: 400px;"
            append-icon="mdi-percent"
            validate-on-blur
            v-model.number="patPercentage"
            :rules="[validators.isPercentageOrEmpty]"
          />

          <DsfrTextField label="Nom du PAT" v-model="patName" hide-details />
        </v-col>
      </v-row>
      <v-btn x-large color="primary" @click="submit" class="my-8">
        Générer mon affiche
      </v-btn>
    </v-form>
    <div id="poster-preview" class="poster-sizing mb-8">
      <CanteenPoster
        id="canteen-poster"
        :canteen="originalCanteen"
        :diagnostic="currentDiagnostic"
        :previousDiagnostic="previousDiagnostic"
        :customText="customText"
        :patPercentage="showPatData ? patPercentage : null"
        :patName="showPatData ? patName : null"
      />
    </div>
  </div>
</template>

<script>
import validators from "@/validators"
import { lastYear } from "@/utils"
import html2pdf from "html2pdf.js"
import CanteenPoster from "@/views/GeneratePosterPage/CanteenPoster"
import DsfrTextField from "@/components/DsfrTextField"
import DsfrTextarea from "@/components/DsfrTextarea"

export default {
  name: "CanteenGeneratePoster",
  components: { CanteenPoster, DsfrTextField, DsfrTextarea },
  props: {
    originalCanteen: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      formIsValid: true,
      publicationYear: lastYear(),
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
    diagnosticSet() {
      return this.usesCentralKitchenDiagnostics
        ? this.originalCanteen.centralKitchenDiagnostics
        : this.originalCanteen.diagnostics
    },
    currentDiagnostic() {
      return this.diagnosticSet?.find((x) => x.year === this.publicationYear) || {}
    },
    previousDiagnostic() {
      return this.diagnosticSet?.find((x) => x.year === this.publicationYear - 1) || {}
    },
  },
  methods: {
    async submit() {
      this.$refs.form.validate()
      if (!this.formIsValid) {
        this.$store.dispatch("notifyRequiredFieldsError")
        return
      }

      // this fixes an issue where the beginning of the pdf is blank depending on the scroll position
      window.scrollTo({ top: 0 })

      if (this.$matomo) {
        this.$matomo.trackEvent("form", "submit", "poster-generator-canteen-page")
      }

      const htmlPoster = document.getElementById("canteen-poster")
      const pdfOptions = {
        filename: `Affiche_convives_${this.originalCanteen.name.replaceAll(" ", "_")}_${this.publicationYear}.pdf`,
        image: { type: "jpeg", quality: 1 },
        html2canvas: { scale: 2, dpi: 300, letterRendering: true, useCORS: true },
        jsPDF: { unit: "in", format: "a4", orientation: "portrait" },
      }
      return html2pdf()
        .from(htmlPoster)
        .set(pdfOptions)
        .save()
    },
  },
  created() {
    document.title = `Générer mon affiche - ${this.originalCanteen.name} - ${this.$store.state.pageTitleSuffix}`
  },
}
</script>

<style scoped lang="scss">
#poster-preview {
  border: 1px solid $ma-cantine-grey;
  position: relative;
}
.poster-sizing {
  width: 210mm;
  min-width: 210mm;
  height: 296mm;
  min-height: 296mm;
}
@media (max-width: 210mm) {
  #poster-preview {
    display: none;
  }
}
</style>
