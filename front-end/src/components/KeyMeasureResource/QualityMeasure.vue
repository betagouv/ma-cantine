<template>
  <div>
    <a href="/Diagnostic approvisionnement (ma-cantine-alpha) v0.3.ods" class="resource calculator" download>
      <div class="resource-icon"><i class="fas fa-calculator"></i></div>
      <p class="resource-prompt">
        Si vous avez besoin d'aide pour calculer votre part de bios et de produits labélisés,
        vous pouvez tester notre calculateur sous format excel.
      </p>
      <div class="resource-icon"><i class="fas fa-file-download"></i></div>
    </a>
    <a href="https://www.inao.gouv.fr/Espace-professionnel-et-outils/Rechercher-un-produit" class="resource" target="_blank">
      <div class="resource-icon"><i class="fas fa-seedling"></i></div>
      <p class="resource-prompt">
        Trouver des catégories de produits en recherchant par labels, siqo et/ou régions
        avec le moteur de recherche de l'INAO.
      </p>
      <div class="resource-icon"><i class="fas fa-external-link-alt"></i></div>
    </a>
    <a href="/Guide Pratique MP Gestion directe.pdf" class="resource" download>
      <div class="resource-icon"><i class="fas fa-archive"></i></div>
      <p class="resource-prompt">
        Télécharger le guide pratique de rédaction des marchés publics pour des appros
        durables à destination des acteurs la restauration collective en gestion directe.
      </p>
      <div class="resource-icon"><i class="fas fa-file-download"></i></div>
    </a>
  </div>
</template>

<style scoped lang="scss">
  .resource.calculator {
    background: $light-blue;
    border-color: $blue;

    .fa-calculator {
      color: $blue;
    }

    .fa-file-download {
      color: $blue;
    }

    .resource-prompt {
      color: $blue;
    }
  }
</style>
