<template>
  <div>
    <v-dialog max-width="700" v-model="calculatorModal">
      <template v-slot:activator="{ on, attrs }">
        <v-card class="text-decoration-none text-left mt-4" hover v-on="on" v-bind="attrs">
          <v-alert
            icon="mdi-calculator"
            class="text-body-2 mb-0"
            color="#3F62D5"
            prominent
            colored-border
            border="left"
          >
            Si vous avez besoin d'aide pour calculer votre part de bios et de produits labélisés, vous pouvez tester
            notre calculateur sous format excel.
          </v-alert>
        </v-card>
      </template>
      <CalculatorResourceModal @closeModal="closeCalculatorModal" />
    </v-dialog>

    <v-card
      href="https://www.inao.gouv.fr/Espace-professionnel-et-outils/Rechercher-un-produit"
      target="_blank"
      class="text-decoration-none text-left mt-4"
      hover
    >
      <v-alert icon="mdi-sprout" class="text-body-2 mb-0" color="primary" prominent colored-border border="left">
        Trouver des catégories de produits en recherchant par labels, siqo et/ou régions avec le moteur de recherche de
        l'INAO.
      </v-alert>
    </v-card>

    <v-card
      href="/static/documents/Guide Pratique MP Gestion directe.pdf"
      target="_blank"
      class="text-decoration-none text-left mt-4"
      hover
    >
      <v-alert icon="mdi-archive" class="text-body-2 mb-0" color="primary" prominent colored-border border="left">
        Télécharger le guide pratique de rédaction des marchés publics pour des appros durables à destination des
        acteurs de la restauration collective en gestion directe.
      </v-alert>
    </v-card>
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
      this.calculatorModal = false
    },
  },
}
</script>
