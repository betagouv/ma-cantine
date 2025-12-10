<script setup>
const pictoCrispTeledeclaration = "/static/images/picto-dsfr/crisp-teledeclaration.svg"
const pictoCrispBienDemarrer = "/static/images/picto-dsfr/crisp-bien-demarrer.svg"
const pictoSelfTraining = "/static/images/picto-dsfr/self-training.svg"

const tiles = [
{
    title: "Bien démarrer",
    to: "https://ma-cantine.crisp.help/fr/category/bien-demarrer-1fn9r2h/",
    horizontal: true,
    details: "Découverte de la plateforme : inscription, configuration et premières actions.",
    imgSrc: pictoCrispBienDemarrer,
  },
  {
    title: "Télédéclaration",
    horizontal: true,
    details: "Déclarer vos achats et à suivre vos indicateurs EGalim.",
    to: "https://ma-cantine.crisp.help/fr/category/teledeclaration-18r0z84/",
    imgSrc: pictoCrispTeledeclaration,
  },
  {
    title: "Inscrivez-vous à nos webinaires",
    to: { name: "CommunityPage" },
    horizontal: true,
    details: "Loi EGalim, utilisation de la plateforme...",
    imgSrc: pictoSelfTraining,
  },
]
</script>
<template>
  <ul class="ma-cantine--unstyled-list fr-grid-row fr-grid-row--gutters">
    <li v-for="tile in tiles" :key="tile.title" class="fr-col-12 fr-col-md-4">
      <DsfrTile
        class="gestionnaire-guides__tiles"
        title-tag="h2"
        :title="tile.title"
        :to="tile.to"
        :horizontal="true"
        :details="tile.details"
        :icon="true"
        :imgSrc="tile.imgSrc"
        :download="tile.download"
      />
    </li>
  </ul>
</template>

<style lang="scss">
.gestionnaire-guides__tiles {
  .fr-artwork {
    max-width: 100% !important;
  }
}
</style>
