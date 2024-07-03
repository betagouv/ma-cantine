<template>
  <div>
    <DownloadLink
      href="/static/documents/Convention de dons type - restauration collective.docx"
      label="Vous voulez éviter le gaspillage ? Télécharger ce modèle type de convention aux associations auxquelles faire des dons."
      sizeStr="575 Ko"
      class="mt-4"
    />
    <DownloadLink
      href="/static/documents/Guide_pratique_XP_RESERVATION.pdf"
      label="Consulter le Guide d’accompagnement – décret d’expérimentation de solution de réservation de repas en restauration collective"
      sizeStr="2,1 Mo"
      class="mt-4"
    />
  </div>
</template>

<script>
import DownloadLink from "@/components/DownloadLink"

export default {
  components: { DownloadLink },
}
</script>
