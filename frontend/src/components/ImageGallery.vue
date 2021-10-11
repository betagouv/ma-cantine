<template>
  <div>
    <CarouselImageOverlay
      :items="images"
      :visible="imageCarouselVisible"
      :index.sync="carouselIndex"
      @done="imageCarouselVisible = false"
    />
    <v-row>
      <v-col v-for="(image, index) in images" :key="index" cols="6" sm="4" md="3">
        <v-hover v-slot:default="{ hover }">
          <v-card flat style="cursor: pointer;overflow: hidden;">
            <v-img
              v-on:click="
                imageCarouselVisible = true
                carouselIndex = index
              "
              :src="image.image"
              aspect-ratio="1.2"
              class="grey lighten-2"
            >
              <div v-if="hover" class="d-flex display-3 white--text" style="height: 100%; background: #42424260;">
                <v-icon color="white" size="30" style="margin-left: auto; margin-right: auto;">
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
}
</script>
