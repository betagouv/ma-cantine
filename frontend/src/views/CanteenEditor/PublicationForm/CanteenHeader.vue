<template>
  <div :class="{ 'd-sm-flex align-center': !hasLongCanteenName }">
    <div class="d-sm-flex align-center mb-3 mr-2">
      <UploadLogo v-if="$vuetify.breakpoint.smAndUp" :canteen="canteen" />
      <div>
        <h2 class="mb-2">{{ canteen.name }}</h2>
        <div>
          <CanteenIndicators :canteen="canteen" :singleLine="true" :useCategories="true" />
        </div>
      </div>
    </div>
    <v-spacer></v-spacer>
    <div :class="{ 'fr-text-sm': true, 'text-right': hasLongCanteenName }">
      <p class="mb-0">Vous remarquez une erreur ?</p>
      <router-link
        :to="{
          name: 'GestionnaireCantineGerer',
          params: { canteenUrlComponent: this.$store.getters.getCanteenUrlComponent(canteen) },
        }"
      >
        <v-icon class="mr-1" small>mdi-pencil</v-icon>
        Modifier mon établissement
      </router-link>
    </div>
    <UploadLogo v-if="$vuetify.breakpoint.xs" :canteen="canteen" class="my-4" />
  </div>
</template>

<script>
import CanteenIndicators from "@/components/CanteenIndicators"
import UploadLogo from "./UploadLogo"

export default {
  name: "CanteenHeader",
  props: {
    canteen: {
      type: Object,
    },
  },
  components: { CanteenIndicators, UploadLogo },
  computed: {
    hasLongCanteenName() {
      return this.canteen.name.length > 70
    },
  },
}
</script>
