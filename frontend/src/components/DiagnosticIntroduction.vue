<template>
  <p>
    Vous pouvez créer des diagnostics par année pour decouvrir les atouts ainsi que les points d'amélioration de votre
    cantine en relation avec les mesures de la loi EGAlim. Après creation, vos diagnostics vous permettront à publier
    vos données en répondant
    <router-link
      :to="{ name: 'KeyMeasurePage', params: { id: 'information-des-usagers' } }"
      class="text-decoration-underline primary--text"
    >
      la mesure d'information
    </router-link>
    .
  </p>
</template>
