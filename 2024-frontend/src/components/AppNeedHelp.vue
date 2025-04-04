<script setup>
import AppSeparator from "@/components/AppSeparator.vue"
defineProps(["badge", "title"])
</script>

<template>
  <section class="app-need-help fr-mt-4w fr-mt-lg-10w fr-grid-row fr-grid-row--center">
    <div class="fr-col-12 fr-col-lg-8">
      <div class="app-need-help__separator fr-mb-5w">
        <AppSeparator />
        <DsfrBadge class="app-need-help__badge" type="none" :label="badge" />
      </div>
      <div class="fr-pr-0 fr-pr-lg-8w">
        <h2>{{ title }}</h2>
        <slot />
      </div>
    </div>
  </section>
</template>

<style lang="scss">
.app-need-help {
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
