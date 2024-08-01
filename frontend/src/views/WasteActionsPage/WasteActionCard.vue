<template>
  <v-card
    outlined
    class="fill-height text-left d-flex flex-column dsfr expanded-link"
    :to="{ name: 'WasteActionPage', params: { id: wasteaction.id } }"
  >
    <img
      :src="wasteaction.lead_image ? wasteaction.lead_image.url : '/static/images/wasteaction-default-image.png'"
      alt=""
    />
    <v-card-title class="d-flex flex-column-reverse align-start">
      <DsfrTagGroup v-if="wasteaction.waste_origin.length" :tags="tags" :closeable="false" :small="true" />
      {{ wasteaction.title }}
    </v-card-title>
    <v-card-subtitle class="pt-1">
      <p class="mb-0">
        {{ wasteaction.subtitle }}
      </p>
    </v-card-subtitle>
  </v-card>
</template>

<script>
import DsfrTagGroup from "@/components/DsfrTagGroup"

export default {
  name: "WasteActionCard",
  props: {
    wasteaction: {
      type: Object,
      required: true,
    },
  },
  components: { DsfrTagGroup },
  methods: {},
  computed: {
    tags() {
      const effort = [{ id: this.wasteaction.effort, text: this.wasteaction.effort, color: "rgb(238, 238, 238)" }]
      const waste_origins = this.wasteaction.waste_origin.map((tag) => {
        return {
          id: tag,
          text: tag,
          color: "rgb(238, 238, 238)",
        }
      })
      return effort.concat(waste_origins)
    },
  },
}
</script>

<style scoped>
img {
  height: 200px;
  max-width: 100%;
  object-fit: cover;
}
</style>
