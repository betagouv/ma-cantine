<template>
  <div>
    <DsfrCallout v-if="publicationPending" class="mb-1 body-2">
      <span class="grey--text text--darken-2">
        La publication de cette cantine est en attente de validation. Une fois validé par notre équipe, vous recevrez un
        email confirmant sa publication.
        <router-link v-if="includeLink" :to="{ name: 'PublicationForm', params: { canteenUrlComponent } }">
          En voir plus.
        </router-link>
      </span>
    </DsfrCallout>
    <DsfrCallout v-else-if="readyToPublish" class="mb-1 body-2">
      <span class="grey--text text--darken-2">
        Vos données d'approvisionnement pour l'année {{ publicationYear }} sont completées, alors nous vous encourageons
        de publier votre cantine.
        <router-link v-if="includeLink" :to="{ name: 'PublicationForm', params: { canteenUrlComponent } }">
          Publier cette cantine.
        </router-link>
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
    publicationPending() {
      return this.canteen.publicationStatus === "pending"
    },
    canteenUrlComponent() {
      return this.$store.getters.getCanteenUrlComponent(this.canteen)
    },
    readyToPublish() {
      const diagnostic = this.canteen.diagnostics.find((x) => x.year === this.publicationYear)
      return this.canteen.publicationStatus === "draft" && !!diagnostic && hasDiagnosticApproData(diagnostic)
    },
  },
}
</script>
