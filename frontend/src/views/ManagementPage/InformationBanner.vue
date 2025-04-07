<template>
  <DsfrCallout noIcon class="mt-2">
    <div v-if="isCorrection">
      <h2 class="fr-text font-weight-bold mb-2 mt-2">
        <span class="text-uppercase">Droit à l'erreur :</span>
        du {{ correctionStartDate }} au {{ correctionEndDate }} {{ year + 1 }}
      </h2>
      <p class="mb-0">
        Valable uniquement pour les établissements qui ont validé leur télé-déclaration. Depuis votre bilan, vous pouvez
        corriger vos informations si besoin. Attention la télé-déclaration rectificative doit être déposée avant le
        {{ correctionEndDate }}.
      </p>
    </div>
    <v-row class="mt-4 mb-0 mx-0 align-center">
      <v-btn v-if="isTeledeclaration" :to="{ name: 'PendingActions' }" color="primary" class="mb-5 mb-md-2 mr-4">
        Télédéclarer mes cantines
      </v-btn>
      <v-btn
        v-if="isTeledeclaration"
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
  name: "InformationBanner",
  components: {
    DsfrCallout,
  },
  data() {
    return {
      year: lastYear(),
      correctionStartDate: null,
      correctionEndDate: null,
      isCorrection: false,
    }
  },
  mounted() {
    // TODO : change for api
    this.updateBanner({
      isCorrection: true,
      isTeledeclaration: false,
      correctionEndDate: "2025-04-30 00:00:00+01:00",
      correctionStartDate: "2025-04-16 00:00:00+01:00",
    })
  },
  methods: {
    updateBanner(infos) {
      this.isCorrection = infos.isCorrection
      this.isTeledeclaration = infos.isTeledeclaration
      this.correctionStartDate = this.prettifyDate(infos.correctionStartDate)
      this.correctionEndDate = this.prettifyDate(infos.correctionEndDate)
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
