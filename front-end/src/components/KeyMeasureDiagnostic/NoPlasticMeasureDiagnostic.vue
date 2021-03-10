<template>
  <div class="form-item">
    <label for="cooking-food-container">
      Je n’utilise plus de contenants alimentaires de cuisson / de réchauffe en plastique
    </label>
    <input id="cooking-food-container" v-model="diagnostic.cookingFoodContainersSubstituted" type="checkbox" />
  </div>

  <div class="form-item">
    <label for="service-food-container">
      Je n’utilise plus de contenants de service en plastique
    </label>
    <input id="service-food-container" v-model="diagnostic.serviceFoodContainersSubstituted" type="checkbox" />
  </div>

  <div class="form-item">
    <label for="water-bottles">
      Je ne mets plus à disposition des convives des bouteilles d’eau plate en plastique
    </label>
    <input id="water-bottles" v-model="diagnostic.waterBottlesSubstituted" type="checkbox" />
  </div>

  <div class="form-item">
    <label for="disposable-ustensils">
      Je ne mets plus à disposition des convives des ustensiles à usage unique en matière plastique
    </label>
    <input id="disposable-ustensils" v-model="diagnostic.disposableUstensilsSubstituted" type="checkbox" />
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
  }

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
</style>
