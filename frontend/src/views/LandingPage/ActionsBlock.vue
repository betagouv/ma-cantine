<template>
  <div>
    <v-row class="text-left">
      <v-spacer></v-spacer>
      <v-col cols="12" sm="6">
        <v-card elevation="0" class="fill-height pa-4 d-flex flex-column">
          <v-img
            src="/static/images/ChartDoodle.png"
            v-if="$vuetify.breakpoint.smAndUp"
            class="mx-auto rounded-0"
            contain
            max-height="130"
          ></v-img>
          <v-card-title>
            <h2 class="text-h6 font-weight-bold">
              Vous connaissez déjà la part de bio, durable et produits issus du commerce équitable de votre cantine
              scolaire
            </h2>
          </v-card-title>
          <v-card-text>
            Vous pouvez générer une affiche à poser dans votre cantine ainsi qu’un email-type à destination des convives
            et parents d'élèves.
          </v-card-text>
          <v-spacer></v-spacer>
          <v-card-actions class="pa-4">
            <v-btn :to="{ name: 'GeneratePosterPage' }" outlined color="primary">J'informe mes convives</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6">
        <v-card elevation="0" class="fill-height pa-4 d-flex flex-column">
          <v-img
            src="/static/images/ReadingDoodle.png"
            v-if="$vuetify.breakpoint.smAndUp"
            class="mx-auto rounded-0"
            contain
            max-height="130"
          ></v-img>
          <v-card-title class="text-h6 font-weight-bold">
            <h2 class="text-h6 font-weight-bold">Vous avez besoin d’aide pour le calcul ?</h2>
          </v-card-title>
          <v-card-text>
            Si vous ne connaissez pas votre part de bio, produits durables, produits issues du commerce équitable, nous
            vous proposons un outil simple pour les calculer. Sous forme de tableur, remplissez vos achats HT suivant
            leurs labels et/ou sigles de qualité.
          </v-card-text>
          <v-spacer></v-spacer>
          <v-card-actions class="pa-4">
            <v-dialog max-width="700" v-model="calculatorModal" @input="stopVideo">
              <template v-slot:activator="{ on, attrs }">
                <v-btn outlined color="primary" v-on="on" v-bind="attrs">
                  Télécharger notre tableur
                </v-btn>
              </template>
              <CalculatorResourceModal ref="modalContent" @closeModal="closeCalculatorModal" />
            </v-dialog>
          </v-card-actions>
        </v-card>
      </v-col>
      <v-spacer></v-spacer>
    </v-row>
  </div>
</template>

<script>
import CalculatorResourceModal from "@/components/KeyMeasureResource/CalculatorResourceModal"

export default {
  components: {
    CalculatorResourceModal,
  },
  data() {
    return {
      calculatorModal: false,
    }
  },
  methods: {
    closeCalculatorModal() {
      this.$refs.modalContent.stopVideo()
      this.calculatorModal = false
    },
    stopVideo(modalIsOpened) {
      if (!modalIsOpened) this.$refs.modalContent.stopVideo()
    },
  },
}
</script>
