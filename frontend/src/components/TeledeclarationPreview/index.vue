<template>
  <v-dialog v-model="isOpen" max-width="900">
    <!-- maybe make dialog fullscreen for xs (and s) ? -->
    <SingleView :canteen="canteen" :diagnostic="diagnostic" @teledeclare="teledeclare" @close="close" />
  </v-dialog>
</template>

<script>
import SingleView from "./SingleView"

export default {
  components: { SingleView },
  props: {
    value: {
      required: true,
    },
    diagnostic: {
      required: true,
    },
    canteen: {
      required: true,
    },
  },
  computed: {
    isOpen: {
      get() {
        return this.value
      },
      set(newValue) {
        this.$emit("input", newValue)
      },
    },
  },
  methods: {
    teledeclare() {
      this.$emit("teledeclare")
    },
    close() {
      this.$emit("input", false)
    },
  },
}
</script>
