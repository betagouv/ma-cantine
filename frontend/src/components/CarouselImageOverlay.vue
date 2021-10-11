<template>
  <div v-if="visible">
    <v-overlay :value="visible" :dark="false">
      <v-btn @click="close" class="close-overlay" fab dark small color="grey lighten-5">
        <v-icon color="red darken-3">mdi-close</v-icon>
      </v-btn>

      <v-carousel
        v-click-outside="close"
        :value="index"
        :height="carouselHeight"
        hide-delimiter-background
        :hide-delimiters="items.length <= 1"
        :show-arrows="items.length > 1"
      >
        <v-carousel-item
          v-for="(item, idx) in items"
          :key="idx"
          style="background: #333; border-radius: 5px; overflow: hidden;"
          :width="carouselWidth"
          :src="item.image"
          contain
        ></v-carousel-item>
      </v-carousel>
    </v-overlay>
  </div>
</template>

<script>
export default {
  name: "CarouselImageOverlay",
  props: {
    items: {
      type: Array,
      required: true,
    },
    index: {
      type: Number,
      default: 0,
    },
    visible: {
      type: Boolean,
      required: true,
    },
  },
  data() {
    return {}
  },
  computed: {
    carouselWidth() {
      switch (this.$vuetify.breakpoint.name) {
        case "xs":
        case "sm":
          return `${window.innerWidth - 30}px`
        case "md":
          return `${window.innerWidth - 60}px`
        default:
          return `${Math.min(window.innerWidth - 80, 1000)}px`
      }
    },
    carouselHeight() {
      return `${Math.min(window.innerHeight - 100, 800)}px`
    },
  },
  methods: {
    move(e) {
      e = e || window.event
      const leftArrowCode = "37"
      const rightArrowCode = "39"
      const escapeCode = "27"
      if (e.keyCode == leftArrowCode) {
        this.$emit("update:index", this.index === 0 ? this.items.length - 1 : this.index - 1)
      } else if (e.keyCode == rightArrowCode) {
        this.$emit("update:index", this.index === this.items.length - 1 ? 0 : this.index + 1)
      } else if (e.keyCode == escapeCode) {
        this.close()
      }
    },
    close() {
      this.$emit("done")
    },
  },
  mounted() {
    window.addEventListener("keydown", this.move)
  },
  beforeDestroy() {
    window.removeEventListener("keydown", this.move)
  },
}
</script>

<style scoped>
.close-overlay {
  position: absolute;
  right: -10px;
  top: -20px;
  z-index: 99999;
}
</style>
