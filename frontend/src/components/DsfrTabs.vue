<template>
  <div>
    <v-tabs v-bind="$attrs" v-model="tab" v-on="$listeners">
      <slot name="tabs" />
    </v-tabs>

    <v-tabs-items v-model="tab">
      <slot name="items" />
    </v-tabs-items>
  </div>
</template>

<script>
export default {
  inheritAttrs: false,
  props: ["value"],
  data() {
    return {
      tab: null,
    }
  },
}
</script>
