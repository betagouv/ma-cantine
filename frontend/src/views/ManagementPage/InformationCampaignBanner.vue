<template>
  <DsfrCallout v-if="inCorrection || inTeledeclaration" noIcon class="mt-2">
    <div v-if="inTeledeclaration">
      <h2 class="fr-text font-weight-bold mb-2 mt-2">
        <span class="text-uppercase">Campagne de télédéclaration {{ currentYear }} :</span>
        du {{ teledeclarationStartDate }} au {{ teledeclarationEndDate }}
      </h2>
      <p class="mb-0">
        Dans votre espace cantine, remplissez votre bilan sur les données d'achat {{ lastYear }} et télédéclarez vos
        données.
        <br />
        Pour rappel, selon l’arrêté ministériel du 14 septembre 2022, il est obligatoire de télédéclarer ses achats.
      </p>
    </div>
    <div v-if="inCorrection">
      <h2 class="fr-text font-weight-bold mb-2 mt-2">
        <span class="text-uppercase">Droit à l'erreur :</span>
        du {{ correctionStartDate }} au {{ correctionEndDate }} {{ currentYear }}
      </h2>
      <p class="mb-0">
        Valable uniquement pour les établissements qui ont validé leur télé-déclaration. Depuis votre bilan, vous pouvez
        corriger vos informations si besoin. Attention la télé-déclaration rectificative doit être déposée avant le
        {{ correctionEndDate }}.
      </p>
    </div>
    <v-row class="mt-4 mb-0 mx-0 align-center">
      <v-btn v-if="inTeledeclaration" :to="{ name: 'PendingActions' }" color="primary" class="mb-5 mb-md-2 mr-4">
        Télédéclarer mes cantines
      </v-btn>
      <v-btn
        v-if="inTeledeclaration"
        :to="{ name: 'CommunityPage', hash: '#evenements' }"
        color="primary"
        outlined
        class="mb-5 mb-md-2 mr-4"
      >
        Inscrivez-vous à nos derniers webinaires
      </v-btn>
      <p class="fr-text-sm mb-5 mb-md-2 mr-4">
        <a
          href="https://894795896-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F-MSCF7Mdc8yfeIjMxMZr%2Fuploads%2F85J5bYm9Nd4aFRJk1pvm%2FGuide_prise_en_main_ma_cantine_janv2025.pdf?alt=media"
          target="_blank"
          rel="noopener external"
          title="Le guide de télédéclaration - ouvre une nouvelle fenêtre"
          class="grey--text text--darken-4"
        >
          Le guide de télédéclaration
          <v-icon small class="ml-2 grey--text text--darken-4">mdi-open-in-new</v-icon>
        </a>
      </p>
      <p class="fr-text-sm mb-5 mb-md-2">
        <a
          href="/static/documents/Antiseche_donnees_dachat_ma_cantine_2025.pdf"
          download
          title="Comment saisir mes données d'achat"
          class="grey--text text--darken-4"
        >
          Comment saisir mes données d'achat
          <v-icon class="ml-2 grey--text text--darken-4 icon-small">$download-line</v-icon>
        </a>
      </p>
    </v-row>
  </DsfrCallout>
</template>

<script>
import DsfrCallout from "@/components/DsfrCallout"
import { lastYear } from "@/utils"

export default {
  name: "InformationCampaignBanner",
  components: {
    DsfrCallout,
  },
  computed: {
    currentYear() {
      return this.lastYear + 1
    },
  },
  data() {
    return {
      lastYear: lastYear(),
      teledeclarationStartDate: null,
      teledeclarationEndDate: null,
      correctionStartDate: null,
      correctionEndDate: null,
      inCorrection: false,
      inTeledeclaration: false,
    }
  },
  mounted() {
    fetch(`/api/v1/campaignDates/${this.lastYear}`)
      .then((response) => response.json())
      .then((response) => this.updateBanner(response))
  },
  methods: {
    updateBanner(infos) {
      this.inCorrection = infos.inCorrection
      this.inTeledeclaration = infos.inTeledeclaration
      this.correctionStartDate = this.prettifyDate(infos.correctionStartDate)
      this.correctionEndDate = this.prettifyDate(infos.correctionEndDate)
      this.teledeclarationStartDate = this.prettifyDate(infos.teledeclarationStartDate)
      this.teledeclarationEndDate = this.prettifyDate(infos.teledeclarationEndDate)
    },
    prettifyDate(date) {
      const dateObject = new Date(date)
      const day = dateObject.getDate()
      const monthName = dateObject.toLocaleString("default", { month: "long" })
      return `${day} ${monthName}`
    },
  },
}
</script>

<style scoped>
.v-sheet--shaped {
  border-radius: 26px 4px !important;
}

.icon-small {
  width: 1rem;
}
</style>
