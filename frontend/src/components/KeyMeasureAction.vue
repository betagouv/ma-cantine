<template>
  <div class="action">
    <v-icon small v-if="isDone" color="secodary">mdi-check-bold</v-icon>
    <v-icon small v-else>mdi-close</v-icon>
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

  .fa-check,
  .fa-times {
    height: 30px;
    width: 30px;
  }

  .fa-check {
    color: $ma-cantine-green;
  }

  .fa-times {
    color: $ma-cantine-red;
  }
}
</style>
