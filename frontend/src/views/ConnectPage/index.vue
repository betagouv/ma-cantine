<template>
  <div id="connect">
    <router-view :key="$route.fullPath" />

    <p id="help">
      Vous avez besoin d'aide ? Contactez nous par email :
      <a href="mailto:contact@egalim.beta.gouv.fr">contact@egalim.beta.gouv.fr</a>
    </p>
  </div>
</template>

<style scoped lang="scss">
#connect {
  padding: 3em;

  ::v-deep(h1) {
    font-weight: bold;
    font-size: 48px;
    color: $ma-cantine-green;
  }

  ::v-deep(.container) {
    background-color: $ma-cantine-light-yellow;
    border: dotted 1px $ma-cantine-yellow;
    border-radius: 4px;
    margin: auto;
    padding: 3em;
    display: flex;
    flex-direction: column;
    max-width: 35em;
  }

  ::v-deep(form) {
    label {
      text-align: left;
      margin-top: 15px;
    }

    input,
    select {
      margin-top: 10px;
      border: none;
      font-size: 1.2em;
      padding: 5px;
      border: 1px solid $ma-cantine-yellow;
      border-radius: 4px;
    }
  }

  ::v-deep(.action) {
    margin: auto;
    margin-top: 2em;
    width: 50%;
    min-width: 9em;
    border-radius: 1em;
    padding: 0.5em;
    font-weight: bold;
    cursor: pointer;
    border: 2px solid $ma-cantine-orange;
    color: $ma-cantine-orange;
    text-decoration: none;
  }

  ::v-deep(.primary.action) {
    background: $ma-cantine-orange;
    color: $ma-cantine-white;
  }

  ::v-deep(.secondary.action) {
    background-color: $ma-cantine-white;
    font-size: 1em;
  }

  ::v-deep(#alt-choice) {
    margin: 3em auto;

    p {
      margin: 0;
      font-size: 1.2em;
    }
  }

  #help {
    margin-top: 3em;
  }
}
</style>
