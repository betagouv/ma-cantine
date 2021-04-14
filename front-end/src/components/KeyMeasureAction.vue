<template>
  <div class="action">
    <i class="fas" :class="isDone ? 'fa-check' : 'fa-times'" :title="isDone ? 'fait' : 'pas fait'"></i>
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

    .fa-check, .fa-times {
      height: 30px;
      width: 30px;
    }

    .fa-check {
      color: $green;
    }

    .fa-times {
      color: $red;
    }
  }
</style>
