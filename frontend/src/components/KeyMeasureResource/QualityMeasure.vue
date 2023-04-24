<template>
  <div>
    <v-dialog max-width="700" v-model="calculatorModal" @input="stopVideo">
      <template v-slot:activator="{ on, attrs }">
        <v-card class="text-decoration-none text-left mt-4" hover v-on="on" v-bind="attrs">
          <DsfrCallout icon="mdi-calculator" class="text-body-2 mb-0">
            Si vous avez besoin d'aide pour calculer votre part de bios et de produits labélisés, vous pouvez tester
            notre calculateur sous format excel.
          </DsfrCallout>
        </v-card>
      </template>
      <CalculatorResourceModal ref="modalContent" @closeModal="closeCalculatorModal" />
    </v-dialog>

    <v-card
      href="https://www.inao.gouv.fr/Espace-professionnel-et-outils/Rechercher-un-produit"
      target="_blank"
      class="text-decoration-none text-left mt-4"
      hover
    >
      <DsfrCallout icon="mdi-sprout" color="#00A95F" class="text-body-2 mb-0">
        Trouver des catégories de produits en recherchant par labels, siqo et/ou régions avec le moteur de recherche de
        l'INAO.
      </DsfrCallout>
    </v-card>

    <DownloadLink
      href="/static/documents/Guide Pratique MP Gestion directe.pdf"
      label="Télécharger le guide pratique de rédaction des marchés publics pour des appros durables à destination des acteurs de la restauration collective en gestion directe."
      sizeStr="2,1 Mo"
      class="mt-4"
    />
  </div>
</template>

<script>
import CalculatorResourceModal from "@/components/KeyMeasureResource/CalculatorResourceModal"
import DsfrCallout from "@/components/DsfrCallout"
import DownloadLink from "@/components/DownloadLink"

export default {
  components: {
    CalculatorResourceModal,
    DsfrCallout,
    DownloadLink,
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
