<template>
  <div class="text-left">
    <h1 class="text-h4 text-center font-weight-black mt-12 mb-6">M'auto-évaluer</h1>
    <v-row class="mb-12">
      <v-spacer></v-spacer>
      <v-col cols="12" sm="8" md="6">
        <p class="text-body-1 text-center mb-0">
          Évaluez-vous sur les mesures déjà mises en place dans votre établissement, programmées ou celles restantes à
          faire.
        </p>
      </v-col>
      <v-spacer></v-spacer>
    </v-row>

    <div v-for="measure in keyMeasures" :key="`measure: ${measure.id}`" class="mb-10">
      <div class="d-flex flex-column flex-sm-row mb-4 mb-sm-0">
        <h2 class="fr-h6">
          <KeyMeasureTitle class="flex-shrink-1" :measure="measure" />
        </h2>
        <v-spacer></v-spacer>
        <v-btn
          :outlined="measure.isEvaluated"
          :color="measure.isEvaluated ? 'green darken-3' : 'primary'"
          @click="showDiagnosticModal(measure)"
        >
          <span class="mx-2">
            Je m'évalue
            <span class="d-sr-only">sur la mesure {{ measure.shortTitle }}</span>
            !
          </span>
          <v-icon
            small
            color="green darken-3"
            v-if="measure.isEvaluated"
            aria-hidden="false"
            role="img"
            aria-label="(Statut : évalué)"
          >
            mdi-check
          </v-icon>
        </v-btn>
      </div>
      <DsfrAccordion :items="measure.subMeasures">
        <template v-slot:content="{ item }">
          <KeyMeasureDescription class="measure-description grey--text text--darken-4 mb-n4" :measure="item" />
        </template>
      </DsfrAccordion>

      <v-divider aria-hidden="true" role="presentation" class="mb-2"></v-divider>
    </div>

    <v-row class="mb-4 mt-7">
      <v-btn class="mx-auto" color="primary" x-large :to="{ name: 'KeyMeasuresHome' }">
        Récapitulatif
      </v-btn>
    </v-row>

    <v-dialog
      v-model="showModal"
      :max-width="measureDiagnosticModal && measureDiagnosticModal.baseComponent === 'QualityMeasure' ? 900 : 700"
    >
      <v-card class="pa-6">
        <div class="mt-n6 mx-n6 mb-4 pa-4 d-flex" style="background-color: #F5F5F5">
          <v-spacer></v-spacer>
          <v-btn color="primary" outlined @click="showModal = false">
            Fermer
          </v-btn>
        </div>

        <KeyMeasureDiagnostic
          :measure="measureDiagnosticModal"
          @afterSave="setMeasureEvaluated"
          :diagnosticsCopy="diagnosticsCopy"
        />
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { diagnosticsMap } from "@/utils"
import keyMeasures from "@/data/key-measures.json"
import KeyMeasureTitle from "@/components/KeyMeasureTitle"
import KeyMeasureDescription from "@/components/KeyMeasureDescription"
import KeyMeasureDiagnostic from "@/components/KeyMeasureDiagnostic"
import DsfrAccordion from "@/components/DsfrAccordion"

export default {
  components: {
    KeyMeasureTitle,
    KeyMeasureDescription,
    KeyMeasureDiagnostic,
    DsfrAccordion,
  },
  data() {
    return {
      keyMeasures,
      measureDiagnosticModal: null,
      diagnosticsCopy: {},
    }
  },
  methods: {
    showDiagnosticModal(measure) {
      this.measureDiagnosticModal = measure
    },
    closeDiagnosticModal() {
      this.measureDiagnosticModal = null
    },
    setMeasureEvaluated() {
      const measureIndex = this.keyMeasures.findIndex((measure) => measure.id === this.measureDiagnosticModal.id)
      this.keyMeasures[measureIndex].isEvaluated = true
      this.closeDiagnosticModal()
    },
  },
  computed: {
    initialDiagnostics() {
      const diagnostics = this.$store.getters.getLocalDiagnostics()
      return diagnosticsMap(diagnostics)
    },
    showModal: {
      get() {
        return !!this.measureDiagnosticModal
      },
      set(newValue) {
        if (!newValue) this.measureDiagnosticModal = null
      },
    },
  },
  mounted() {
    this.diagnosticsCopy = JSON.parse(JSON.stringify(this.initialDiagnostics))
  },
}
</script>
