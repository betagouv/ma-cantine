<template>
  <div id="connect">
    <router-view :key="$route.fullPath" :loginUrl="loginUrl" :post="post"/>

    <p id="help">
      Vous avez besoin d'aide ? Contactez nous par email : 
      <a href="mailto:contact@egalim.beta.gouv.fr">contact@egalim.beta.gouv.fr</a>
    </p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      loginUrl: `${process.env.VUE_APP_SITE_URL || "http://localhost:8080"}/connecter?token=`,
    }
  },
  methods: {
    post(apiUrl, url, json) {
      return fetch(`${apiUrl}/${url}`, {
        method: "POST",
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(json)
      });
    }
  }
}
</script>

<style scoped lang="scss">
  #connect {
    padding: 3em;

    :deep(h1) {
      font-weight: bold;
      font-size: 48px;
      color: $green;
    }

    :deep(.container) {
      background-color: $light-yellow;
      border: dotted 1px $yellow;
      border-radius: 4px;
      margin: auto;
      padding: 3em;
      display: flex;
      flex-direction: column;
      max-width: 35em;
    }

    :deep(form) {
      label {
        text-align: left;
        margin-top: 15px;
      }

      input, select {
        margin-top: 10px;
        border: none;
        font-size: 1.2em;
        padding: 5px;
        border: 1px solid $yellow;
        border-radius: 4px;
      }
    }

    :deep(.action) {
      margin: auto;
      margin-top: 2em;
      width: 50%;
      min-width: 9em;
      border-radius: 1em;
      padding: 0.5em;
      font-weight: bold;
      cursor: pointer;
      border: 2px solid $orange;
      color: $orange;
      text-decoration: none;
    }

    :deep(.primary.action) {
      background: $orange;
      color: $white;
    }

    :deep(.secondary.action) {
      background-color: $white;
      font-size: 1em;
    }

    :deep(#alt-choice) {
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
