<template>
  <div class="text-left">
    <h1 class="font-weight-black text-h4 my-4">Créer des achats via CSV</h1>
    <p>
      Créez plusieurs achats pour vos cantines en transférant un fichier CSV suivant les spécifications ci-dessous.
    </p>
    <p>
      Vous pouvez également télécharger un fichier exemple en format de choix :
      <a class="text-decoration-underline" href="/static/documents/achats_fichier_exemple_ma_cantine.csv" download>
        <v-icon small class="mt-n1 ml-1" color="primary">mdi-file-document-outline</v-icon>
        CSV (.csv)
      </a>
      <a class="text-decoration-underline" href="/static/documents/achats_fichier_exemple_ma_cantine.xlsx" download>
        <v-icon small class="mt-n1 ml-1" color="primary">mdi-file-document-outline</v-icon>
        Excel (.xlsx)
      </a>
      <a class="text-decoration-underline" href="/static/documents/achats_fichier_exemple_ma_cantine.ods" download>
        <v-icon small class="mt-n1 ml-1" color="primary">mdi-file-document-outline</v-icon>
        OpenDocument (.ods)
      </a>
      .
    </p>

    <FileDrop
      v-model="file"
      subtitle="Format CSV attendu"
      :acceptTypes="['.csv', 'text/csv', '.tsv', 'text/tsv']"
      maxSize="10485760"
      @upload="upload"
      :disabled="importInProgress"
    />

    <p>
      Si vous avez des questions ou des problèmes, n'hésitez pas à nous contacter à
      <a href="mailto:support-egalim@beta.gouv.fr">support-egalim@beta.gouv.fr</a>
      .
    </p>

    <v-card outlined class="pa-4" v-if="importInProgress">
      <v-progress-circular indeterminate color="primary" size="28" class="mr-4"></v-progress-circular>
      <span class="mt-1">Traitement en cours...</span>
    </v-card>
    <div v-if="!isNaN(purchaseCount) && !importInProgress">
      <v-alert type="success" outlined v-if="!duplicateFile && purchaseCount > 0">
        <span class="grey--text text--darken-4 body-2">
          {{ purchaseCount }} achats
          <span>ont été créés.</span>
        </span>
      </v-alert>
      <div v-if="duplicateFile">
        <p class="orange--text text--darken-4">
          Ce fichier a déjà été utilisé pour importer {{ duplicatePurchaseCount }}
          <span v-if="duplicatePurchaseCount > 1">achats.</span>
          <span v-else>achat.</span>
        </p>
        <p class="orange--text text--darken-4" v-if="duplicatePurchaseCount > 10">
          Les premiers dix achats sont affichés ci-dessous.
        </p>
        <p class="orange--text text--darken-4" v-else>Les achats sont affichés ci-dessous.</p>
        <PurchasesTable :purchases="duplicatePurchases" :hide-default-footer="true" class="mb-6" />
      </div>
      <div v-else-if="errors && errors.length">
        <p class="red--text text--darken-4" v-if="errors.length < errorCount">
          Votre fichier contient {{ errorCount }} lignes avec des erreurs. Vous trouverez ci-dessous les 30 premières
          erreurs rencontrées :
        </p>
        <p class="red--text text--darken-4" v-else>
          Nous n'avons pas pu traiter votre fichier. Vous trouverez ci-dessous des informations sur les erreurs
          rencontrées.
        </p>
        <v-alert type="error" outlined>
          <v-simple-table color="red" dense>
            <template v-slot:default>
              <thead>
                <tr>
                  <th>Ligne</th>
                  <th>Erreur</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(error, idx) in errors" :key="idx">
                  <td>{{ error.row }}</td>
                  <td>{{ error.message }}</td>
                </tr>
              </tbody>
            </template>
          </v-simple-table>
        </v-alert>
      </div>
      <router-link :to="{ name: 'PurchasesHome' }" class="ma-4">← Retourner à mes achats</router-link>
      <v-divider aria-hidden="true" role="presentation" class="my-8"></v-divider>
    </div>
    <h2 class="my-6">Format du fichier</h2>
    <p>
      Le fichier CSV doit contenir un achat par ligne.
    </p>
    <p>Les données doivent être présentées dans l'ordre indiqué ci-dessous.</p>
    <h3 class="my-6">Colonnes</h3>
    <v-simple-table class="my-6">
      <template v-slot:default>
        <thead>
          <tr>
            <th>Colonne</th>
            <th>Champ</th>
            <th>Description</th>
            <th>Type</th>
            <th>Exemple</th>
            <th>Obligatoire</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(field, idx) in documentation" :key="idx">
            <td class="text-center">{{ idx + 1 }}</td>
            <td>{{ field.name }}</td>
            <td v-html="field.description"></td>
            <td style="min-width: 150px;">{{ field.type }}</td>
            <td>{{ field.example }}</td>
            <td class="text-center">{{ field.optional ? "✘" : "✔" }}</td>
          </tr>
        </tbody>
      </template>
    </v-simple-table>

    <h3 class="my-6">Fichier exemple</h3>
    <p>
      Nous mettons à votre disposition un fichier exemple en format de choix :
      <a class="text-decoration-underline" href="/static/documents/achats_fichier_exemple_ma_cantine.csv" download>
        <v-icon small class="mt-n1 ml-1" color="primary">mdi-file-document-outline</v-icon>
        CSV (.csv)
      </a>
      <a class="text-decoration-underline" href="/static/documents/achats_fichier_exemple_ma_cantine.xlsx" download>
        <v-icon small class="mt-n1 ml-1" color="primary">mdi-file-document-outline</v-icon>
        Excel (.xlsx)
      </a>
      <a class="text-decoration-underline" href="/static/documents/achats_fichier_exemple_ma_cantine.ods" download>
        <v-icon small class="mt-n1 ml-1" color="primary">mdi-file-document-outline</v-icon>
        OpenDocument (.ods)
      </a>
      à remplir avec vos données.
    </p>

    <p>
      Si vous avez des questions ou des problèmes, n'hésitez pas à nous contacter à
      <a href="mailto:support-egalim@beta.gouv.fr">support-egalim@beta.gouv.fr</a>
      .
    </p>
  </div>
