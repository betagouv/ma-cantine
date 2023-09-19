<template>
  <div>
    <label v-if="$attrs.label" :for="inputId" :class="labelClasses">
      {{ $attrs.label }}
    </label>
    <v-select
      ref="select"
      density="compact"
      single-line
      v-bind="$attrs"
      persistent-placeholder
      :item-title="itemTitle"
      @update:model-value="(v) => $emit('input', v)"
    >
      <template #label><span></span></template>
      <!-- https://github.com/vuetifyjs/vuetify/issues/15721#issuecomment-1595860094 -->
      <template #item="{ item, props }">
        <v-divider v-if="'divider' in item.raw" class="pb-0" />
        <v-list-subheader v-else-if="'header' in item.raw" :title="item.raw.header" />
        <!-- include item.text for backwards compatibility old vuetify 2 code -->
        <v-list-item
          v-else-if="!$attrs.hasOwnProperty('multiple')"
          v-bind="props"
          :title="item.raw.title || item.raw.text"
          :value="item.value"
        />
        <v-list-item v-else>
          <v-checkbox
            v-bind="$attrs"
            :label="item.raw.title || item.raw.text"
            :value="item.value"
            class="my-0 text-black"
            hide-details
            color="primary"
          />
        </v-list-item>
      </template>
    </v-select>
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
  emits: ["input"],
  data() {
    return { inputId: null }
  },
  computed: {
    value() {
      return this.$refs["select"].value
    },
    // for backwards compatibility with vuetify 2, try to deduce item display text from values given
    // necessary despite VListItem to show the values properly once selected
    itemTitle() {
      const item = this.$attrs.items.find((i) => !!i.value)
      return item?.text ? "text" : "title"
    },
  },
  mounted() {
    this.removeInnerLabel()
    this.assignInputId()
  },
  methods: {
    removeInnerLabel() {
      const labels = this.$refs["select"].$el.getElementsByTagName("label")
      if (labels && labels.length > 0) for (const label of labels) label.parentNode.removeChild(label)
    },
    validate() {
      return this.$refs["select"].validate()
    },
    assignInputId() {
      this.inputId = this.$refs?.["select"]?.$refs?.["input"]?.id
    },
  },
}
</script>

<style scoped>
.v-select >>> .v-input__slot {
  border-radius: 0.25rem 0.25rem 0 0;
  background-color: #eee !important;
  box-shadow: inset 0 -2px 0 0 #3a3a3a;
  transition: none;
}

.v-select.error--text >>> .v-input__slot {
  border-radius: 0.25rem 0.25rem 0 0;
  background-color: #eee !important;
  box-shadow: inset 0 -2px 0 0 #ff5252;
}

.v-select >>> .v-input__slot:focus-within {
  outline-style: solid;
  outline-width: 2px;
  outline-color: #0a76f6;
  outline-offset: 2px;
  border-radius: 2px 2px 0 0;
}

div > label {
  display: block;
}
</style>
