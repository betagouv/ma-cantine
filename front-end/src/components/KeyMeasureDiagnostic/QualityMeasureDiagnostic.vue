<template>
  <div class="form-item">
    <label for="value-total-2019" class="form-label">Je connais la valeur totale (en HT) de mes achats alimentaires en 2019</label>
    <input id="value-total-2019" class="form-input" v-model="diagnostic['2019'].valueTotal" type="number" min=0>
  </div>

  <div class="form-item">
    <label for="value-bio-2019" class="form-label">Je connais la valeur (en HT) des achats alimentaires de produits bio sur 2019</label>
    <input id="value-bio-2019" class="form-input" v-model="diagnostic['2019'].valueBio" type="number" min=0>
  </div>

  <div class="form-item">
    <label for="value-sustainable-2019" class="form-label">Je connais la valeur (en HT) des achats alimentaires de produits durables (hors bio) sur 2019</label>
    <input id="value-sustainable-2019" class="form-input" v-model="diagnostic['2019'].valueSustainable" type="number" min=0>
  </div>

  <div class="form-item">
    <label for="value-fair-trade-2019" class="form-label">Je connais la valeur (en HT) des achats alimentaires de produits issus du commerce équitable sur 2019</label>
    <input id="value-fair-trade-2019" class="form-input" v-model="diagnostic['2019'].valueFairTrade" type="number" min=0>
  </div>

  <div class="form-item">
    <label for="value-total-2020" class="form-label">Je connais la valeur totale (en HT) de mes achats alimentaires en 2020</label>
    <input id="value-total-2020" class="form-input" v-model="diagnostic['2020'].valueTotal" type="number" min=0>
  </div>

  <div class="form-item">
    <label for="value-bio-2020" class="form-label">Je connais la valeur (en HT) des achats alimentaires de produits bio sur 2020</label>
    <input id="value-bio-2020" class="form-input" v-model="diagnostic['2020'].valueBio" type="number" min=0>
  </div>

  <div class="form-item">
    <label for="value-sustainable-2020" class="form-label">Je connais la valeur (en HT) des achats alimentaires de produits durables (hors bio) sur 2020</label>
    <input id="value-sustainable-2020" class="form-input" v-model="diagnostic['2020'].valueSustainable" type="number" min=0>
  </div>

  <div class="form-item">
    <label for="value-fair-trade-2020" class="form-label">Je connais la valeur (en HT) des achats alimentaires de produits issus du commerce équitable sur 2020</label>
    <input id="value-fair-trade-2020" class="form-input" v-model="diagnostic['2020'].valueFairTrade" type="number" min=0>
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
  .form-item {
    display: flex;
    justify-content: space-between;
    padding: 10px 0;
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
