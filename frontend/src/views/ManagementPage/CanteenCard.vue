<template>
  <v-card
    :to="{
      name: 'CanteenModification',
      params: { canteenUrlComponent: $store.getters.getCanteenUrlComponent(canteen) },
    }"
  >
    <v-img :src="canteen.mainImage || '/static/images/canteen-default-image.jpg'" height="160"></v-img>
    <v-card-title class="font-weight-bold">{{ canteen.name }}</v-card-title>
    <v-card-subtitle class="py-1">
      <v-chip
        small
        :color="publicationStatus.color"
        label
        :to="{
          name: 'PublicationForm',
          params: { canteenUrlComponent: $store.getters.getCanteenUrlComponent(canteen) },
        }"
      >
        {{ publicationStatus.text }}
      </v-chip>
    </v-card-subtitle>
    <v-card-subtitle v-if="canteen.dailyMealCount || canteen.city || canteen.sectors" class="mt-0">
      <CanteenIndicators :canteen="canteen" />
    </v-card-subtitle>
  </v-card>
</template>

<script>
import CanteenIndicators from "@/components/CanteenIndicators"

export default {
  name: "CanteenCard",
  props: {
    canteen: {
      type: Object,
      required: true,
    },
  },
  components: {
    CanteenIndicators,
  },
  computed: {
    publicationStatus() {
      return {
        draft: {
          color: "grey lighten-4",
          text: "Pas encore publiée",
        },
        pending: {
          color: "amber lighten-4",
          // TODO: make it clear that the task is with our team, not theirs
          text: "En attente de validation",
        },
        published: {
          color: "green lighten-4",
          text: "Publiée",
        },
      }[this.canteen.publicationStatus || "draft"]
    },
  },
}
</script>
