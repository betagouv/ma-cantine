<template>
  <div class="select-input">
    <label :for="inputId">{{label}}</label>
    <select :id="inputId" :value="modelValue" @input="$emit('update:modelValue', $event.target.value)">
      <option v-for="(option, key) in options" :key="key" :value="key">
        {{option}}
      </option>
    </select>
  </div>
</template>

<script>
  export default {
    props: ['modelValue', 'label', 'inputId', 'options'],
  }
</script>

<style scoped lang="scss">
  .select-input {
    display: flex;
    justify-content: space-between;
    margin: 10px 0;

    label {
      font-weight: bold;
      max-width: 45%;
      text-align: left;
    }

    select {
      border: none;
      background-color: $white;
      text-align-last: right;
      height: 60px;
      width: 17%;
      font-size: 1.5em;
    }
  }
</style>
