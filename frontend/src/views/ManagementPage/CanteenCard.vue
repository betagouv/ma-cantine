<template>
  <v-card
    :to="{
      name: 'CanteenModification',
      params: { canteenUrlComponent: $store.getters.getCanteenUrlComponent(canteen) },
    }"
    class="dsfr d-flex flex-column"
    outlined
    :ripple="false"
  >
    <v-img :src="canteenImage || '/static/images/canteen-default-image.jpg'" height="160" max-height="160"></v-img>
    <v-card-title class="font-weight-bold">{{ canteen.name }}</v-card-title>
    <v-card-subtitle class="py-1">
      <v-chip small :color="publicationStatus.color" label>
        {{ publicationStatus.text }}
      </v-chip>
    </v-card-subtitle>
    <v-card-subtitle v-if="canteen.dailyMealCount || canteen.city || canteen.sectors" class="mt-0 pb-0">
      <CanteenIndicators :canteen="canteen" />
    </v-card-subtitle>
    <v-spacer></v-spacer>
    <v-card-actions class="px-4 py-4">
      <v-spacer></v-spacer>
      <span class="icon-hint access">Modifier {{ canteen.name }}</span>
    </v-card-actions>
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
          text: "En attente de validation",
        },
        published: {
          color: "green lighten-4",
          text: "Publiée",
        },
      }[this.canteen.publicationStatus || "draft"]
    },
    canteenImage() {
      if (!this.canteen.images || this.canteen.images.length === 0) return null
      return this.canteen.images[0].image
    },
  },
}
</script>

<style scoped>
.icon-hint {
  --icon-size: 1.75rem;
  height: var(--icon-size);
  width: var(--icon-size);
  overflow: hidden;
  display: inline-block;
  vertical-align: calc(0.435em - var(--icon-size) * 0.5);
}
.icon-hint::before {
  --icon-size: 1.75rem;
  content: "";
  display: inline-block;
  flex: 0 0 auto;
  height: var(--icon-size);
  width: var(--icon-size);
  --blue-france-sun-113-625: #000091;
  background-color: var(--blue-france-sun-113-625);
  vertical-align: calc(0.435em - var(--icon-size) * 0.5);
}
.access::before {
  -webkit-mask-image: url("/static/icons/arrow-right-line.svg");
  mask-image: url("/static/icons/arrow-right-line.svg");
}
</style>
