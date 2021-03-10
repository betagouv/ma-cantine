<template>
  <fieldset class="form-communication-support">
    <legend>Quel(s) support(s) de communication utilisez vous ?</legend>

    <div class="form-group">
      <div class="form-item">
        <input id="email" value="email" v-model="diagnostic.communicationSupport" type="checkbox" >
        <label for="email">Envoi d’e-mail aux convives</label>
      </div>

      <div class="form-item">
        <input id="display" value="display" v-model="diagnostic.communicationSupport" type="checkbox" >
        <label for="display">Par affichage sur le lieu de restauration</label>
      </div>

      <div class="form-item">
        <input id="website" value="website" v-model="diagnostic.communicationSupport" type="checkbox" >
        <label for="website">Sur site internet (mairie, cantine)</label>
      </div>

      <div class="form-item">
        <input id="other" value="other" v-model="diagnostic.communicationSupport" type="checkbox" >
        <label for="other">Autre(s)</label>
      </div>
    </div>
  </fieldset>

  <div class="form-item">
    <label for="communication-link" class="form-label">Lien vers le support de communication</label>
    <input id="communication-link" class="form-input" v-model="diagnostic.communicationSupportLink" type="text">
  </div>
</template>

<script>
  export default {
    props: {
      modelValue: Object,
    },
    computed: {
      diagnostic() {
        return this.modelValue;
      }
    }
  }
</script>

<style scoped lang="scss">
  fieldset {
    border: none;
    padding: 0;
    margin: 0;
  }

  .form-communication-support {
    legend {
      text-align: left;
      font-weight: bold;
    }

    .form-group {
      display: flex;
      flex-direction: column;
      margin-top: 20px;
    }

    .form-item {
      justify-content: left;

      label {
        font-weight: normal;
        line-height: 35px;
        padding-left: 5px;
        cursor: pointer;
      }

      input {
        width: 30px;
        height: 30px;
      }
    }
  }

  .form-item {
    display: flex;
    justify-content: space-between;
  }

  label {
    font-weight: bold;
    max-width: 45%;
    text-align: left;
  }

  input {
    border: none;
    height: 50px;
    width: 35%;
    padding: 5px;
    font-size: 1.5em;
    text-align: right;
  }
</style>
