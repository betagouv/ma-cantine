<template>
  <fieldset>
    <legend>{{legend}}</legend>

    <div class="checkboxes">
      <div v-for="(option, key) in options" :key="key" class="checkbox">
        <input :id="key" :checked="modelValue.includes(key)" @input="updateInput(key, $event)" type="checkbox" >
        <label :for="key"><p>{{option}}</p></label>
      </div>
    </div>
  </fieldset>
</template>

<script>
  export default {
    props: ['legend', 'modelValue', 'options'],
    data() {
      return {
        newValue: this.modelValue,
      };
    },
    methods: {
      updateInput(value, event) {
        event.target.checked ? this.newValue.push(value) : this.newValue.splice(this.newValue.indexOf(value), 1);

        this.$emit('update:modelValue', this.newValue);
      }
    }
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

  .checkboxes {
    display: flex;
    flex-direction: column;
    margin-top: 10px;
  }

  .checkbox {
    display: flex;
    justify-content: left;
    align-items: center;
    padding: 5px 0;

    label {
      text-align: left;
      font-weight: normal;
      max-width: 85%;
      padding-left: 5px;
      cursor: pointer;
      height: 30px;
      display: table;

      p {
        display: table-cell;
        vertical-align: middle;
      }
    }

    input {
      width: 30px;
      height: 30px;
    }
  }
</style>
