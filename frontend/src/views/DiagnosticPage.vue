<template>
  <div class="text-left">
    <h1 class="text-h4 text-center font-weight-black mt-12 mb-6">M'auto-évaluer</h1>
    <v-row class="mb-12">
      <v-spacer></v-spacer>
      <v-col cols="12" sm="8" md="6">
        <h2 class="text-body-1 text-center">
          Évaluez-vous sur les mesures déjà mises en place dans votre établissement, programmées ou celles restantes à
          faire.
        </h2>
      </v-col>
      <v-spacer></v-spacer>
    </v-row>

    <div v-for="measure in keyMeasures" :key="`measure: ${measure.id}`">
      <v-card elevation="0" class="mb-8">
        <v-card-title class="font-weight-bold d-flex">
          <KeyMeasureTitle class="flex-shrink-1" :measure="measure" />
          <v-spacer></v-spacer>
          <v-btn outlined :color="measure.isEvaluated ? 'green' : 'primary'" @click="showDiagnosticModal(measure)">
            <span class="mx-2">
              Je m'évalue
              <span class="d-sr-only">sur la mesure {{ measure.shortTitle }}</span>
              !
            </span>
            <v-icon small color="green" v-if="measure.isEvaluated">mdi-check</v-icon>
          </v-btn>
        </v-card-title>
        <v-card-text class="py-0" v-for="subMeasure in measure.subMeasures" :key="`submeasure: ${subMeasure.id}`">
          <v-btn class="d-inline mt-n1" text plain :ripple="false" @click="toggleDescriptionDisplay(subMeasure)">
            <span>{{ subMeasure.title }}.&nbsp;</span>
            <span class="text-decoration-underline">{{ subMeasure.readMore ? "Moins" : "En savoir plus" }}</span>
          </v-btn>

          <v-alert outlined color="blue-grey lighten-4" :value="subMeasure.readMore" transition="scroll-y-transition">
            <KeyMeasureDescription class="measure-description grey--text text--darken-4" :measure="subMeasure" />
          </v-alert>
        </v-card-text>
      </v-card>

      <v-divider class="mb-2"></v-divider>
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

export default {
  components: {
    KeyMeasureTitle,
    KeyMeasureDescription,
    KeyMeasureDiagnostic,
  },
  data() {
    return {
      keyMeasures,
      measureDiagnosticModal: null,
      diagnosticsCopy: {},
    }
  },
  methods: {
    toggleDescriptionDisplay(subMeasure) {
      subMeasure.readMore = !subMeasure.readMore
    },
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
