<template>
    <button type="button" class="filter-button" :class="{active: isActive}" @click="$emit('toggle-activation')">{{text}}</button>
</template>

<style scoped>
.filter-button {
  border: none;
  border: 2px solid #fff;
  background-color: #fff;
  cursor: pointer;
  margin: 0.2em 0em;
  padding: 0.5em 1em;
  border-radius: 42px;
  font-weight: bold;
  font-size: 18px;
  /* Dark 1 */
  color: #333333;
}

.filter-button.active {
  /* Green 3 */
  background: #F1F3EE;
  /* Green 1 */
  color: #748852;
}

.filter-button:hover {
  border-color: #F1F3EE;
}
</style>

<script>
export default {
  name: "FilterButton",
  props: {
    text: String,
    isActive: Boolean
  }
};
</script>