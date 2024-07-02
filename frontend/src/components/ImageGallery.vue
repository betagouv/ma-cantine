<template>
  <div>
    <CarouselImageOverlay
      :items="images"
      :visible="imageCarouselVisible"
      :index.sync="carouselIndex"
      @done="imageCarouselVisible = false"
    />
    <v-row>
      <v-col v-for="(image, index) in images" :key="index" cols="12" sm="4">
        <button @click="openImage(index)" class="image-open" title="agrandir l'image" aria-label="agrandir l'image">
          <img :src="image.image" :alt="image.altText || ''" />
          <span class="overlay align-center justify-center">
            <v-icon large color="white" size="30">
              mdi-magnify-plus-outline
            </v-icon>
          </span>
        </button>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import CarouselImageOverlay from "@/components/CarouselImageOverlay"

export default {
  name: "ImageGallery",
  components: { CarouselImageOverlay },
  data() {
    return {
      imageCarouselVisible: false,
      carouselIndex: 0,
    }
  },
  props: {
    images: {
      type: Array,
      required: true,
    },
  },
  methods: {
    openImage(index) {
      this.imageCarouselVisible = true
      this.carouselIndex = index
    },
  },
}
</script>
<style scoped>
button.image-open {
  background-color: #f5f5fe;
  border: solid 1px #dddddd;
  height: 216px;
  width: 100%;
  position: relative;
}
button.image-open:hover > .overlay,
button.image-open:focus > .overlay {
  display: flex;
}
.overlay {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  width: 100%;
  background-color: #42424260;
  display: none;
}
button.image-open > img {
  height: 100%;
  width: 100%;
  object-fit: contain;
}
</style>
