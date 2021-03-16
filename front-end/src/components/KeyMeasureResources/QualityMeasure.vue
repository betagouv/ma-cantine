<template>
  <div>
    <a href="Diagnostic approvisionnement (ma-cantine-alpha) v0.2.ods" class="resource calculator" download>
      <div class="link-icon"><i class="fas fa-calculator"></i></div>
      <p>
        Si vous avez besoin d'aide pour calculer votre part de bios et de produits labélisés,
        vous pouvez tester notre calculateur sous format excel.
      </p>
      <div class="link-icon"><i class="fas fa-file-download"></i></div>
    </a>
    <a href="https://www.inao.gouv.fr/Espace-professionnel-et-outils/Rechercher-un-produit" class="resource" target="_blank">
      <div class="link-icon"><i class="fas fa-seedling"></i></div>
      <p>
        Trouver des catégories de produits en recherchant par labels, siqo et/ou régions
        avec le moteur de recherche de l'INAO.
      </p>
      <div class="link-icon"><i class="fas fa-external-link-alt"></i></div>
    </a>
  </div>
</template>

<style scoped lang="scss">
  @import '@/styles/key-measure-resource.scss';

  .resource.calculator {
    background: $light-blue;
    border-color: $blue;

    .fa-calculator {
      color: $blue;
    }

    .fa-file-download {
      color: $blue;
    }

    p {
      color: $blue;
    }
  }
</style>