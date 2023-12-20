<template>
  <div class="text-left fr-body">
    <h1 class="fr-h1">Importer vos données</h1>

    <v-row>
      <v-col><p>Nom du champ</p></v-col>
      <v-col v-for="(_, itemIdx) in processedFileContent" :key="`hr_${itemIdx}`">
        <p class="d-flex justify-space-between">
          <b>Item #{{ itemIdx + 1 }}</b>
          <!-- NB: icons should be accessible -->
          <span v-if="itemHasError(itemIdx)">❌</span>
          <span v-else>✔️</span>
        </p>
      </v-col>
    </v-row>
    <v-row v-for="(field, idx) in defaultFieldOrder" :key="field">
      <v-col>
        <p class="d-flex justify-space-between">
          <b>{{ fields[field].name }}</b>
          <!-- NB: icons should be accessible -->
          <span v-if="fieldHasError(field)">❌</span>
          <span v-else>✔️</span>
        </p>
      </v-col>
      <v-col v-for="(line, itemIdx) in processedFileContent" :key="itemIdx">
        <p>{{ line[idx] }}</p>
      </v-col>
    </v-row>
  </div>
</template>

<script>
const fields = {
  siret: {
    name: "SIRET",
  },
  name: {
    name: "Nom de la cantine",
  },
}

const defaultFieldOrder = ["siret", "name"]

export default {
  name: "EveryoneGetsToImport",
  data() {
    return {
      // constants
      fields,
      defaultFieldOrder,
      // variables
      processedFileContent: [
        ["75461089423143", "Cantine de l'avenir"],
        ["", "Cantine sans SIRET"],
      ],
    }
  },
  computed: {
    itemsWithErrors() {
      return [1]
    },
    fieldsWithErrors() {
      return ["siret"]
    },
  },
  methods: {
    itemHasError(itemIdx) {
      return this.itemsWithErrors.indexOf(itemIdx) > -1
    },
    fieldHasError(fieldName) {
      return this.fieldsWithErrors.indexOf(fieldName) > -1
    },
  },
}
</script>
