<script setup>
const props = defineProps(['filePreviews'])
const fileSuccessPath = `/static/documents/${props.filePreviews.success}`
const fileErrorPath = `/static/documents/${props.filePreviews.error}`
</script>

<template>
  <ul class="ma-cantine--unstyled-list import-files-example">
    <li class="import-files-example__bloc fr-mt-2w">
      <DsfrBadge class="import-files-example__badge" type="error" label="Automatiquement rejeté" />
      <div class="import-files-example__image-container import-files-example__image-container--error">
        <img class="import-files-example__image" :src="fileErrorPath" alt="Exemple de fichier automatiquement rejeté" />
      </div>
    </li>
    <li class="import-files-example__bloc fr-mt-2w">
      <DsfrBadge class="import-files-example__badge" type="success" label="accepté" />
      <div class="import-files-example__image-container import-files-example__image-container--success">
        <img class="import-files-example__image" :src="fileSuccessPath"  alt="Exemple de fichier automatiquement rejeté" />
      </div>
    </li>
  </ul>
</template>

<style lang="scss">
.import-files-example {

  &__bloc {
    padding-top: 0.5rem;
    overflow: hidden;
    position: relative;
  }

  &__image-container {
    width: 100%;
    overflow-x: scroll;
    height: 15rem;
    border-style: solid;
    border-width: 0.5rem;

    &--error {
      border-color: var(--background-contrast-error);
    }

    &--success {
      border-color: var(--background-contrast-success);
    }
  }

  &__image {
    width: auto;
    height: calc(100% - 0.5rem);
  }

  &__badge {
    position: absolute;
    top: 0;
    left: 0;
  }
}
</style>
