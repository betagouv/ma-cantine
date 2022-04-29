<template>
  <div class="text-left">
    <h1 class="font-weight-black text-h4 my-4">Créer des cantines via CSV</h1>
    <p>
      Créez plusieurs cantines et diagnostics en transférant un fichier CSV suivant les spécifications ci-dessous.
    </p>
    <p>
      Vous pouvez également télécharger un fichier exemple en format de choix :
      <a class="text-decoration-underline" href="/static/documents/fichier_exemple_ma_cantine.csv" download>
        <v-icon small class="mt-n1 ml-1" color="primary">mdi-file-document-outline</v-icon>
        CSV (.csv)
      </a>
      <a class="text-decoration-underline" href="/static/documents/fichier_exemple_ma_cantine.xlsx" download>
        <v-icon small class="mt-n1 ml-1" color="primary">mdi-file-document-outline</v-icon>
        Excel (.xlsx)
      </a>
      <a class="text-decoration-underline" href="/static/documents/fichier_exemple_ma_cantine.ods" download>
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
      <a href="mailto:contact@egalim.beta.gouv.fr">contact@egalim.beta.gouv.fr</a>
      .
    </p>

    <v-card outlined class="pa-4" v-if="importInProgress">
      <v-progress-circular indeterminate color="primary" size="28" class="mr-4"></v-progress-circular>
      <span class="mt-1">Traitement en cours...</span>
    </v-card>
    <div v-if="!isNaN(canteenCount) && !importInProgress">
      <v-alert type="success" outlined v-if="canteenCount > 0">
        <span class="grey--text text--darken-4 body-2">
          {{ canteenCount }} cantines
          <span v-if="diagnosticCount">et {{ diagnosticCount }} diagnostics&nbsp;</span>
          <span>ont été {{ diagnosticCount ? "traités" : "traitées" }}.</span>
        </span>
      </v-alert>
      <div v-if="errors && errors.length">
        <p class="text-body-2 red--text text--darken-4" v-if="canteenCount === 0">
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
      <router-link :to="{ name: 'ManagementPage' }" class="ma-4">← Retourner à mes cantines</router-link>
      <v-divider class="my-8"></v-divider>
    </div>
    <h2 class="my-6">Format du fichier</h2>
    <p>
      Le fichier CSV doit être encodé avec UTF-8 et contenir un diagnostic par ligne. Chaque ligne doit aussi inclure
      les informations de la cantine associée.
    </p>
    <p>Les données doivent être présentées dans l'ordre indiqué ci-dessous.</p>
    <p>Si un diagnostic pour la même année et la même cantine existe déjà il ne sera pas modifié.</p>
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
            <td>{{ field.type }}</td>
            <td style="min-width: 160px;">{{ field.example }}</td>
            <td class="text-center">{{ field.optional ? "✘" : "✔" }}</td>
          </tr>
        </tbody>
      </template>
    </v-simple-table>

    <h3 class="my-6">Fichier exemple</h3>
    <p>
      Nous mettons à votre disposition un fichier exemple en format de choix :
      <a class="text-decoration-underline" href="/static/documents/fichier_exemple_ma_cantine.csv" download>
        <v-icon small class="mt-n1 ml-1" color="primary">mdi-file-document-outline</v-icon>
        CSV (.csv)
      </a>
      <a class="text-decoration-underline" href="/static/documents/fichier_exemple_ma_cantine.xlsx" download>
        <v-icon small class="mt-n1 ml-1" color="primary">mdi-file-document-outline</v-icon>
        Excel (.xlsx)
      </a>
      <a class="text-decoration-underline" href="/static/documents/fichier_exemple_ma_cantine.ods" download>
        <v-icon small class="mt-n1 ml-1" color="primary">mdi-file-document-outline</v-icon>
        OpenDocument (.ods)
      </a>
      à remplir avec vos données.
    </p>

    <h2 class="my-6">Vous avez besoin d'aide ?</h2>
    <p>
      Si votre fichier comptable agrégé ne ressemble pas du tout à ça, vous pouvez nous l'envoyer en remplissant les
      champs ci-dessous ou nous contacter directement à l'adresse
      <a href="mailto:contact@egalim.beta.gouv.fr">contact@egalim.beta.gouv.fr</a>
      .
    </p>
    <v-form v-model="helpFormIsValid" ref="helpForm" @submit.prevent class="my-12">
      <v-row class="mb-1">
        <v-col cols="12" md="6" class="py-0">
          <v-text-field
            v-model="fromEmail"
            label="Votre email"
            :rules="[validators.email]"
            validate-on-blur
            outlined
          ></v-text-field>
        </v-col>
        <v-col class="py-0">
          <v-text-field v-model="name" label="Prénom et nom" outlined></v-text-field>
        </v-col>
      </v-row>
      <v-textarea v-model="message" label="Message (facultatif)" outlined></v-textarea>
      <v-file-input
        v-model="unusualFile"
        label="Fichier"
        outlined
        :rules="[validators.required, validators.maxFileSize(10485760, '10 Mo')]"
        validate-on-blur
        show-size
      />
      <v-btn x-large color="primary" @click="emailUnusualFile">
        <v-icon class="mr-2">mdi-send</v-icon>
        Envoyer
      </v-btn>
    </v-form>
  </div>
