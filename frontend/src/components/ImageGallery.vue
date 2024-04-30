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
        <v-hover v-slot:default="{ hover }">
          <v-card
            flat
            style="cursor: pointer;overflow: hidden;"
            v-on:click="openImage(index)"
            @keydown.enter="openImage(index)"
          >
            <v-img
              :src="image.image"
              aspect-ratio="1.2"
              class="image-card"
              :alt="image.altText"
              contain
              max-height="216"
            >
              <div
                v-if="hover"
                class="d-flex display-3 white--text"
                style="height: 100%; background: #42424260;"
                title="agrandir l'image"
              >
                <v-icon large color="white" size="30" style="margin-left: auto; margin-right: auto;">
                  mdi-magnify-plus-outline
                </v-icon>
              </div>
            </v-img>
          </v-card>
        </v-hover>
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
.v-card:focus {
  border: dotted 2px #0c7f46;
}
.image-card {
  background-color: #f5f5fe;
  border: solid 1px #dddddd;
}
</style>
