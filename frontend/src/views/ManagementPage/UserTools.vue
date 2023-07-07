<template>
  <div>
    <v-row>
      <v-col cols="12" sm="6" height="100%">
        <v-card outlined class="d-flex flex-column fill-height pa-2">
          <v-card-title class="font-weight-bold">Tableur d'aide pour le calcul</v-card-title>
          <v-card-text>
            Si vous ne connaissez pas votre part de bio, produits durables, produits issus du commerce équitable, nous
            vous proposons un outil simple pour les calculer. Sous forme de tableur, remplissez vos achats HT suivant
            leurs labels et/ou sigles de qualité.
            <br />
            Merci à nos beta-testeurs et notamment au PETR Pays d’Armagnac qui nous ont inspiré ce tableur.
          </v-card-text>
          <v-spacer></v-spacer>
          <v-card-actions class="px-4">
            <v-spacer></v-spacer>
            <v-dialog max-width="700" v-model="calculatorModal">
              <template v-slot:activator="{ on, attrs }">
                <v-btn outlined color="primary" v-on="on" v-bind="attrs">
                  Télécharger le tableur
                </v-btn>
              </template>
              <CalculatorResourceModal @closeModal="closeCalculatorModal" />
            </v-dialog>
          </v-card-actions>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" height="100%">
        <v-card outlined class="d-flex flex-column fill-height pa-2">
          <v-card-title class="font-weight-bold">Suivi d'achats</v-card-title>
          <v-card-text>
            Une alimentation saine et durable commence par un suivi comptable de vos achats. Rentrez et suivez vos
            achats pour faciliter la télédéclaration annuelle.
          </v-card-text>
          <v-spacer></v-spacer>
          <v-card-actions class="px-4">
            <v-spacer></v-spacer>
            <v-btn :to="{ name: 'PurchasesHome' }" outlined color="primary">
              Gérer mes achats
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" sm="6" height="100%">
        <v-card outlined class="d-flex flex-column fill-height pa-2">
          <v-card-title class="font-weight-bold">Trouver des acteurs de l'éco-système pour vos besoins</v-card-title>
          <v-card-text>
            Rechercher des acteurs de l'éco-système qui pourraient vous aidez à améliorer votre offre selon vos besoins.
          </v-card-text>
          <v-spacer></v-spacer>
          <v-card-actions class="px-4">
            <v-spacer></v-spacer>
            <v-btn :to="{ name: 'PartnersHome' }" outlined color="primary">Trouver des acteurs</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" height="100%">
        <v-card outlined class="d-flex flex-column fill-height pa-2">
          <v-card-title class="font-weight-bold">Générateur d'affiches</v-card-title>
          <v-card-text>
            Vous pouvez générer une affiche à poser dans votre cantine ainsi qu’un email-type à destination des convives
            et parents d'élèves.
          </v-card-text>
          <v-spacer></v-spacer>
          <v-card-actions class="px-4">
            <v-spacer></v-spacer>
            <v-btn :to="{ name: 'GeneratePosterPage' }" outlined color="primary">J'informe mes convives</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" sm="6" height="100%">
        <v-card outlined class="d-flex flex-column fill-height pa-2">
          <v-card-title class="font-weight-bold">Blog</v-card-title>
          <v-card-text>
            Découvrez notre espace blog et témoignages
          </v-card-text>
          <v-spacer></v-spacer>
          <v-card-actions class="px-4">
            <v-spacer></v-spacer>
            <v-btn :to="{ name: 'BlogsHome' }" outlined color="primary">Lire notre blog</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" height="100%">
        <v-card outlined class="d-flex flex-column fill-height pa-2">
          <v-card-title class="font-weight-bold">Documentation</v-card-title>
          <v-card-text>
            Ressources pour les acteurs et actrices de la restauration collective
          </v-card-text>
          <v-spacer></v-spacer>
          <v-card-actions class="px-4">
            <v-spacer></v-spacer>
            <v-btn
              href="https://ma-cantine-1.gitbook.io/ma-cantine-egalim/"
              target="_blank"
              outlined
              color="primary"
              rel="noopener"
            >
              Decouvrir nos ressources
              <v-icon small class="ml-2">mdi-open-in-new</v-icon>
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import CalculatorResourceModal from "@/components/KeyMeasureResource/CalculatorResourceModal"

export default {
  components: { CalculatorResourceModal },
  props: {
    canteenCount: Boolean,
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
