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
      subtitle="Format CSV encodé en UTF-8 attendu"
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
      <v-alert type="success" outlined v-if="purchaseCount > 0">
        <span class="grey--text text--darken-4 body-2">
          {{ purchaseCount }} achats
          <span>ont été créés.</span>
        </span>
      </v-alert>
      <div v-if="errors && errors.length">
        <p class="text-body-2 red--text text--darken-4" v-if="purchaseCount === 0">
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
                <tr v-for="error in errors" :key="error.row">
                  <td>{{ error.row }}</td>
                  <td>{{ error.message }}</td>
                </tr>
              </tbody>
            </template>
          </v-simple-table>
        </v-alert>
      </div>
      <router-link :to="{ name: 'PurchasesHome' }" class="ma-4">← Retourner à mes achats</router-link>
      <v-divider class="my-8"></v-divider>
    </div>
    <h2 class="my-6">Format du fichier</h2>
    <p>
      Le fichier CSV doit être encodé avec UTF-8 et contenir un achat par ligne.
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
import validators from "@/validators"
import Constants from "@/constants"

export default {
  name: "ImportPurchases",
  components: { FileDrop },
  data() {
    const user = this.$store.state.loggedUser
    const numberFormatExample = "En format <code>1234</code>/<code>1234.5</code>/<code>1234.56</code>."
    return {
      file: undefined,
      canteens: undefined,
      purchaseCount: undefined,
      diagnosticCount: undefined,
      errors: undefined,
      seconds: undefined,
      importInProgress: false,
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
          type: "Texte (choix unique)",
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
    }
  },
  methods: {
    upload() {
      this.importInProgress = true
      this.$store
        .dispatch("importPurchases", { file: this.file })
        .then((json) => {
          this.importInProgress = false
          this.file = null
          this.purchaseCount = json.count
          this.errors = json.errors
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
