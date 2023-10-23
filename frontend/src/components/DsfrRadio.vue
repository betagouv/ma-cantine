<template>
  <div>
    <fieldset id="radio-hint" aria-labelledby="radio-hint-legend radio-hint-messages">
      <legend v-if="$attrs.label" class="mb-2" id="radio-hint-legend">
        {{ $attrs.label }}
        <span v-if="$attrs.hint">{{ $attrs.hint }}</span>
      </legend>
      <v-radio-group class="my-0" ref="radio" v-bind="$attrs" v-on="$listeners" @change="(v) => $emit('input', v)">
        <v-radio v-for="item in $attrs.items" :key="item.value" :label="item.text" :value="item.value"></v-radio>
      </v-radio-group>
    </fieldset>
  </div>
</template>

<script>
export default {
  inheritAttrs: false,
  props: {
    labelClasses: {
      type: String,
      required: false,
      default: "mb-2 text-sm-subtitle-1 text-body-2 text-left",
    },
  },
  data() {
    return { inputId: null }
  },
  computed: {
    value() {
      return this.$refs["radio"].value
    },
  },
  methods: {
    removeInnerLabel() {
      const labels = this.$refs["radio"].$el.getElementsByTagName("legend")
      if (labels && labels.length > 0) for (const label of labels) label.parentNode.removeChild(label)
    },
    validate() {
      return this.$refs["radio"].validate()
    },
  },
  mounted() {
    this.removeInnerLabel()
  },
}
</script>

<style scoped>
.v-radio >>> label {
  color: inherit;
}
</style>
