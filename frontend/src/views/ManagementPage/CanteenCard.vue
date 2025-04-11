<template>
  <v-card :to="canteenLink" class="dsfr d-flex flex-column" outlined :ripple="false">
    <v-img :src="canteenImage || '/static/images/canteen-default-image.jpg'" height="160" max-height="160"></v-img>
    <v-card-title>
      <h3 class="fr-h6 font-weight-bold mb-1">{{ canteen.name }}</h3>
    </v-card-title>
    <v-card-subtitle class="pb-0 mx-n1">
      <p class="pl-1 mb-2">SIRET : {{ canteen.siret || "inconnu" }}</p>
      <p v-if="canteen.sirenUniteLegale" class="pl-1 mb-2">SIREN de l'unité légale : {{ canteen.sirenUniteLegale }}</p>
      <DataInfoBadge :canteen-action="canteen.action" />
      <DsfrTag
        v-if="publicationStatusIsNotPublished"
        :text="publicationStatus.text"
        :color="publicationStatus.color"
        :small="true"
      />
    </v-card-subtitle>
    <v-card-subtitle class="mt-0 pb-0 pt-2">
      <ProductionTypeTag :canteen="canteen" position="top-left" />
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
import ProductionTypeTag from "@/components/ProductionTypeTag"
import DsfrTag from "@/components/DsfrTag"
import DataInfoBadge from "@/components/DataInfoBadge"
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
    ProductionTypeTag,
    DsfrTag,
    DataInfoBadge,
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
    publicationStatusIsNotPublished() {
      return this.canteen.publicationStatus !== "published"
    },
    canteenImage() {
      return this.canteen.leadImage?.image
    },
    canteenLink() {
      return {
        name: "DashboardManager",
        params: { canteenUrlComponent: this.$store.getters.getCanteenUrlComponent(this.canteen) },
      }
    },
  },
}
</script>
