<template>
  <v-card outlined class="fill-height text-left d-flex flex-column dsfr expanded-link ">
    <v-img
      v-if="wasteaction.lead_image"
      :src="wasteaction.lead_image.meta.download_url"
      class="lead-image"
      alt="wasteaction.lead_image.title"
      max-height="150"
      cover
    >
      <DsfrBadge :mode="wasteaction.effort == 'SMALL' ? 'SUCCESS' : 'ERROR'" class="mt-2 ml-2">
        {{ wasteaction.effort }}
      </DsfrBadge>
    </v-img>
    <DsfrBadge
      v-if="!wasteaction.lead_image"
      :mode="wasteaction.effort == 'SMALL' ? 'SUCCESS' : 'ERROR'"
      class="mt-2 ml-2"
    >
      {{ wasteaction.effort }}
    </DsfrBadge>
    <v-card-title class="d-flex flex-column-reverse align-start">
      <DsfrTagGroup v-if="wasteaction.waste_origin.length" :tags="wasteOrigins" :closeable="false" :small="true" />
      {{ wasteaction.title }}
    </v-card-title>
    <v-card-subtitle class="pt-1">
      <p class="mb-0">
        {{ wasteaction.subtitle }}
      </p>
    </v-card-subtitle>
    <!-- <v-card-actions class="px-4 py-0">
      <v-spacer></v-spacer>
      <v-icon color="primary">$arrow-right-line</v-icon>
    </v-card-actions> -->
  </v-card>
</template>

<script>
import DsfrTagGroup from "@/components/DsfrTagGroup"
import DsfrBadge from "@/components/DsfrBadge"

export default {
  name: "WasteActionCard",
  props: {
    wasteaction: {
      type: Object,
      required: true,
    },
  },
  components: { DsfrTagGroup, DsfrBadge },
  methods: {
    tagColor(tag) {
      const colours = [
        "pink lighten-4",
        "blue lighten-4",
        "green lighten-4",
        "purple lighten-4",
        "yellow lighten-4",
        "teal lighten-4",
      ]
      const colourIndex = Array.from(tag, (x) => x.charCodeAt(0)).reduce((a, b) => a + b) % (colours.length - 1)
      return colours[colourIndex]
    },
  },
  computed: {
    wasteOrigins() {
      return this.wasteaction.waste_origin.map((tag) => {
        return {
          id: tag,
          text: tag,
          color: "rgb(238, 238, 238)",
        }
      })
    },
  },
}
</script>

<style scoped>
.wasteaction-card {
  min-height: 256px;
  height: 100%;
}
.wasteaction-card img.lead-image {
  opacity: 0.5;
  max-height: 100%;
  max-width: 100%;
  height: 100%;
  width: 100%;
  object-fit: cover;
  position: absolute;
}
.wasteaction-card:hover img.lead-image,
.wasteaction-card:focus-within img.lead-image {
  opacity: 1;
}
.card-image-wrap {
  position: relative;
}
</style>
