<template>
  <v-card outlined class="fill-height text-left d-flex flex-column dsfr expanded-link">
    <img
      :src="
        wasteaction.lead_image
          ? wasteaction.lead_image.meta.download_url
          : '/static/images/wasteaction-default-image.jpg'
      "
      alt=""
    />
    <v-card-text class="pa-10 pb-5">
      <DsfrTagGroup v-if="wasteaction.waste_origin.length" :tags="tags" :closeable="false" :small="true" />
      <h2 class="mt-6 fr-h4">
        <router-link :to="{ name: 'WasteActionPage', params: { id: wasteaction.id } }">
          {{ wasteaction.title }}
        </router-link>
      </h2>
      <p class="mb-0">
        {{ wasteaction.subtitle }}
      </p>
    </v-card-text>
    <v-spacer></v-spacer>
    <v-card-actions class="pa-10 pt-0">
      <v-spacer></v-spacer>
      <v-icon color="primary">$arrow-right-line</v-icon>
    </v-card-actions>
  </v-card>
</template>

<script>
import DsfrTagGroup from "@/components/DsfrTagGroup"
import Constants from "@/constants"

export default {
  name: "WasteActionCard",
  props: {
    wasteaction: {
      type: Object,
      required: true,
    },
  },
  components: { DsfrTagGroup },
  computed: {
    tags() {
      let effortLabel = Constants.WasteActionEffortLevels.find((item) => item.value === this.wasteaction.effort).text
      if (effortLabel === undefined) effortLabel = "default"
      const effort = [{ id: this.wasteaction.effort, text: effortLabel }]
      const waste_origins = this.wasteaction.waste_origin.map((wasteOriginId) => {
        let wasteOriginLabel = Constants.WasteActionOrigins.find((item) => item.value === wasteOriginId).text
        if (wasteOriginLabel === undefined) wasteOriginLabel = "default"
        return {
          id: wasteOriginId,
          text: wasteOriginLabel,
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
