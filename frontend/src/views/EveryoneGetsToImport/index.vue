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
        <!-- this could become a drop down field with all the column options -->
        <!-- if a column is selected that is already elsewhere, clear the other field -->
        <!-- and require the user to specify what it is -->
        <p class="d-flex">
          <v-select
            v-if="idxForField === fieldIdx"
            v-model="fieldToMove"
            :items="fieldOptions"
            item-text="name"
            @change="updateFieldOrder"
          />
          <b v-else>{{ fields[field].name }}</b>
          <v-spacer />
          <v-btn v-if="idxForField !== fieldIdx" @click="idxForField = fieldIdx" text small>changer</v-btn>
          <!-- NB: icons should be accessible -->
          <span v-if="fieldHasError(field)">❌</span>
          <span v-else>✔️</span>
        </p>
      </v-col>
      <v-col
        v-for="(line, lineIdx) in processedFileContent"
        :key="lineIdx"
        :class="{
          'field-error': !!itemFieldError(lineIdx, field),
          blink: errorToBlink.lineIdx === lineIdx && errorToBlink.field === field,
        }"
        :title="itemFieldError(lineIdx, field) ? itemFieldError(lineIdx, field).message : ''"
      >
        <!-- TODO: replace problematic tooltip hover text with a toggletip style:
        https://inclusive-components.design/tooltips-toggletips/ -->
        <p>{{ line[fieldIdx] }}</p>
      </v-col>
    </v-row>

    <div v-if="errors.length">
      <h2 class="fr-h2 mt-8">Vérifier les erreurs suivantes</h2>
      <ul>
        <li v-for="(error, errorIdx) in errors" :key="errorIdx">
          <v-btn @click="goToError(error)" text class="ml-n3">
            {{ error.message }} sur {{ itemDisplayName(error.lineIdx) }}
          </v-btn>
        </li>
      </ul>
      <p v-if="processingFile">
        <v-progress-circular indeterminate color="primary" />
        <span>Upload en cours...</span>
      </p>
      <p v-else>
        <v-btn @click="checkErrors" large color="primary" outlined class="fr-text-lg mt-4">
          Upload nouveau fichier
        </v-btn>
      </p>
    </div>
    <div v-else-if="importSuccess">
      <h2 class="fr-h2 mt-8">Félicitations !</h2>
      <v-btn :to="{ name: 'ManagementPage' }" color="primary">Mon tableau de bord</v-btn>
    </div>
    <div v-else>
      <h2 class="fr-h2 mt-8">Vérifier que tout est bon !</h2>
      <p>Il n'y a pas d'erreurs avec cet import !</p>
      <p>Vérifiez que les actions suivantes sont attendues :</p>
      <ul>
        <li>
          Je vais créer
          <b>{{ createCount }}</b>
          {{ itemWord(createCount) }}
        </li>
        <li>
          Je vais modifier
          <b>{{ modifyCount }}</b>
          {{ itemWord(modifyCount) }}
        </li>
      </ul>
      <p v-if="importingData">
        <v-progress-circular indeterminate color="primary" />
        <span>Import en cours...</span>
      </p>
      <p v-else>
        <!-- checkbox: "Je suis authorisé.e de faire cet import pour l'utilisateur" -->
        <!-- in the case where it is a team member and there are canteens they don't manage there -->
        <v-btn @click="completeImport" large color="primary" class="fr-text-lg mt-4">Importer ces données</v-btn>
      </p>
    </div>
  </div>
</template>

<script>
const FIELDS = {
  siret: {
    value: "siret",
    name: "SIRET",
  },
  name: {
    value: "name",
    name: "Nom de la cantine",
  },
}

const DEFAULT_FIELD_ORDER = ["siret", "name"]

const LOADING_STATUS_ENUM = {
  processingFile: "processingFile",
  importing: "importing",
}

