<template>
  <div>
    <v-card
      href="/static/documents/Convention de dons type - restauration collective.docx"
      target="_blank"
      class="text-decoration-none text-left mt-4"
      hover
    >
      <DsfrCallout icon="mdi-file-download-outline" class="text-body-2 mb-0">
        Vous voulez éviter le gaspillage ? Télécharger ce modèle type de convention aux associations auxquelles faire
        des dons.
      </DsfrCallout>
    </v-card>
    <v-card
      href="/static/documents/Guide_pratique_XP_RESERVATION.pdf"
      target="_blank"
      class="text-decoration-none text-left mt-4"
      hover
    >
      <DsfrCallout icon="mdi-file-download-outline" class="text-body-2 mb-0">
        Consulter le Guide d’accompagnement – décret d’expérimentation de solution de réservation de repas en
        restauration collective
      </DsfrCallout>
    </v-card>
  </div>
</template>

<script>
import DsfrCallout from "@/components/DsfrCallout"

export default {
  components: { DsfrCallout },
}
</script>
