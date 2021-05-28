<template>
  <fieldset>
    <legend>{{ legend }}</legend>

    <div class="radios">
      <div v-for="option in options" :key="option.inputId" class="radio">
        <input
          :id="option.inputId"
          :checked="modelValue === option.value"
          @input="$emit('update:modelValue', option.value)"
          type="radio"
        />
        <label :for="option.inputId">{{ option.label }}</label>
      </div>
    </div>
  </fieldset>
</template>

<script>
export default {
  props: ["legend", "modelValue", "options"],
}
</script>

<style scoped lang="scss">
fieldset {
  border: none;
  padding: 0;
  margin: 10px 0;
}

legend {
  text-align: left;
  font-weight: bold;
  padding: 0;
}

.radios {
  display: flex;
  flex-wrap: wrap;
  margin-top: 10px;
}

.radio {
  display: flex;
  min-width: 150px;
  width: 30%;
  justify-content: left;
  padding: 10px;
  text-align: left;

  label {
    padding-left: 5px;
    max-width: 105px;
    cursor: pointer;
    font-weight: normal !important;
  }

  input {
    width: 30px;
    height: 30px;
  }
}
</style>
