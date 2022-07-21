<template>
  <div>
    <v-alert v-if="publicationPending" color="indigo" class="mb-1 body-2" outlined>
      <span class="grey--text text--darken-2">
        <v-icon class="mb-1 mr-2" color="indigo">mdi-information-outline</v-icon>
        La publication de cette cantine est en attente de validation. Une fois validé par notre équipe, vous recevrez un
        email confirmant sa publication.
        <router-link v-if="includeLink" :to="{ name: 'PublicationForm', params: { canteenUrlComponent } }">
          En voir plus.
        </router-link>
      </span>
    </v-alert>
    <v-alert v-else-if="readyToPublish" color="primary" class="mb-1 body-2" outlined>
      <span class="grey--text text--darken-2">
        <v-icon class="mb-1 mr-2" color="primary">mdi-information-outline</v-icon>
        Vos données d'approvisionnement pour l'année {{ publicationYear }} sont completées, alors nous vous encourageons
        de publier votre cantine.
        <router-link v-if="includeLink" :to="{ name: 'PublicationForm', params: { canteenUrlComponent } }">
          Publier cette cantine.
        </router-link>
      </span>
    </v-alert>
  </div>
</template>

<script>
import { hasDiagnosticApproData, lastYear } from "@/utils"

export default {
  name: "PublicationStateNotice",
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
