<template>
  <div class="checkbox-unique">
    <label :for="inputId">{{label}}</label>
    <input :id="inputId" :checked="modelValue" @input="$emit('update:modelValue', $event.target.checked)" type="checkbox" />
  </div>
</template>

<script>
  export default {
    props: ['modelValue', 'label', 'inputId', 'type', 'min'],
  }
</script>

<style scoped lang="scss">
  .checkbox-unique {
    display: flex;
    justify-content: space-between;
    padding: 10px 0;

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
  }
</style>
