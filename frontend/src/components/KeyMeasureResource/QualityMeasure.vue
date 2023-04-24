<template>
  <div>
    <v-dialog max-width="700" v-model="calculatorModal" @input="stopVideo">
      <template v-slot:activator="{ on, attrs }">
        <p class="mt-4 body-1">
          Si vous avez besoin d'aide pour calculer votre part de bios et de produits labélisés, vous pouvez
          <a href="#" v-on="on" v-bind="attrs">tester notre calculateur sous format excel</a>
        </p>
      </template>
      <CalculatorResourceModal ref="modalContent" @closeModal="closeCalculatorModal" />
    </v-dialog>

    <p class="mt-4 body-1">
      Trouver des catégories de produits en recherchant par labels, SIQO et/ou régions avec
      <a
        href="https://www.inao.gouv.fr/Espace-professionnel-et-outils/Rechercher-un-produit"
        target="_blank"
        rel="noopener"
      >
        le moteur de recherche de l'INAO
        <v-icon color="primary" small>mdi-open-in-new</v-icon>
      </a>
    </p>

    <DownloadLink
      href="/static/documents/Guide Pratique MP Gestion directe.pdf"
      label="Télécharger le guide pratique CNRC de rédaction des marchés publics pour des appros durables à destination des acteurs de la restauration collective en gestion directe"
      sizeStr="2,4 Mo"
      class="mt-4"
    />

    <DownloadLink
      href="/static/documents/Guide Pratique pour des Prestations Intégrant des Produits Durables et de Qualité.pdf"
      label="Télécharger le guide pratique CNRC à destination des acteurs de la restauration collective en prestation de service"
      sizeStr="2,2 Mo"
      class="mt-4"
    />
  </div>
</template>

<script>
import CalculatorResourceModal from "@/components/KeyMeasureResource/CalculatorResourceModal"
import DownloadLink from "@/components/DownloadLink"

export default {
  components: {
    CalculatorResourceModal,
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
