<script setup>
import AppSeparator from "@/components/AppSeparator.vue"
</script>

<template>
  <section class="import-help fr-mt-8w fr-grid-row fr-grid-row--center">
    <div class="fr-col-12 fr-col-md-8">
      <div class="import-help__separator fr-mb-5w">
        <AppSeparator />
        <DsfrBadge class="import-help__badge" type="none" label="Besoin d'aide ?" />
      </div>
      <h2>Vous n’arrivez pas à importer votre fichier</h2>
      <p class="fr-pr-0 fr-pr-md-8w">
        Si vous avez des questions ou des problèmes pour importer votre fichier, vous pouvez
        <a
          href="https://ma-cantine.crisp.help/fr/"
          target="_blank"
        >
          consulter nos ressources
        </a>
      </p>
    </div>
  </section>
</template>

<style lang="scss">
.import-help {
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
