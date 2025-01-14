<template>
  <div class="text-left">
    <h1 class="font-weight-black text-h4 my-4">Créer des achats via CSV</h1>
    <p>
      Créez plusieurs achats pour vos cantines en transférant un fichier CSV suivant les spécifications ci-dessous.
    </p>
    <p>
      Vous pouvez également télécharger un fichier exemple :
      <a class="text-decoration-underline" href="/static/documents/achats_fichier_exemple_ma_cantine.csv" download>
        <v-icon small class="mt-n1 ml-1" color="primary">mdi-file-document-outline</v-icon>
        CSV (.csv)
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
      <ImporterSuccessDialog
        :isOpen="showSuccessDialog && !duplicateFile && purchaseCount > 0"
        :description="
          purchaseCount > 1
            ? 'Vos achats sont enregistrés et sont maintenant disponibles.'
            : 'Votre achat est enregistré et est maintenant disponible.'
        "
      />
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
      Le fichier CSV doit commencer par une ligne en-tête avec le nom des colonnes exactement comme listé ci-dessous
      dans "Titre". Il doit ensuite contenir un achat par ligne.
    </p>
    <p>Les données doivent être présentées dans l'ordre indiqué ci-dessous.</p>
    <h3 class="my-6">Colonnes</h3>
    <SchemaTable :schemaUrl="purchaseSchemaUrl" />

    <h3 class="my-6">Fichier exemple</h3>
    <p>
      Nous mettons à votre disposition un fichier exemple :
      <a class="text-decoration-underline" href="/static/documents/achats_fichier_exemple_ma_cantine.csv" download>
        <v-icon small class="mt-n1 ml-1" color="primary">mdi-file-document-outline</v-icon>
        CSV (.csv)
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
import SchemaTable from "@/components/SchemaTable"
import validators from "@/validators"
import ImporterSuccessDialog from "@/components/ImporterSuccessDialog.vue"

export default {
  name: "ImportPurchases",
  components: { FileDrop, PurchasesTable, SchemaTable, ImporterSuccessDialog },
  data() {
    const user = this.$store.state.loggedUser
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
      purchaseSchemaUrl:
        "https://raw.githubusercontent.com/betagouv/ma-cantine/refs/heads/main/data/schemas/imports/achats.json",
      validators,
      isStaff: user.isStaff,
      duplicateFile: false,
      showSuccessDialog: false,
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
          this.showSuccessDialog = true
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
