<template>
  <div class="text-left">
    <div class="d-block d-sm-flex align-center justify-space-between">
      <div class="d-flex flex-column mb-2">
        <h1 class="fr-text font-weight-bold">Mon affiche</h1>
        <DsfrBadge :mode="badge.mode" :icon="badge.icon">
          <p class="mb-0 text-uppercase">{{ badge.text }}</p>
        </DsfrBadge>
      </div>
      <div class="mx-2 px-3 py-2" style="border: dotted 2px #CCC" v-if="$vuetify.breakpoint.mdAndUp">
        <p class="mb-0 fr-text-sm font-weight-medium">
          Personnalisez votre affiche pour communiquer avec vos convives
        </p>
      </div>
      <div>
        <v-btn
          :large="$vuetify.breakpoint.smAndUp"
          color="primary"
          outlined
          class="mr-2 mb-4 mb-sm-0"
          :to="{ name: 'CanteenGeneratePoster' }"
        >
          Télécharger en .pdf
        </v-btn>
        <v-btn
          :large="$vuetify.breakpoint.smAndUp"
          :disabled="!isPublished"
          color="primary"
          :to="{
            name: 'CanteenPage',
            params: { canteenUrlComponent },
          }"
          target="_blank"
          rel="noopener external"
          title="Voir la version en ligne - ouvre une nouvelle fenêtre"
          class="mb-4 mb-sm-0"
        >
          Voir la version en ligne
          <v-icon small class="ml-1" color="white">mdi-open-in-new</v-icon>
        </v-btn>
      </div>
    </div>

    <ImagesField v-if="$vuetify.breakpoint.smAndUp" :canteen="canteen" :end="imageHeaderLimit" class="mt-0 mb-4" />
    <CanteenHeader class="my-6" :canteen="canteen" @logoChanged="(x) => (originalCanteen.logo = x)" />

    <CanteenPublication :canteen="canteen" :editable="true" />
    <div>
      <div v-if="showImagesOverflow">
        <h3>Galerie</h3>
        <ImagesField :canteen="canteen" :start="imageHeaderLimit" :end="additionalImagesMax" class="mt-0 mb-4" />
      </div>
      <DsfrAccordion v-if="isPublished" :items="[{ title: 'Ajouter un aperçu sur votre site' }]" class="my-6">
        <template v-slot:content>
          <AddPublishedCanteenWidget :canteen="canteen" />
        </template>
      </DsfrAccordion>
      <v-sheet rounded color="grey lighten-4 pa-3 my-6" class="d-flex flex-wrap align-center">
        <v-form ref="form" @submit.prevent class="publication-checkbox">
          <PublicationField :canteen="canteen" v-model="acceptPublication" />
        </v-form>
        <v-spacer v-if="$vuetify.breakpoint.smAndUp"></v-spacer>
        <v-btn
          v-if="!isPublished"
          x-large
          outlined
          color="primary"
          class="mr-4 align-self-center"
          :to="{
            name: 'DashboardManager',
            params: { canteenUrlComponent },
          }"
        >
          Annuler
        </v-btn>
        <v-btn v-if="!isPublished" x-large color="primary" @click="publishCanteen">
          Publier
        </v-btn>
        <v-btn v-else x-large color="red darken-3" class="mr-4" outlined @click="removeCanteenPublication">
          Retirer la publication
          <!-- TODO: remove options -->
        </v-btn>
      </v-sheet>
    </div>
  </div>
</template>

<script>
import PublicationField from "../PublicationField"
import { lastYear } from "@/utils"
import AddPublishedCanteenWidget from "@/components/AddPublishedCanteenWidget"
import DsfrBadge from "@/components/DsfrBadge"
import DsfrAccordion from "@/components/DsfrAccordion"
import CanteenHeader from "./CanteenHeader"
import CanteenPublication from "@/components/CanteenPublication"
import ImagesField from "./ImagesField"

export default {
  name: "PublicationForm",
  props: {
    originalCanteen: {
      type: Object,
    },
  },
  components: {
    DsfrBadge,
    PublicationField,
    AddPublishedCanteenWidget,
    CanteenHeader,
    CanteenPublication,
    ImagesField,
    DsfrAccordion,
  },
  data() {
    return {
      acceptPublication: false,
      canteen: {},
      publicationYear: lastYear(),
    }
  },
  beforeMount() {
    const canteen = this.originalCanteen
    if (canteen) {
      this.canteen = JSON.parse(JSON.stringify(canteen))
      if (!this.canteen.images) this.canteen.images = []
      this.acceptPublication = !!canteen.publicationStatus && canteen.publicationStatus !== "draft"
    }
  },
  methods: {
    publishCanteen() {
      const valid = this.$refs.form.validate()
      if (!valid) {
        this.$store.dispatch("notifyRequiredFieldsError")
        return
      }
      this.changePublicationStatus(true)
    },
    removeCanteenPublication() {
      this.changePublicationStatus(false)
    },
    changePublicationStatus(toPublish, title) {
      if (!title) {
        title = toPublish ? "Votre cantine est publiée" : "Votre cantine n'est plus publiée"
      }
      this.$store
        .dispatch(toPublish ? "publishCanteen" : "unpublishCanteen", {
          id: this.canteen.id,
          payload: this.canteen,
        })
        .then(() => {
          if (toPublish) {
            return this.$router.push({
              name: "CanteenPage",
              params: { canteenUrlComponent: this.$store.getters.getCanteenUrlComponent(this.canteen) },
            })
          } else {
            return this.$router.push({
              name: "DashboardManager",
              params: {
                canteenUrlComponent: this.canteenUrlComponent,
              },
            })
          }
        })
        .then(() => this.$store.dispatch("notify", { title, status: "success" }))
        .catch((e) => {
          this.$store.dispatch("notifyServerError", e)
        })
    },
  },
  created() {
    document.title = `Éditer mon affiche - ${this.originalCanteen.name} - ${this.$store.state.pageTitleSuffix}`
  },
  computed: {
    canteenUrlComponent() {
      return this.$store.getters.getCanteenUrlComponent(this.canteen)
    },
    isPublished() {
      return this.canteen.publicationStatus === "published"
    },
    badge() {
      return {
        true: {
          mode: "SUCCESS",
          text: "En ligne",
          icon: "mdi-circle",
        },
        false: {
          mode: "INFO",
          text: "Non publiée",
          icon: "mdi-circle-outline",
        },
      }[this.isPublished]
    },
    imageHeaderLimit() {
      return this.$vuetify.breakpoint.xs ? 0 : 3
    },
    additionalImagesMax() {
      return Math.max(this.canteen.images.length, this.imageHeaderLimit)
    },
    showImagesOverflow() {
      const allowMobileAdd = this.$vuetify.breakpoint.xs && this.canteen.images.length === 0
      const showRemainingImages = this.canteen.images.length > this.imageHeaderLimit
      return allowMobileAdd || showRemainingImages
    },
  },
}
</script>

<style scoped>
.publication-checkbox {
  min-width: 40%;
  max-width: 50%;
}
</style>