</template>

<script>
import FileDrop from "@/components/FileDrop"
import PurchasesTable from "@/components/PurchasesTable"
import validators from "@/validators"
import Constants from "@/constants"

export default {
  name: "ImportPurchases",
  components: { FileDrop, PurchasesTable },
  data() {
    const user = this.$store.state.loggedUser
    const numberFormatExample = "En format <code>1234</code>/<code>1234.5</code>/<code>1234.56</code>."
    return {
      file: undefined,
      canteens: undefined,
      purchaseCount: undefined,
      diagnosticCount: undefined,
      errors: undefined,
      errorCount: undefined,
      seconds: undefined,
      importInProgress: false,
      duplicatePurchases: null,
      documentation: [
        {
          name: "SIRET de la cantine ayant réalisé l'achat",
          description: "La cantine avec ce SIRET doit être déjà enregistrée sur notre plateforme.",
          type: "14 chiffres, avec ou sans espaces",
          example: "000 000 000 00000",
        },
        {
          name: "Description de l'achat",
          example: "Pommes de terre",
          type: "Texte libre",
        },
        {
          name: "Fournisseur",
          example: "Le traiteur du village",
          type: "Texte libre",
        },
        {
          name: "Date d'achat",
          type: "Date en format AAAA-MM-JJ",
          example: "2022-01-30",
        },
        {
          name: "Prix HT",
          description: numberFormatExample,
          type: "Chiffre",
          example: "3290.23",
        },
        {
          name: "Famille de produits",
          description: `Options acceptées : ${Object.keys(Constants.ProductFamilies).map(
            (x) => " <code>" + x + "</code>"
          )}`,
          type: "Texte (choix unique)",
          example: `${Object.keys(Constants.ProductFamilies)[0]}`,
        },
        {
          name: "Caractéristiques",
          description: `Options acceptées : ${Object.keys(Constants.Characteristics).map(
            (x) => " <code>" + x + "</code>"
          )}. Spécifiez plusieurs en séparant avec un <code>,</code>.`,
          type: "Texte",
          example: `${Object.keys(Constants.Characteristics)[0]},${Object.keys(Constants.Characteristics)[3]}`,
        },
        {
          name: "Définition de local",
          description: `Obligatoire si l'achat a la caractéristique de LOCAL. Options acceptées : ${Object.keys(
            Constants.LocalDefinitions
          ).map((x) => " <code>" + x + "</code>")}.`,
          type: "Texte (choix unique)",
          example: `${Object.keys(Constants.LocalDefinitions)[0]}`,
        },
      ],
      validators,
      isStaff: user.isStaff,
      duplicateFile: false,
    }
  },
  methods: {
    upload() {
      this.importInProgress = true
      this.duplicateFile = false
      this.$store
        .dispatch("importPurchases", { file: this.file })
        .then((json) => {
          this.importInProgress = false
          this.file = null
          this.purchaseCount = json.count
          this.errors = json.errors
          this.errorCount = json.errorCount
          this.duplicateFile = json.duplicateFile
          this.duplicatePurchases = json.duplicatePurchases
          this.duplicatePurchaseCount = json.duplicatePurchaseCount
          this.seconds = json.seconds
          this.$store.dispatch("notify", {
            message: `Fichier traité en ${Math.round(this.seconds)} secondes`,
          })
          if (this.$matomo) {
            this.$matomo.trackEvent("inquiry", "send", "import-purchases-success")
          }
        })
        .catch((e) => {
          this.importInProgress = false
          this.$store.dispatch("notifyServerError", e)
        })
    },
  },
}
</script>
