<template>
  <CheckboxUnique
    v-model="diagnostic.hasMadeDiversificationPlan"
    :label="'J’ai mis en place un plan pluriannuel de diversification des protéines'"
    :inputId="'plan-made'"
  />

  <fieldset class="form-bloc">
    <legend>J’ai mis en place un menu végétarien dans ma cantine :</legend>

    <div class="form-group">
      <div class="form-item">
        <input id="less-than-once" value="lessThanOnce" v-model="diagnostic.vegetarianFrequency" type="radio" >
        <label for="less-than-once">Moins d'une fois par semaine</label>
      </div>

      <div class="form-item">
        <input id="once" value="once" v-model="diagnostic.vegetarianFrequency" type="radio" >
        <label for="once">1 fois par semaine</label>
      </div>

      <div class="form-item">
        <input id="more-than-once" value="moreThanOnce" v-model="diagnostic.vegetarianFrequency" type="radio" >
        <label for="more-than-once">Plus d'une fois par semaine</label>
      </div>
    </div>
  </fieldset>

  <fieldset class="form-bloc">
    <legend>Le menu végétarien proposé est :</legend>

    <div class="form-group">
      <div class="form-item">
        <input id="standalone" value="standalone" v-model="diagnostic.vegetarianMenuType" type="radio" >
        <label for="standalone">Un menu végétarien unique</label>
      </div>

      <div class="form-item">
        <input id="all-vegetarian" value="allVegetarian" v-model="diagnostic.vegetarianMenuType" type="radio" >
        <label for="all-vegetarian">Plusieurs menus végétariens alternatifs</label>
      </div>

      <div class="form-item">
        <input id="alternative" value="alternative" v-model="diagnostic.vegetarianMenuType" type="radio" >
        <label for="alternative">Un menu végétarien alternatif à d'autres menus non-végétariens</label>
      </div>
    </div>
  </fieldset>
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
    margin: 20px 0;

    legend {
      text-align: left;
      font-weight: bold;
    }

    .form-group {
      display: flex;
      margin-top: 20px;
      flex-wrap: wrap;
    }

    .form-item {
      display: flex;
      justify-content: space-between;
      min-width: 150px;
      width: 30%;
      justify-content: left;
      padding: 10px;
      text-align: left;

      label {
        font-weight: normal;
        padding-left: 5px;
        max-width: 105px;
        cursor: pointer;
      }

      input {
        width: 30px;
        height: 30px;
      }
    }
  }
</style>
