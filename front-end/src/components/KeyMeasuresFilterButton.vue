<template>
    <button type="button" class="filter-button" :class="{active: isActive}" @click="$emit('toggle-activation')">{{text}}</button>
</template>

<style scoped>
.filter-button {
  border: none;
  background-color: #fff;
  cursor: pointer;
  margin: 0.5em;
  font-weight: bold;
  font-size: 20px;
  /* Dark 1 */
  color: #333333;
}

.filter-button.active {
  width: 244px;
  height: 43px;
  left: 0px;
  top: 0px;

  /* Green 3 */
  background: #F1F3EE;
  border-radius: 42px;
  /* Green 1 */
  color: #748852;
}
</style>

<script>
export default {
  name: "KeyMeasuresFilterButton",
  props: {
    text: String,
    isActive: Boolean
  }
};
</script>