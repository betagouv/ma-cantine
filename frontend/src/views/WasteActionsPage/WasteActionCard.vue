<template>
  <v-card outlined class="fill-height text-left d-flex flex-column dsfr expanded-link">
    <img
      :src="
        wasteAction.leadImage ? wasteAction.leadImage.meta.downloadUrl : '/static/images/wasteaction-default-image.jpg'
      "
      alt=""
    />
    <v-card-text class="pa-10 pb-5">
      <DsfrTagGroup v-if="wasteAction.wasteOrigin.length" :tags="tags" :closeable="false" :small="true" />
      <h2 class="mt-6 fr-h4">
        <router-link :to="{ name: 'WasteActionPage', params: { id: wasteAction.id } }">
          {{ wasteAction.title }}
        </router-link>
      </h2>
      <p class="mb-0">
        {{ wasteAction.subtitle }}
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
    wasteAction: {
      type: Object,
      required: true,
    },
  },
  components: { DsfrTagGroup },
  computed: {
    tags() {
      const effortLabel = Constants.WasteActionEffortLevels.find((item) => item.value === this.wasteAction.effort)?.text
      const effort = [{ id: this.wasteAction.effort, text: effortLabel || "Inconnu" }]
      const wasteOrigins = this.wasteAction.wasteOrigin.map((wasteOriginId) => {
        const wasteOriginLabel = Constants.WasteActionOrigins.find((item) => item.value === wasteOriginId)?.text
        return {
          id: wasteOriginId,
          text: wasteOriginLabel || "Inconnu",
        }
      })
      return effort.concat(wasteOrigins)
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
