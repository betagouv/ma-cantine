<template>
  <v-card :to="canteenLink" class="dsfr d-flex flex-column" outlined :ripple="false">
    <v-img :src="canteenImage || '/static/images/canteen-default-image.jpg'" height="160" max-height="160"></v-img>
    <v-card-title>
      <h3 class="fr-h6 font-weight-bold mb-1">{{ canteen.name }}</h3>
    </v-card-title>
    <v-card-subtitle class="pb-0 mx-n1">
      <DsfrTag
        v-if="teledeclarationIsActive"
        :text="teledeclarationStatus.text"
        :color="teledeclarationStatus.color"
        :small="true"
      />
      <DsfrTag :text="publicationStatus.text" :color="publicationStatus.color" :small="true" />
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
import { lastYear } from "@/utils"

export default {
  name: "CentralKitchenCard",
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
    teledeclarationIsActive() {
      return window.ENABLE_TELEDECLARATION
    },
    canteenLink() {
      if (window.ENABLE_DASHBOARD) {
        return {
          name: "DashboardManager",
          params: { canteenUrlComponent: this.$store.getters.getCanteenUrlComponent(this.canteen) },
        }
      }
      return {
        name: "CanteenModification",
        params: { canteenUrlComponent: this.$store.getters.getCanteenUrlComponent(this.canteen) },
      }
    },
  },
}
</script>
