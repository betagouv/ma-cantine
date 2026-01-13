<template>
  <ul class="gestionnaire-empty-canteen ma-cantine--unstyled-list fr-grid-row fr-grid-row--gutters fr-my-4w">
    <li class="fr-col-12 fr-col-md-4">
      <DsfrCard
        class="gestionnaire-empty-canteen__card"
        title="Ajouter une cantine via le formulaire"
        :link="{ name: 'GestionnaireCantineRestaurantAjouter' }"
        endDetail="Ajouter votre cantine"
        description="Pour ajouter votre lieu de restauration collective munissez-vous de votre numéro SIRET ou du numéro SIREN de votre unité légale."
      />
    </li>
    <li class="fr-col-12 fr-col-md-4">
      <DsfrCard
        class="gestionnaire-empty-canteen__card"
        title="Ajouter un groupe de restaurants satellites"
        :link="{ name: 'GestionnaireCantineGroupeAjouter' }"
        endDetail="Ajouter votre groupe"
        description="Les groupes de restaurants satellites vous permettent de gérer plusieurs cantines ensemble et réaliser une déclaration unique."
      />
    </li>
    <li class="fr-col-12 fr-col-md-4">
      <DsfrCard
        class="gestionnaire-empty-canteen__card"
        title="Créer plus de 5 cantines via import de fichier"
        :link="{ name: 'GestionnaireImportCantines' }"
        endDetail="Importer toutes vos cantines"
        description="Notre outil d’import de masse vous permet de créer vos cantines ou de modifier vos cantines existantes d’un coup. Il concerne uniquement les gestionnaires qui ont plus de 5 cantines."
      />
    </li>
  </ul>
</template>

<style lang="scss">
.gestionnaire-empty-canteen {
  &__card {
    .fr-card__header {
      padding-top: 1rem !important;
    }

    .fr-card__img img {
      max-height: 7rem !important;
      object-fit: contain !important;
    }
  }
}
</style>
