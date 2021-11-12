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
      @upload="upload"
    />

    <p>
      Si vous avez des questions ou des problèmes, n'hésitez pas à nous contacter à
      <a href="mailto:contact@egalim.beta.gouv.fr">contact@egalim.beta.gouv.fr</a>
      .
    </p>

    <div v-if="!isNaN(count)">
      <v-alert type="success" outlined v-if="count > 0">
        <span class="grey--text text--darken-4 body-2">
          {{ count }}
          <span v-if="count === 1">diagnostic a été créé.</span>
          <span v-else>diagnostics ont été créés.</span>
        </span>
      </v-alert>
      <div v-if="errors && errors.length">
        <p class="text-body-2 red--text text--darken-4" v-if="count === 0">
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
      <router-link :to="{ name: 'ManagementPage' }" class="ma-4">← Retour aux cantines et diagnostics</router-link>
      <v-divider class="my-8"></v-divider>
    </div>
    <h2 class="my-6">Format du fichier</h2>
    <p>
      Le fichier CSV doit être encodé avec UTF-8 et contenir un diagnostic par ligne. Chaque ligne doit aussi inclure
      les informations de la cantine associée. Si un diagnostic pour la même année et la même cantine existe déjà il ne
      sera pas modifié.
    </p>
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
  </div>
</template>

<script>
import FileDrop from "./FileDrop"

export default {
  name: "ImportDiagnostics",
  components: { FileDrop },
  data() {
    return {
      file: undefined,
      canteens: undefined,
      count: undefined,
      errors: undefined,
      seconds: undefined,
      documentation: [
        {
          name: "SIRET",
          description: "Le SIRET de la cantine.",
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
          name: "SIRET de la cuisine centrale",
          description: "Le SIRET de la cuisine centrale.",
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
            "Le lieu de production des repas. Options acceptées : <code>site</code> (cuisine-site) et <code>central</code> (cuisine centrale).",
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
          name: "Année du diagnostic",
          description: "En format <code>YYYY</code>.",
          type: "Chiffre",
          example: "2020",
        },
        {
          name: "Valeur totale d'achats HT",
          description: "En format <code>1234</code>/<code>1234.5</code>/<code>1234.56</code>.",
          type: "Chiffre",
          example: "3290.23",
        },
        {
          name: "Valeur d'achats bio HT",
          description: "En format <code>1234</code>/<code>1234.5</code>/<code>1234.56</code>.",
          type: "Chiffre",
          example: "1284.70",
        },
        {
          name: "Valeur d'achats durables et de qualité (hors bio) HT",
          description: "En format <code>1234</code>/<code>1234.5</code>/<code>1234.56</code>.",
          type: "Chiffre",
          example: "681",
        },
      ],
    }
  },
  methods: {
    upload() {
      this.$store
        .dispatch("importDiagnostics", { file: this.file })
        .then((json) => {
          this.file = null
          this.canteens = json.canteens
          this.count = json.count
          this.errors = json.errors
          this.seconds = json.seconds
          this.$store.dispatch("notify", {
            message: `Fichier traité en ${Math.round(this.seconds)} secondes`,
          })
        })
        .catch(() => {
          this.$store.dispatch("notifyServerError")
        })
    },
  },
}
</script>
