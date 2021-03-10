<template>
  <fieldset class="form-bloc">
    <legend>A quelle fréquence proposez-vous un repas végétarien ?</legend>

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
    <legend>Le menu végétarien proposé est un menu unique ou une alternative à d’autres menus ?</legend>

    <div class="form-group">
      <div class="form-item">
        <input id="standalone" value="standalone" v-model="diagnostic.vegetarianMenuIsStandalone" type="radio" >
        <label for="standalone">Un menu végétarien unique</label>
      </div>

      <div class="form-item">
        <input id="vegetarian-or-meat" value="vegetarianOrMeat" v-model="diagnostic.vegetarianMenuIsStandalone" type="radio" >
        <label for="vegetarian-or-meat">Un menu végétarien alternatif à un menu carné</label>
      </div>

      <div class="form-item">
        <input id="all-vegetarians" value="allVegetarians" v-model="diagnostic.vegetarianMenuIsStandalone" type="radio" >
        <label for="all-vegetarians">Menus tous végétariens</label>
      </div>
    </div>
  </fieldset>
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

  .form-bloc {
    legend {
      text-align: left;
      font-weight: bold;
    }

    .form-group {
      display: flex;
      margin-top: 20px;
      flex-wrap: wrap;
      justify-content: space-between;
    }

    .form-item {
      display: flex;
      justify-content: space-between;
      width: 180px;
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
