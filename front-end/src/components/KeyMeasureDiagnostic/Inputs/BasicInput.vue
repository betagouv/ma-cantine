<template>
  <div class="basic-input">
    <label :for="inputId">{{label}}</label>
    <input :id="inputId" :value="modelValue" @input="$emit('update:modelValue', $event.target.value)" :type="type" :min="min">
  </div>
</template>

<script>
  export default {
    props: ['modelValue', 'label', 'inputId', 'type', 'min'],
  }
</script>

<style scoped lang="scss">
  .basic-input {
    display: flex;
    justify-content: space-between;
    margin: 10px 0;

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
  }
</style>
