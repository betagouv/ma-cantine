<template>
  <p class="action my-0">
    <v-icon v-if="isDone" color="primary" aria-label="Fait" role="img" aria-hidden="false" class="pl-0">
      $check-line
    </v-icon>
    <v-icon v-else aria-label="Pas encore fait" role="img" aria-hidden="false" class="pl-0">$close-line</v-icon>
    <span>{{ label }}</span>
  </p>
</template>

<script>
export default {
  props: {
    isDone: Boolean,
    label: String,
  },
}
</script>

<style scoped lang="scss">
.action {
  padding: 10px;
  display: flex;
  align-items: center;
  text-align: left;

  span {
    padding-left: 10px;
    max-width: 90%;
  }
}
</style>
