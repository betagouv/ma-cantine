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

    <v-card
      href="/static/documents/Guide Pratique MP Gestion directe.pdf"
      target="_blank"
      class="text-decoration-none text-left mt-4"
      hover
    >
      <DsfrCallout icon="mdi-file-download-outline" class="text-body-2 mb-0" color="#C08C65">
        Télécharger le guide pratique de rédaction des marchés publics pour des appros durables à destination des
        acteurs de la restauration collective en gestion directe.
      </DsfrCallout>
    </v-card>

    <v-card
      href="https://ma-cantine-1.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F-MSCF7Mdc8yfeIjMxMZr%2Fuploads%2FnKCl4FRksM2ovwTi7ORw%2FCNRC%20Guide%20acheteurs%20prestation%20service%2011%202021.pdf?alt=media"
      target="_blank"
      class="text-decoration-none text-left mt-4"
      hover
    >
      <DsfrCallout icon="mdi-file-download-outline" color="#C08C65" class="text-body-2 mb-0">
        Télécharger le guide pratique à destination des acteurs de la restauration collective en prestation de service.
      </DsfrCallout>
    </v-card>
  </div>
</template>

<script>
import CalculatorResourceModal from "@/components/KeyMeasureResource/CalculatorResourceModal"
import DsfrCallout from "@/components/DsfrCallout"

export default {
  components: {
    CalculatorResourceModal,
    DsfrCallout,
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
