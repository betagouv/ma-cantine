<script setup>
console.log("Import cantine")
</script>

<template>
  <h1>Importer des cantines</h1>
  <p class="fr-col-12 fr-col-md-7">
    Notre outil d’import de masse vous permet de créer vos cantines ou de modifier vos cantines existantes d’un coup.
    <strong>Il concerne uniquement les gestionnaires qui ont plus de 5 cantines.</strong>
    Si vous avez moins de 5 cantines vous pouvez créer ou modifier des cantines depuis
    <router-link :to="{ name: 'NewCanteen' }">notre formulaire</router-link>
    .
  </p>
</template>
