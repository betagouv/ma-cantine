<template>
  <div class="text-left">
    <h1 class="font-weight-black text-h4 my-4">Import des diagnostics via CSV</h1>
    <p>
      Créez plusieurs diagnostics en transferant un fichier CSV suivant les spécifications ci-dessous.
    </p>
    <p>
      Vous pouvez également
      <a class="text-decoration-underline" href="/static/documents/fichier_exemple_ma_cantine.csv" download>
        <v-icon small class="mt-n1 ml-1" color="primary">mdi-file-document-outline</v-icon>
        télécharger un fichier exemple
      </a>
      .
    </p>
    <v-form class="ma-8">
      <v-row class="mt-10">
        <v-col rows="12" md="8" class="d-flex pa-0">
          <v-file-input v-model="file" outlined show-size label="Choisissez un fichier" accept=".csv"></v-file-input>
          <v-btn x-large color="primary" @click="upload" :disabled="!file" class="ml-6">Valider</v-btn>
        </v-col>
      </v-row>
    </v-form>
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
            <th>Exemple</th>
            <th>Obligatoire</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(field, idx) in documentation" :key="idx">
            <td>{{ idx + 1 }}</td>
            <td>{{ field.name }}</td>
            <td v-html="field.description"></td>
            <td style="min-width: 160px;">{{ field.example }}</td>
            <td>{{ field.optional ? "✘" : "✔" }}</td>
          </tr>
        </tbody>
      </template>
    </v-simple-table>

    <h3 class="my-6">Fichier exemple</h3>
    <p>
      Nous mettons à votre disposition
      <a class="text-decoration-underline" href="/static/documents/fichier_exemple_ma_cantine.csv" download>
        <v-icon small class="mt-n1" color="primary">mdi-file-document-outline</v-icon>
        un fichier exemple
      </a>
      à remplir avec vos données.
    </p>
  </div>
</template>

<script>
export default {
  name: "ImportDiagnostics",
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
          description: "Le SIRET de la cantine (14 chiffres)",
          example: "362 521 879 00034",
        },
        {
          name: "Nom de la cantine",
          example: "Ma Cantine",
        },
        {
          name: "Code géographique INSEE de la ville",
          example: "69123",
          optional: true,
        },
        {
          name: "Code postale",
          description: "En cas d'absence de code INSEE, ce champ devient obligatoire",
          example: "69001",
          optional: true,
        },
        {
          name: "SIRET de la cuisine centrale",
          description: "Le SIRET de la cuisine centrale s'il y en a une",
          example: "362 521 879 00034",
          optional: true,
        },
        {
          name: "Nombre de repas servis par jour",
          example: "300",
        },
        {
          name: "Secteurs",
          description: `Options acceptées : ${this.$store.state.sectors.map(
            (x) => " <code>" + x.name + "</code>"
          )}. Spécifiez plusieurs en séparant avec un <code>+</code>.`,
          example: `${this.$store.state.sectors[0].name}+${this.$store.state.sectors[1].name}`,
        },
        {
          name: "Mode de production",
          description:
            "Le lieu de production des repas. Options acceptées : <code>site</code> (cuisine-site) et <code>central</code> (cuisine centrale).",
          example: "central",
        },
        {
          name: "Mode de gestion",
          description:
            "Comment le service des repas est géré. Options acceptées : <code>direct</code> (directe) et <code>conceded</code> (concédé).",
          example: "direct",
        },
        {
          name: "Année du diagnostic",
          description: "En format <code>YYYY</code>.",
          example: "2020",
        },
        {
          name: "Valeur totale d'achats HT",
          description: "En format <code>1234</code>/<code>1234.5</code>/<code>1234.56</code>.",
          example: "3290.23",
        },
        {
          name: "Valeur d'achats bio HT",
          description: "En format <code>1234</code>/<code>1234.5</code>/<code>1234.56</code>.",
          example: "1284.70",
        },
        {
          name: "Valeur d'achats durables et de qualité (hors bio) HT",
          description: "En format <code>1234</code>/<code>1234.5</code>/<code>1234.56</code>.",
          example: "681",
        },
        {
          name: "Valeur d'achats du commerce équitable HT",
          description: "En format <code>1234</code>/<code>1234.5</code>/<code>1234.56</code>.",
          example: "1084.2",
          optional: true,
        },
      ],
    }
  },
  methods: {
    upload() {
      this.$store
        .dispatch("importDiagnostics", { file: this.file })
        .then((json) => {
          this.file = undefined
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
