<template>
  <div class="fr-skiplinks">
    <nav class="fr-container" role="navigation" aria-label="Accès rapide">
      <ul class="fr-skiplinks__list no-bullets px-2">
        <li>
          <a class="fr-link mr-2" href="#contenu">Contenu</a>
        </li>
        <li>
          <a class="fr-link mr-2" href="#pied-de-page">Pied de page</a>
        </li>
      </ul>
    </nav>
  </div>
</template>

<script>
export default {
  name: "SkipLinks",
}
</script>

<style lang="scss" scoped>
.fr-skiplinks {
  top: 0;
  left: 0;
  position: absolute;
  padding: 1rem 0;
  background-color: #ddd;
  width: 100%;
  z-index: 1;
}

// focus-within not currently supported by IE but I think skiplinks are mostly helpful for people
// using screenreaders, which will read out the link whether or not it is visible on screen.
.fr-skiplinks:focus-within {
  z-index: 7;
}

.fr-skiplinks__list {
  display: flex;
}
</style>
