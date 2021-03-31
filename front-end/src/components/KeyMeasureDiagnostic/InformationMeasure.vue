<template>
  <fieldset class="form-communication-support">
    <legend>Information sur la qualité des approvisionnements :</legend>

    <div class="form-group">
      <div class="form-item">
        <input id="email-communication" value="email" v-model="diagnostic.communicationSupport" type="checkbox" >
        <label for="email-communication"><p>Envoi d’e-mail aux convives ou à leurs représentants</p></label>
      </div>

      <div class="form-item">
        <input id="display-communication" value="display" v-model="diagnostic.communicationSupport" type="checkbox" >
        <label for="display-communication"><p>Par affichage sur le lieu de restauration</p></label>
      </div>

      <div class="form-item">
        <input id="website-communication" value="website" v-model="diagnostic.communicationSupport" type="checkbox" >
        <label for="website-communication"><p>Sur site internet ou intranet (mairie, cantine)</p></label>
      </div>

      <div class="form-item">
        <input id="other-communication" value="other" v-model="diagnostic.communicationSupport" type="checkbox" >
        <label for="other-communication"><p>Autres moyens d'affichage et de communication électronique</p></label>
      </div>
    </div>
  </fieldset>

  <BasicInput
    v-model="diagnostic.communicationSupportLink"
    :label="'Lien vers le support de communication'"
    :inputId="'communication-link'"
    :type="'text'"
  />

  <CheckboxUnique
    v-model="diagnostic.communicateOnFoodPlan"
    :label="'Je communique sur la mise en place d\'un plan alimentaire'"
    :inputId="'food-plan'"
  />
</template>

<script>
  import BasicInput from '@/components/KeyMeasureDiagnostic/Inputs/BasicInput';
  import CheckboxUnique from '@/components/KeyMeasureDiagnostic/Inputs/CheckboxUnique';

  export default {
    components: {
      BasicInput,
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
    margin: 10px 0;
  }

  .form-communication-support {
    legend {
      text-align: left;
      font-weight: bold;
      padding: 0;
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
        max-width: 85%;
        padding-left: 5px;
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
