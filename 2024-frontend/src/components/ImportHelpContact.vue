<script setup>
import AppLinkMailto from "@/components/AppLinkMailto.vue"
import AppSeparator from "@/components/AppSeparator.vue"
</script>

<template>
  <section class="import-help-contact fr-grid-row fr-grid-row--center">
    <div class="fr-col-12 fr-col-md-8">
      <div class="import-help-contact__separator fr-mb-5w">
        <AppSeparator />
        <DsfrBadge class="import-help-contact__badge" type="none" label="Besoin d'aide ?" />
      </div>
      <h2>Vous n’arrivez pas à importer votre fichier</h2>
      <p class="fr-pr-0 fr-pr-md-8w">
        Si vous avez des questions ou des problèmes, si votre fichier comptable agrégé ne ressemble pas du tout à ça,
        vous pouvez nous l'envoyer à l'adresse
        <AppLinkMailto />
      </p>
    </div>
  </section>
</template>

<style lang="scss">
.import-help-contact {
  &__separator {
    position: relative;
  }

  &__badge {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
  }
}
</style>
