<script setup>
defineProps(["question"])
</script>

<template>
  <div class="help-block fr-pl-4w fr-py-1w fr-my-2w">
    <p v-if="question" class="fr-mb-1w question">
      <span class="fr-icon-question-fill fr-icon--sm fr-mr-1v"></span>
      {{ question }}
    </p>
    <slot />
  </div>
</template>

<style scoped>
.help-block {
  border-left: solid 4px var(--info-425-625);
}
.question {
  font-weight: bold;
}
</style>
