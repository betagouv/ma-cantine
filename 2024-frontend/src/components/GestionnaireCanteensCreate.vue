<script setup>
const pictoDocuments = "/static/images/picto-dsfr/documents.svg"
const pictoDocumentAdd = "/static/images/picto-dsfr/document-add.svg"
</script>

<template>
  <ul class="ma-cantine--unstyled-list fr-grid-row fr-grid-row--gutters fr-my-4w">
    <li class="fr-col-12 fr-col-md-6">
      <DsfrCard
        class="gestionnaire-tableau-de-bord__card"
        title="Ajouter une cantine via le formulaire"
        :imgSrc="pictoDocuments"
        :link="{ name: 'GestionnaireCantineAjouter' }"
        endDetail="Ajouter votre cantine"
        description="Pour ajouter votre lieu de restauration collective munissez-vous de votre numéro SIRET ou du numéro SIREN de votre unité légale."
      />
    </li>
    <li class="fr-col-12 fr-col-md-6">
      <DsfrCard
        class="gestionnaire-tableau-de-bord__card"
        title="Créer plus de 5 cantines via import de fichier"
        :imgSrc="pictoDocumentAdd"
        :link="{ name: 'GestionnaireImportCantines' }"
        endDetail="Importer toutes vos cantines"
        description="Notre outil d’import de masse vous permet de créer vos cantines ou de modifier vos cantines existantes d’un coup. Il concerne uniquement les gestionnaires qui ont plus de 5 cantines."
      />
    </li>
  </ul>
</template>
