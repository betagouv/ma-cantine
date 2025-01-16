<script setup>
import AppLinkMailto from "@/components/AppLinkMailto.vue"
import AppSeparator from "@/components/AppSeparator.vue"
</script>

<template>
  <section class="fr-grid-row fr-grid-row--center">
    <div class="fr-col-8">
      <div class="import-help-center-separator fr-mb-5w">
        <AppSeparator />
        <DsfrBadge class="import-help-center-separator__badge" type="none" label="Besoin d'aide ?" />
      </div>
      <h2>Vous n’arrivez pas à importer votre fichier ?</h2>
      <p class="fr-pr-12w">
        Si votre fichier comptable agrégé ne ressemble pas du tout à ça, vous pouvez nous l'envoyer à l'adresse
        <AppLinkMailto />
      </p>
    </div>
  </section>
</template>

<style lang="scss">
.import-help-center-separator {
  position: relative;

  &__badge {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
  }
}
</style>
