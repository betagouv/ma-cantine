<template>
  <li class="statistic">
    <div class="vertically-align-header">
      <h3>{{ title }}</h3>
    </div>
    <p class="number">{{ value }} %</p>
  </li>
</template>

<script>
  export default {
    props: {
      title: String,
      value: Number
    }
  }
</script>

<style scoped lang="scss">
  .statistic {
    width: 30%;
    text-align: center;
  }

  .vertically-align-header {
    height: 5em;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  h3 {
    font-size: 1em;
    font-weight: normal;
  }

  .number {
    font-size: 2.5em;
    margin-top: 0.2em;
  }

  .bio > .number {
    color: $green;
  }

  .sustainable > .number {
    color: $orange;
  }

  @media (max-width: 850px) {
    .number {
      margin: 0;
      margin-bottom: 0.7em;
      font-size: 2em;
    }
  }
</style>