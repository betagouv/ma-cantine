<script setup></script>

<template>
  <div>
    <p class="fr-mb-0">Mon établissement</p>
    <p class="fr-hint-text">
      Nous utilisons le site
      <a href="https://annuaire-entreprises.data.gouv.fr/" target="_blank">annuaire-des-entreprises</a>
      afin de retrouver les informations votre établissement
    </p>
    <DsfrSearchBar placeholder="Tapez votre n° SIRET" button-text="Rechercher" :large="true" />
  </div>
</template>
