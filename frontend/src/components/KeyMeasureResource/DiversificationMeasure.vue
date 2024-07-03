<template>
  <div>
    <DownloadLink
      href="/static/documents/Guide CNRC Expérimentation du Menu Végétarien Restauration Scolaire.pdf"
      label="Télécharger un guide sur le menu végétarien hebdomadaire en restauration scolaire"
      sizeStr="2,1 Mo"
      class="mt-4"
    />
    <DownloadLink
      href="/static/documents/Livret de Recettes Végétariennes.pdf"
      label="Télécharger un livret de recettes pour menus végétariens"
      sizeStr="8,9 Mo"
      class="mt-4"
    />
    <DownloadLink
      href="/static/documents/Cadre Général CNRC Plan pluriannuel de diversification des sources de protéines.pdf"
      label="Télécharger le cadre général du plan pluriannuel de diversification des sources de protéines"
      sizeStr="5,6 Mo"
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
