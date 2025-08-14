<script setup>
defineProps(["url", "title"])
</script>

<template>
  <section class="fr-card fr-my-5w fr-p-5w">
    <div class="fr-grid-row fr-grid-row--gutters fr-grid-row--middle">
      <div class="fr-col-12 fr-col-md-6">
        <h6 class="fr-mb-1w">{{ title }}</h6>
        <p class="fr-mb-0">Donnez-nous votre avis, cela ne prend que 2 minutes.</p>
      </div>
      <div class="fr-col-12 fr-col-md-6 fr-mt-2w fr-mt-md-0 fr-grid-row fr-grid-row--center">
        <a class="ma-cantine--unstyled-link" :href="url" target="_blank" title="Je donne mon avis - nouvelle fenêtre">
          <img src="https://jedonnemonavis.numerique.gouv.fr/static/bouton-bleu-clair.svg" alt="Je donne mon avis" />
        </a>
      </div>
    </div>
  </section>
</template>
