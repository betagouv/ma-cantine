<template>
  <div class="fr-highlight fr-text ml-8 pl-9">
    <slot />
  </div>
</template>

<script>
export default {
  name: "DsfrHighlight",
}
</script>

<style scoped>
.fr-highlight {
  background-image: linear-gradient(0deg, #6a6af4, #6a6af4);
  background-position: 0 0;
  background-repeat: no-repeat;
  background-size: 0.25rem 100%;
  font-size: 1rem;
  line-height: 1.5rem;

  color: #3a3a3a;
}
</style>