</template>

<script>
import FileDrop from "@/components/FileDrop"
import validators from "@/validators"

export default {
  name: "ImportDiagnostics",
  components: { FileDrop },
  data() {
    const user = this.$store.state.loggedUser
    const numberFormatExample = "En format <code>1234</code>/<code>1234.5</code>/<code>1234.56</code>."
    return {
      file: undefined,
      canteens: undefined,
      canteenCount: undefined,
      diagnosticCount: undefined,
      errors: undefined,
      seconds: undefined,
      importInProgress: false,
      documentation: [
        {
          name: "SIRET de la cuisine-site",
          description: "Ce SIRET doit être unique car il correspond à un lieu physique.",
          type: "14 chiffres, avec ou sans espaces",
          example: "000 000 000 00000",
        },
        {
          name: "Nom de la cantine",
          example: "Ma Cantine",
          type: "Texte libre",
        },
        {
          name: "Code géographique INSEE de la ville",
          example: "69123",
          optional: true,
        },
        {
          name: "Code postal",
          description: "En cas d'absence de code INSEE, ce champ devient obligatoire.",
          example: "69001",
          optional: true,
        },
        {
          name: "SIRET de la cantine distributrice ou SRC",
          description:
            "Ce SIRET peut être vide ou utilisé pour plusieurs lignes, dans le cas où c'est le gestionnaire de la SRC ou de la cuisine centrale qui remplit les lignes pour chaque cuisine-site/satellite.",
          type: "14 chiffres, avec ou sans espaces",
          example: "999 999 999 99999",
          optional: true,
        },
        {
          name: "Nombre de repas servis par jour",
          type: "Chiffre",
          example: "300",
        },
        {
          name: "Secteurs",
          description: `Options acceptées : ${this.$store.state.sectors.map(
            (x) => " <code>" + x.name + "</code>"
          )}. Spécifiez plusieurs en séparant avec un <code>+</code>.`,
          type: "Texte (choix unique)",
          example: `${this.$store.state.sectors[0].name}+${this.$store.state.sectors[1].name}`,
        },
        {
          name: "Mode de production",
          description:
            "Le mode de production de votre cantine. Les options :<br />- <code>central</code> si vous êtes une cuisine centrale sans lieu de consommation<br/>- <code>central_serving</code> si vous êtes une cuisine centrale qui accueille aussi des convives sur place,<br/>- <code>site</code> si vous êtes une cantine qui produit les repas sur place, et<br/>- <code>site_cooked_elsewhere</code> si vous êtes une cantine qui sert des repas preparés par une cuisine centrale.<br/>",
          type: "Texte (choix unique)",
          example: "central",
        },
        {
          name: "Mode de gestion",
          description:
            "Comment le service des repas est géré. Options acceptées : <code>direct</code> (directe) et <code>conceded</code> (concédé).",
          type: "Texte (choix unique)",
          example: "direct",
        },
        {
          name: "Secteur économique",
          description:
            "Le type d'établissement. Options acceptées : <code>public</code> et <code>private</code> (privé).",
          type: "Texte (choix unique)",
          example: "public",
        },
        {
          name: "Gestionnaires additionnels (adresses emails)",
          description:
            "Les personnes avec ces adresses seront considérées comme gestionnaires de la cantine et pourront modifier toutes ses données.",
          type: "Texte (adresses email séparées par une virgule)",
          example: "gestionnaire1@example.com, gestionnaire2@example.com",
          optional: true,
        },
        {
          name: "Année du diagnostic",
          description: "En format <code>YYYY</code>.",
          type: "Chiffre",
          example: "2020",
        },
        {
          name: "Valeur totale d'achats HT",
          description: numberFormatExample,
          type: "Chiffre",
          example: "3290.23",
        },
        {
          name: "Valeur d'achats bio HT",
          description: numberFormatExample,
          type: "Chiffre",
          example: "1284.70",
        },
        {
          name: "Valeur d'achats durables et de qualité (hors bio) HT",
          description: numberFormatExample,
          type: "Chiffre",
          example: "681",
        },
        {
          name: "Valeur d'achats Label Rouge HT",
          description: numberFormatExample,
          type: "Chiffre",
          example: "681",
          optional: true,
        },
        {
          name: "Valeur d'achats Label AOC / AOP / IGP HT",
          description: numberFormatExample,
          type: "Chiffre",
          example: "681",
          optional: true,
        },
        {
          name: "Valeur d'achats HVE HT",
          description: numberFormatExample,
          type: "Chiffre",
          example: "681",
          optional: true,
        },
      ],
      validators,
      helpFormIsValid: true,
      fromEmail: user ? user.email : "",
      name: user ? `${user.firstName} ${user.lastName}` : "",
      message: "",
      unusualFile: null,
    }
  },
  methods: {
    upload() {
      this.importInProgress = true
      this.$store
        .dispatch("importDiagnostics", { file: this.file })
        .then((json) => {
          this.importInProgress = false
          this.file = null
          this.canteens = json.canteens
          this.canteenCount = json.canteens.length
          this.diagnosticCount = json.count
          this.errors = json.errors
          this.seconds = json.seconds
          this.$store.dispatch("notify", {
            message: `Fichier traité en ${Math.round(this.seconds)} secondes`,
          })
          if (this.$matomo) {
            this.$matomo.trackEvent("inquiry", "send", "import-diagnostics-success")
          }
        })
        .catch((e) => {
          this.importInProgress = false
          this.$store.dispatch("notifyServerError", e)
        })
    },
    emailUnusualFile() {
      this.$refs.helpForm.validate()
      if (!this.helpFormIsValid) {
        this.$store.dispatch("notifyRequiredFieldsError")
        return
      }
      let form = new FormData()
      form.append("file", this.unusualFile)
      form.append("name", this.name)
      form.append("email", this.fromEmail)
      form.append("message", this.message)
      fetch("/api/v1/emailDiagnosticImportFile/", {
        method: "POST",
        headers: {
          "X-CSRFToken": window.CSRF_TOKEN || "",
        },
        body: form,
      })
        .then((response) => {
          if (response.ok) {
            this.$store.dispatch("notify", {
              status: "success",
              title: "Fichier envoyé",
              message: "Merci, nous vous contacterons dans les plus brefs délais.",
            })
            this.unusualFile = null
            this.message = ""
          } else {
            this.$store.dispatch("notifyServerError", response)
          }
        })
        .catch((e) => {
          this.$store.dispatch("notifyServerError", e)
        })
    },
  },
}
</script>
