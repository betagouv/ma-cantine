<template>
  <CheckboxUnique
    v-model="diagnostic.hasMadeWasteDiagnostic"
    :label="'J’ai réalisé un diagnostic sur les causes probables de gaspillage alimentaire'"
    :inputId="'diagnostic-made'"
  />

  <fieldset class="form-bloc">
    <legend>J'ai réalisé des actions de lutte contre le gaspillage alimentaire</legend>

    <div class="form-group">
      <div class="form-item">
        <input id="pre-registration" value="preRegistration" v-model="diagnostic.wasteActions" type="checkbox" >
        <label for="pre-registration"><p>Pré-inscription des convives obligatoire</p></label>
      </div>

      <div class="form-item">
        <input id="raise-awareness" value="raiseAwareness" v-model="diagnostic.wasteActions" type="checkbox" >
        <label for="raise-awareness"><p>Sensibilisation par affichage ou autre média</p></label>
      </div>

      <div class="form-item">
        <input id="training" value="training" v-model="diagnostic.wasteActions" type="checkbox" >
        <label for="training"><p>Formation / information du personnel de restauration</p></label>
      </div>

      <div class="form-item">
        <input id="reorganization" value="reorganization" v-model="diagnostic.wasteActions" type="checkbox" >
        <label for="reorganization"><p>Réorganisation de la distribution des composantes du repas</p></label>
      </div>

      <div class="form-item">
        <input id="portion-size" value="portionSize" v-model="diagnostic.wasteActions" type="checkbox" >
        <label for="portion-size"><p>Choix des portions (grande faim, petite faim)</p></label>
      </div>

      <div class="form-item">
        <input id="reuse" value="reuse" v-model="diagnostic.wasteActions" type="checkbox" >
        <label for="reuse"><p>Réutilisation des restes de préparation / surplus</p></label>
      </div>
    </div>
  </fieldset>

  <CheckboxUnique
    v-model="diagnostic.hasCovenant"
    :label="'J’ai proposé des conventions de dons à des associations habilitées d’aide alimentaire'"
    :inputId="'has-covenant'"
  />
</template>

<script>
  import CheckboxUnique from '@/components/KeyMeasureDiagnostic/Inputs/CheckboxUnique';

  export default {
    components: {
      CheckboxUnique
    },
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
      justify-content: left;
      padding: 5px 0;

      label {
        text-align: left;
        font-weight: normal;
        padding-left: 5px;
        max-width: 85%;
        cursor: pointer;
        height: 30px;
        display: table;

        p {
          display: table-cell;
          vertical-align: middle;
        }
      }

      input {
        width: 30px;
        height: 30px;
      }
    }
  }
</style>
