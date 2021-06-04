<template>
  <div class="action">
    <v-icon small v-if="isDone" color="light-green darken-4" aria-label="Fait" aria-hidden="false">
      mdi-check-bold
    </v-icon>
    <v-icon small v-else aria-label="Pas encore fait" aria-hidden="false">mdi-close</v-icon>
    <span>{{ label }}</span>
  </div>
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
