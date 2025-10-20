<script setup>
const pictoDocuments = "/static/images/picto-dsfr/documents.svg"

const tiles = [
  {
    title: "Le guide de télédéclaration",
    download: true,
    horizontal: true,
    details: "PDF - 4,5 Mo",
    to: "static/documents/Guide_prise_en_main_ma_cantine_janv2025.pdf",
    imgSrc: pictoDocuments,
  },
  {
    title: "Comment saisir mes achats",
    to: "https://ma-cantine.crisp.help/fr/",
    horizontal: true,
    details: "Aller à la page support",
    imgSrc: pictoDocuments,
  },
  {
    title: "Inscrivez-vous à nos webinaires",
    to: { name: "CommunityPage" },
    horizontal: true,
    details: "Aller à la page ...",
    imgSrc: pictoDocuments,
  },
]
</script>
<template>
  <ul class="ma-cantine--unstyled-list ma-cantine--bg-blue fr-grid-row fr-grid-row--gutters fr-py-4w">
    <li v-for="tile in tiles" :key="tile.title" class="fr-col-4">
      <DsfrTile
        :title="tile.title"
        :to="tile.to"
        :horizontal="true"
        :details="tile.details"
        :icon="true"
        :imgSrc="tile.imgSrc"
      />
    </li>
  </ul>
</template>