export default {
  name: "EveryoneGetsToImport",
  data() {
    return {
      // constants
      fields: FIELDS,
      defaultFieldOrder: DEFAULT_FIELD_ORDER,
      // variables
      userFieldOrder: DEFAULT_FIELD_ORDER,
      processedFileContent: [
        ["75461089423143", ""],
        ["", "Cantine sans SIRET"],
      ],
      errors: [
        {
          field: "name",
          lineIdx: 0,
          message: "Faut avoir un nom de la cantine",
        },
        {
          field: "siret",
          lineIdx: 1,
          message: "Faut avoir un SIRET",
          // we could imagine having an errorId field and grouping together errors by id to have less
          // overwhelming UI, esp when the columns are just in a bad order
        },
      ],
      errorToBlink: {},
      itemsToCreate: [],
      itemsToModify: [],
      waitingForWhat: null,
      importSuccess: false,
      idxForField: null,
      fieldToMove: null,
    }
  },
  computed: {
    itemsWithErrors() {
      return this.errors.map((error) => error.lineIdx)
    },
    fieldsWithErrors() {
      return this.errors.map((error) => error.field)
    },
    createCount() {
      return this.itemsToCreate.length
    },
    modifyCount() {
      return this.itemsToModify.length
    },
    processingFile() {
      return this.waitingForWhat === LOADING_STATUS_ENUM.processingFile
    },
    importingData() {
      return this.waitingForWhat === LOADING_STATUS_ENUM.importing
    },
    fieldOptions() {
      return DEFAULT_FIELD_ORDER.map((f) => FIELDS[f])
    },
  },
  methods: {
    itemWord(itemCount) {
      if (itemCount === 1) {
        return "cantine"
      } else {
        return "cantines"
      }
    },
    itemDisplayName(itemIdx) {
      return `${this.itemWord(1)} #${itemIdx + 1}`
    },
    itemHasError(itemIdx) {
      return this.itemsWithErrors.indexOf(itemIdx) > -1
    },
    fieldHasError(fieldName) {
      return this.fieldsWithErrors.indexOf(fieldName) > -1
    },
    itemFieldError(itemIdx, fieldName) {
      // potential problems with perf if iterating v large imports, since this is called a few times
      return this.errors.find((error) => error.lineIdx === itemIdx && error.field === fieldName)
    },
    goToError(error) {
      this.errorToBlink = error
      setTimeout(() => (this.errorToBlink = {}), 1000)
    },
    completeImport() {
      this.waitingForWhat = LOADING_STATUS_ENUM.importing
      setTimeout(() => {
        this.importSuccess = true
        this.waitingForWhat = null
      }, 1000)
    },
    checkErrors() {
      this.waitingForWhat = LOADING_STATUS_ENUM.processingFile
      setTimeout(() => {
        this.processedFileContent = [
          ["75461089423143", "Cantine de l'avenir"],
          ["36419155442551", "Cantine avec SIRET"],
        ]
        this.errors = []
        this.itemsToCreate = [{ siret: "75461089423143", name: "Cantine de l'avenir" }]
        this.itemsToModify = [{ siret: "36419155442551", name: "Cantine avec SIRET" }]
        this.waitingForWhat = null
      }, 1000)
    },
    updateFieldOrder() {
      if (!this.fieldToMove) {
        this.idxForField = null
        this.fieldToMove = null
        return
      }
      const currentField = this.userFieldOrder[this.idxForField]
      const fieldHasChanged = currentField !== this.fieldToMove
      if (fieldHasChanged) {
        const fieldUsedToBeAtIdx = this.userFieldOrder.indexOf(this.fieldToMove)
        if (fieldUsedToBeAtIdx === -1) {
          // if it isn't in array that's weird. Reset?
          return
        }
        const fieldBeingReplaced = this.userFieldOrder[this.idxForField]
        this.userFieldOrder[this.idxForField] = this.fieldToMove
        this.userFieldOrder[fieldUsedToBeAtIdx] = fieldBeingReplaced // swap columns
        // TODO: debug error highlighting post column order change
      }
      this.idxForField = null
      this.fieldToMove = null
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
