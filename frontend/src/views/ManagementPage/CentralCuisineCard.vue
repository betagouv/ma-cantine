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
    <div class="tag body-2 font-weight-medium">
      <v-icon class="mt-n1" small>$community-fill</v-icon>
      Cuisine centrale
    </div>
    <v-img :src="canteenImage || '/static/images/canteen-default-image.jpg'" height="160" max-height="160"></v-img>
    <v-card-title class="font-weight-bold">{{ canteen.name }}</v-card-title>
    <v-card-subtitle class="py-1">
      <v-chip small :color="teledeclarationStatus.color" label class="mr-1">
        {{ teledeclarationStatus.text }}
      </v-chip>
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
      <v-icon color="primary">$arrow-right-line</v-icon>
    </v-card-actions>
  </v-card>
</template>

<script>
import CanteenIndicators from "@/components/CanteenIndicators"
import { lastYear } from "@/utils"

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
  data() {
    return {
      teledeclarationYear: lastYear(),
    }
  },
  computed: {
    publicationStatus() {
      return {
        draft: {
          color: "grey lighten-4",
          text: "Non-publiée",
        },
        published: {
          color: "green lighten-4",
          text: "Publiée",
        },
      }[this.canteen.publicationStatus || "draft"]
    },
    teledeclarationStatus() {
      const diagnostics = this.canteen.diagnostics
      const diagnostic = diagnostics.find((d) => d.year === this.teledeclarationYear)
      const teledeclared = diagnostic && diagnostic.teledeclaration && diagnostic.teledeclaration.status === "SUBMITTED"
      if (teledeclared) {
        return {
          color: "green lighten-4",
          text: `Télédéclarée (${this.teledeclarationYear})`,
        }
      } else {
        return {
          color: "grey lighten-4",
          text: `Non-télédéclarée (${this.teledeclarationYear})`,
        }
      }
    },
    canteenImage() {
      if (!this.canteen.images || this.canteen.images.length === 0) return null
      return this.canteen.images[0].image
    },
  },
}
</script>

<style scoped>
.tag {
  position: absolute;
  top: 0;
  z-index: 1;
  background: #e0e0f2;
  left: 10px;
  padding: 3px 10px;
  border-radius: 0px 0px 4px 4px;
  box-shadow: 4px 0px 5px -4px black;
  color: #333;
}
</style>
