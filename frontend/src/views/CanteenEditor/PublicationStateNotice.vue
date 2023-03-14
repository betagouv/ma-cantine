<template>
  <div>
    <DsfrCallout v-if="isPublished" icon="$checkbox-circle-fill" color="green">
      Cette cantine est actuellement publiée sur
      <router-link
        :to="{
          name: 'CanteenPage',
          params: { canteenUrlComponent: $store.getters.getCanteenUrlComponent(canteen) },
        }"
        target="_blank"
      >
        nos cantines
        <v-icon small class="ml-1" color="primary">mdi-open-in-new</v-icon>
      </router-link>
    </DsfrCallout>
    <DsfrCallout v-else-if="readyToPublish" class="mb-1">
      <span class="grey--text text--darken-2">
        Vos données d'approvisionnement pour l'année {{ publicationYear }} sont completées, alors nous vous encourageons
        de publier votre cantine.
        <router-link v-if="includeLink" :to="{ name: 'PublicationForm', params: { canteenUrlComponent } }">
          Publier cette cantine.
        </router-link>
      </span>
    </DsfrCallout>
    <!-- includeLink currently only used by CanteenPage, where we don't want this to show. Bit hacky -->
    <DsfrCallout color="#C08C65" class="mb-1" v-else-if="!includeLink">
      <span class="grey--text text--darken-2">
        Nous vous conseillons de remplir des
        <router-link :to="{ name: 'DiagnosticList', params: { canteenUrlComponent } }">
          données d'approvisionnement pour l'année {{ this.publicationYear }}
        </router-link>
        avant que vous publiiez vos données.
      </span>
    </DsfrCallout>
  </div>
</template>

<script>
import { hasDiagnosticApproData, lastYear } from "@/utils"
import DsfrCallout from "@/components/DsfrCallout"

export default {
  name: "PublicationStateNotice",
  components: { DsfrCallout },
  props: {
    canteen: Object,
    includeLink: Boolean,
  },
  data() {
    return {
      publicationYear: lastYear(),
    }
  },
  computed: {
    canteenUrlComponent() {
      return this.$store.getters.getCanteenUrlComponent(this.canteen)
    },
    readyToPublish() {
      const diagnostic = this.canteen.diagnostics.find((x) => x.year === this.publicationYear)
      return this.canteen.publicationStatus === "draft" && !!diagnostic && hasDiagnosticApproData(diagnostic)
    },
    isPublished() {
      return this.canteen.publicationStatus === "published"
    },
  },
}
</script>
