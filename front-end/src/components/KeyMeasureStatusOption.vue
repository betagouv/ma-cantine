<template>
  <div class="measure-status">
    <span v-for="(text, status) in STATUSES"
      :key="status"
      class="status-radio-button" :class="{selected: measure.status === status}"
    >
      <input type="radio" :id="measure.id + '-' + status" class="status-input"
      :name="'status-'+measure.id" :value="status" v-model="measure.status" @change="saveStatus(measure.id, measure.status)">
      <label :for="measure.id + '-' + status" class="status-label">{{ text }}</label>
    </span>
  </div>
</template>

<script>
  import STATUSES from "@/data/STATUSES.json";
  import { saveStatus } from "@/data/KeyMeasures.js";

  export default {
    props: {
      initialMeasure: Object
    },
    data() {
      return {
        STATUSES,
        measure: this.initialMeasure
      }
    },
    methods: {
      saveStatus
    }
  }
</script>

<style scoped lang="scss">
  .measure-status {
    border-radius: 1em;
    overflow: hidden;
    /* offset-x | offset-y | blur-radius | spread-radius | color */
    box-shadow: 0px 0px 5px 1px $dark-white;
    height: 2.5em;
    display: flex;
    min-width: 14.5em;
  }

  .status-label {
    border: none;
    margin: 0;
    padding: 1em;
    white-space: nowrap;
    font-size: 14px;
    cursor: pointer;
    position: relative;
    top: 0.4em;
  }

  .status-input {
    opacity: 0;
    position: absolute;
  }

  .status-radio-button.selected, .status-radio-button:hover {
    background-color: $light-yellow;
  }

  @media (max-width: 1000px) {
    .status-label {
      padding: 1em 0.3em;
    }
  }

  @media (max-width: 700px) {
    .measure-status {
      margin: 0.5em 0;
    }

    .status-label {
      padding: 1em 1em;
    }
  }
</style>