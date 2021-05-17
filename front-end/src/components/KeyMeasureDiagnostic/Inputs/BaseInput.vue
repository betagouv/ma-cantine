<template>
  <div class="basic-input">
    <label :for="inputId">{{label}}</label>
    <input :id="inputId" :value="modelValue" @input="$emit('update:modelValue', $event.target.value)" :type="type" :min="min" :required="required">
  </div>
</template>

<script>
  export default {
    props: ['modelValue', 'label', 'inputId', 'type', 'min', 'required'],
  }
</script>

<style scoped lang="scss">
  .basic-input {
    display: flex;
    flex-direction: column;
    margin: 10px 0;

    label {
      text-align: left;
      font-weight: bold;
    }

    input {
      max-width: 20em;
      margin-top: 10px;
      border: none;
      font-size: 1.2em;
      padding: 5px;
      border: 1px solid $yellow;
      border-radius: 4px;
    }
  }
</style>
