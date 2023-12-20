<template>
  <div class="text-left fr-body">
    <h1 class="fr-h1">Importer vos données</h1>

    <v-row>
      <v-col><p>Nom du champ</p></v-col>
      <v-col v-for="(_, itemIdx) in processedFileContent" :key="`hr_${itemIdx}`">
        <p class="d-flex justify-space-between">
          <b>{{ itemDisplayName(itemIdx) }}</b>
          <!-- NB: icons should be accessible -->
          <span v-if="itemHasError(itemIdx)">❌</span>
          <span v-else>✔️</span>
        </p>
      </v-col>
    </v-row>
    <v-row v-for="(field, fieldIdx) in defaultFieldOrder" :key="field">
      <v-col>
        <p class="d-flex justify-space-between">
          <b>{{ fields[field].name }}</b>
          <!-- NB: icons should be accessible -->
          <span v-if="fieldHasError(field)">❌</span>
          <span v-else>✔️</span>
        </p>
      </v-col>
      <v-col
        v-for="(line, lineIdx) in processedFileContent"
        :key="lineIdx"
        :class="{
          'field-error': itemFieldHasError(lineIdx, field),
          blink: errorToBlink.lineIdx === lineIdx && errorToBlink.field === field,
        }"
      >
        <p>{{ line[fieldIdx] }}</p>
      </v-col>
    </v-row>

    <h2 class="fr-h2 mt-8">Vérifier les erreurs suivants</h2>
    <v-btn v-for="(error, errorIdx) in errors" :key="errorIdx" @click="goToError(error)" text class="ml-n3">
      {{ error.message }} sur {{ itemDisplayName(error.lineIdx) }}
    </v-btn>
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
      errors: [
        {
          field: "siret",
          lineIdx: 1,
          message: "Faut avoir un SIRET",
        },
      ],
      errorToBlink: {},
    }
  },
  computed: {
    itemsWithErrors() {
      return this.errors.map((error) => error.lineIdx)
    },
    fieldsWithErrors() {
      return this.errors.map((error) => error.field)
    },
  },
  methods: {
    itemDisplayName(itemIdx) {
      return `Cantine #${itemIdx + 1}`
    },
    itemHasError(itemIdx) {
      return this.itemsWithErrors.indexOf(itemIdx) > -1
    },
    fieldHasError(fieldName) {
      return this.fieldsWithErrors.indexOf(fieldName) > -1
    },
    itemFieldHasError(itemIdx, fieldName) {
      return this.itemHasError(itemIdx) && this.fieldHasError(fieldName)
    },
    goToError(error) {
      this.errorToBlink = error
      setTimeout(() => (this.errorToBlink = {}), 1000)
    },
  },
}
</script>

<style scoped>
.field-error {
  background-color: #ff9999;
}
.blink {
  animation: blinker 0.5s step-start infinite;
}
@keyframes blinker {
  50% {
    opacity: 0;
  }
}
</style>
