<template>
  <v-card
    outlined
    class="fill-height text-left d-flex flex-column dsfr expanded-link"
    :to="{ name: 'WasteActionPage', params: { id: wasteaction.id } }"
  >
    <v-img
      v-if="wasteaction.lead_image"
      :src="wasteaction.lead_image.url"
      class="lead-image"
      alt="wasteaction.lead_image.title"
      max-height="150"
      cover
    >
      <DsfrTag :text="wasteaction.effort" :color="tagColor(wasteaction.effort)" class="mt-2 ml-2" />
    </v-img>
    <div class="mt-2 ml-2">
      <DsfrTag v-if="!wasteaction.lead_image" :text="wasteaction.effort" :color="tagColor(wasteaction.effort)" />
    </div>
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
import DsfrTag from "@/components/DsfrTag"

export default {
  name: "WasteActionCard",
  props: {
    wasteaction: {
      type: Object,
      required: true,
    },
  },
  components: { DsfrTagGroup, DsfrTag },
  methods: {
    tagColor(tag) {
      switch (tag) {
        case "Petit pas":
          return "success"
        case "Moyen":
          return "warning"
        case "Grand projet":
          return "error"
        default:
          return "default"
      }
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

<style scoped></style>
