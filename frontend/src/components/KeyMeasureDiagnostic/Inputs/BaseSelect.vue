<template>
  <div class="select-input">
    <label :for="inputId">{{ label }}</label>
    <select :id="inputId" :value="modelValue" @input="$emit('update:modelValue', $event.target.value)">
      <option v-for="(option, key) in options" :key="key" :value="key">
        {{ option }}
      </option>
    </select>
  </div>
</template>

<script>
export default {
  props: ["modelValue", "label", "inputId", "options"],
}
</script>

<style scoped lang="scss">
.select-input {
  display: flex;
  flex-direction: column;
  margin: 10px 0;

  label {
    text-align: left;
    font-weight: bold;
  }

  select {
    max-width: 20em;
    margin-top: 10px;
    border: none;
    font-size: 1.2em;
    padding: 5px;
    border: 1px solid $ma-cantine-yellow;
    border-radius: 4px;
  }
}
</style>
