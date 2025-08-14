<script setup>
defineProps(["url", "title"])
</script>

<template>
  <section class="fr-background-alt--grey fr-my-5w fr-p-5w fr-grid-row fr-grid-row--center ma-cantine--text-center">
    <div class="fr-col-8">
      <h6>Aidez-nous à améliorer ce service !</h6>
      <slot></slot>
      <p class="fr-mb-5w ma-cantine--bold">Donnez-nous votre avis, cela ne prend que 3 minutes :</p>
      <a class="ma-cantine--unstyled-link" :href="url" target="_blank" title="Je donne mon avis - nouvelle fenêtre">
        <img src="https://jedonnemonavis.numerique.gouv.fr/static/bouton-blanc-clair.svg" alt="Je donne mon avis" />
      </a>
    </div>
  </section>
</template>
