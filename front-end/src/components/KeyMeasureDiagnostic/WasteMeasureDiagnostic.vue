<template>
  <div class="form-item-checkbox">
    <label for="diagnostic-made">
      J’ai réalisé un diagnostic sur tout ou partie des postes de gaspillage alimentaire
    </label>
    <input id="diagnostic-made" v-model="diagnostic.hasMadeWasteDiagnostic" type="checkbox" />
  </div>

  <fieldset class="form-bloc">
    <legend>Quelles actions avez vous mises en place contre le gaspillage alimentaire ?</legend>

    <div class="form-group">
      <div class="form-item">
        <input id="pre-registration" value="preRegistration" v-model="diagnostic.wasteActions" type="checkbox" >
        <label for="pre-registration">Pré-inscription des convives obligatoire</label>
      </div>

      <div class="form-item">
        <input id="sensitization" value="sensitization" v-model="diagnostic.wasteActions" type="checkbox" >
        <label for="sensitization">Sensibilisation par affichage ou autre média</label>
      </div>

      <div class="form-item">
        <input id="training" value="training" v-model="diagnostic.wasteActions" type="checkbox" >
        <label for="training">Formation / information du personnel de restauration</label>
      </div>

      <div class="form-item">
        <input id="reorganization" value="reorganization" v-model="diagnostic.wasteActions" type="checkbox" >
        <label for="reorganization">Réorganisation de la distribution des composantes du repas</label>
      </div>

      <div class="form-item">
        <input id="portion-size" value="portionSize" v-model="diagnostic.wasteActions" type="checkbox" >
        <label for="portion-size">Choix des portions (grande faim, petite faim)</label>
      </div>

      <div class="form-item">
        <input id="reuse" value="reuse" v-model="diagnostic.wasteActions" type="checkbox" >
        <label for="reuse">Réutilisation des restes de préparation / surplus</label>
      </div>
    </div>
  </fieldset>

  <div class="form-item-checkbox">
    <label for="has-covenant">
      J’ai proposé des conventions de dons à des associations habilitées d’aide alimentaire
    </label>
    <input id="has-covenant" v-model="diagnostic.hasCovenant" type="checkbox" />
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
  .form-item-checkbox {
    display: flex;
    justify-content: space-between;

    label {
      font-weight: bold;
      max-width: 45%;
      text-align: left;
      cursor: pointer;
    }

    input {
      width: 30px;
      height: 30px;
    }
  }

  fieldset {
    border: none;
    padding: 0;
    margin: 0;
  }

  .form-bloc {
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
      display: flex;
      justify-content: space-between;
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
</style>
