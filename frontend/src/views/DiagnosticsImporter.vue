<template>
  <div class="text-left">
    <h1 class="font-weight-black text-h4 my-4">Importer diagnostics</h1>
    <v-form class="ma-8">
      <v-row class="mt-10">
        <v-file-input
          v-model="file"
          outlined
          show-size
          label="Fichier des diagnostics"
          accept=".csv"
          class="pr-12"
        ></v-file-input>
        <v-btn x-large color="primary" @click="upload" :disabled="!file">Valider</v-btn>
      </v-row>
    </v-form>
    <div v-if="created || errors">
      <h2 class="my-6">Resultats</h2>
      <p>{{ created.length }} diagnostics ont été créés en {{ Math.round(seconds) }} secondes.</p>
      <div v-if="errors && errors.length">
        <h3 class="my-6">Erreurs</h3>
        <v-simple-table dense class="my-6">
          <template v-slot:default>
            <thead>
              <tr>
                <th>Ligne</th>
                <th>Statut</th>
                <th>Message</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="error in errors" :key="error.row">
                <td>{{ error.row }}</td>
                <td>{{ error.status }}</td>
                <td>{{ error.message }}</td>
              </tr>
            </tbody>
          </template>
        </v-simple-table>
      </div>
      <p v-else>Aucun erreur produit.</p>
      <router-link :to="{ name: 'ManagementPage' }" class="ma-4">← Retour aux cantines et diagnostics</router-link>
      <v-divider class="my-8"></v-divider>
    </div>
    <h2 class="my-6">Documentation</h2>
    <p>
      Ceci est un outil pour importer plusieurs diagnostics avec un fichier CSV. Il est construit pour les cuisines
      centrales pour aider les satellites a télédéclarer et publier ces données.
    </p>
    <p>
      Quand vous téléversez un fichier ici, les diagnostics et cantines vont être créés dans notre base de données.
      Votre compte sera le premier gestionnaire pour chaque cantine. Après que les cantines et diagnostics sont créés,
      vous pouvez les modifier, ajouter d'autres gestionnaires et les publier.
    </p>
    <p>
      Pour importer plusieurs années des diagnostics pour une cantine, on utilise le SIRET pour relier les diagnostics à
      la même cantine.
    </p>
    <h3 class="my-6">Format du fichier</h3>
    <p>Il faut que le fichier soit en format CSV.</p>
    <v-simple-table dense class="my-6">
      <template v-slot:default>
        <thead>
          <tr>
            <th>Ordre</th>
            <th>Champ</th>
            <th>Description</th>
            <th>Obligatoire</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(field, idx) in documentation" :key="idx">
            <td>{{ idx + 1 }}</td>
            <td>{{ field.name }}</td>
            <td v-html="field.description"></td>
            <td>{{ field.optional ? "✘" : "✔" }}</td>
          </tr>
        </tbody>
      </template>
    </v-simple-table>
  </div>
</template>

<script>
const documentation = [
  {
    name: "SIRET",
    description: "Le SIRET de la cantine satellite (d'éspace blanc vont être ignorer)",
  },
  {
    name: "Nom de la cantine",
  },
  {
    name: "Code INSEE de la ville",
    optional: true,
  },
  {
    name: "Code postale",
    description: "Si il n'y a pas un code INSEE, ce champ doit être remplit",
    optional: true,
  },
  {
    name: "SIRET de la cuisine centrale",
    description: "Le SIRET de la cuisine centrale qui gére la cantine (d'éspace blanc vont être ignorer)",
  },
  {
    name: "Nombre de repas servis par jour",
  },
  {
    name: "Secteurs",
    description:
      "Options acceptées : <code>Entreprise</code>, <code>Loisirs</code>, <code>Crèche</code>, <code>Social et Médico-social (ESMS)</code>," +
      "<code>Administration</code>, <code>Médical</code>, <code>Universitaire</code>, <code>Scolaire</code>. Pour spécifier plusieurs, " +
      "les séparer avec '+'. Par exemple, <code>Entreprise+Loisirs</code>.",
  },
  {
    name: "Mode de production",
    description:
      "Le façon dont les repas sont produits. Options acceptées : <code>site</code> (cuisine-site) et <code>central</code> (cuisine centrale).",
  },
  {
    name: "Mode de gestion",
    description:
      "Comment le service des repas est géré. Options acceptées : <code>direct</code> (directe) et <code>conceded</code> (concédé).",
  },
  {
    name: "Année du diagnostic",
    description: "En format <code>YYYY</code>.",
  },
  {
    name: "Totale valeur d'achats HT",
    description: "En format <code>1234</code>/<code>1234.5</code>/<code>1234.56</code>.",
  },
  {
    name: "Valeur d'achats bio HT",
    description: "En format <code>1234</code>/<code>1234.5</code>/<code>1234.56</code>.",
  },
  {
    name: "Valeur d'achats durables et de qualité (hors bio) HT",
    description: "En format <code>1234</code>/<code>1234.5</code>/<code>1234.56</code>.",
  },
  {
    name: "Valeur d'achats du commerce équitable HT",
    description: "En format <code>1234</code>/<code>1234.5</code>/<code>1234.56</code>.",
    optional: true,
  },
]

export default {
  name: "ImportDiagnostics",
  data() {
    return {
      file: undefined,
      created: undefined,
      errors: undefined,
      seconds: undefined,
      documentation,
    }
  },
  methods: {
    upload() {
      console.log(this.file)
      this.$store
        .dispatch("importDiagnostics", { file: this.file })
        .then((json) => {
          this.$store.dispatch("notify", {
            message: "Vos diagnostics a bien été téléversés",
          })
          this.file = undefined
          this.created = json.created
          this.errors = json.errors
          this.seconds = json.seconds
        })
        .catch(() => {
          this.$store.dispatch("notifyServerError")
        })
    },
  },
}
</script>
