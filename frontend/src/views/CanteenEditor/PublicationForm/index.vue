<template>
  <div class="text-left">
    <div class="d-block d-sm-flex align-center justify-space-between">
      <div class="d-flex flex-column mb-2">
        <h1 class="fr-text font-weight-bold">Mon affiche</h1>
        <div v-if="receivesGuests">
          <DsfrBadge :mode="badgeMode">
            <p class="mb-0">{{ badgeText }}</p>
          </DsfrBadge>
        </div>
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
        >
          Voir la version en ligne
          <v-icon small class="ml-1" color="white">mdi-open-in-new</v-icon>
        </v-btn>
      </div>
    </div>

    <ImagesField class="mt-0 mb-4" :canteen="canteen" />

    <CanteenHeader class="my-6" :canteen="canteen" @logoChanged="(x) => (originalCanteen.logo = x)" />

    <PublicationStateNotice v-if="receivesGuests" :canteen="originalCanteen" class="my-4" />
    <div v-if="isPublished">
      <AddPublishedCanteenWidget :canteen="originalCanteen" />
      <div v-if="!receivesGuests">
        <p class="mt-8">
          Précédemment vous aviez choisi de publier cette cantine. En tant que cuisine centrale, vous pouvez désormais
          retirer cette publication.
        </p>
        <v-sheet rounded color="grey lighten-4 pa-3 my-6" class="d-flex">
          <v-spacer></v-spacer>
          <v-btn x-large color="primary" @click="removeCanteenPublication">
            Retirer la publication
          </v-btn>
        </v-sheet>
      </div>
    </div>
    <div v-else-if="!hasDiagnostics && receivesGuests">
      <p>
        Vous n'avez pas encore rempli des diagnostics pour « {{ originalCanteen.name }} ». Les diagnostics sont un
        prérequis pour la publication
      </p>
      <v-btn
        x-large
        color="primary"
        class="mb-8"
        :to="{
          name: 'MyProgress',
          params: { canteenUrlComponent: $store.getters.getCanteenUrlComponent(originalCanteen) },
        }"
      >
        Ajouter un diagnostic
      </v-btn>
    </div>
    <p v-if="isCentralCuisine">
      <router-link :to="{ name: 'PublishSatellites' }">Gérer la publication de mes satellites</router-link>
    </p>
    <div v-if="receivesGuests">
      <h2 class="mt-8 mb-2" v-if="isPublished">Modifier la publication</h2>
      <v-form ref="form" @submit.prevent>
        <DsfrTextarea
          id="general"
          label="Décrivez si vous le souhaitez le fonctionnement, l'organisation, l'historique de votre établissement..."
          class="my-2"
          rows="5"
          counter="500"
          v-model="canteen.publicationComments"
        />
        <PublicationField class="mb-4" :canteen="canteen" v-model="acceptPublication" />
      </v-form>
      <v-sheet rounded color="grey lighten-4 pa-3 my-6" class="d-flex">
        <v-spacer></v-spacer>
        <v-btn
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
        </v-btn>
        <v-btn v-if="isPublished" x-large color="primary" @click="saveCanteen">
          Mettre à jour
        </v-btn>
      </v-sheet>
    </div>
  </div>
</template>

<script>
import PublicationField from "../PublicationField"
import { getObjectDiff, lastYear } from "@/utils"
import PublicationStateNotice from "../PublicationStateNotice"
import DsfrTextarea from "@/components/DsfrTextarea"
import AddPublishedCanteenWidget from "@/components/AddPublishedCanteenWidget"
import DsfrBadge from "@/components/DsfrBadge"
import CanteenHeader from "./CanteenHeader"
import ImagesField from "./ImagesField"

const LEAVE_WARNING = "Voulez-vous vraiment quitter cette page ? Vos changements n'ont pas été sauvegardés."

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
    PublicationStateNotice,
    DsfrTextarea,
    AddPublishedCanteenWidget,
    CanteenHeader,
    ImagesField,
  },
  data() {
    return {
      acceptPublication: false,
      canteen: {},
      bypassLeaveWarning: false,
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
    saveCanteen() {
      this.publishCanteen(true, "Votre publication est mise à jour")
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
          this.bypassLeaveWarning = true
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
    handleUnload(e) {
      if (this.hasChanged && !this.bypassLeaveWarning) {
        e.preventDefault()
        e.returnValue = LEAVE_WARNING
      } else {
        delete e["returnValue"]
      }
    },
  },
  created() {
    window.addEventListener("beforeunload", this.handleUnload)
    document.title = `Publier - ${this.originalCanteen.name} - ${this.$store.state.pageTitleSuffix}`
  },
  beforeDestroy() {
    window.removeEventListener("beforeunload", this.handleUnload)
  },
  beforeRouteLeave(to, from, next) {
    if (!this.hasChanged || this.bypassLeaveWarning) {
      next()
      return
    }
    window.confirm(LEAVE_WARNING) ? next() : next(false)
  },
  computed: {
    hasChanged() {
      const diff = getObjectDiff(this.originalCanteen, this.canteen)
      let changes = Object.keys(diff)
      const ignoreKeys = ["images", "logo"]
      changes = changes.filter((changedKey) => !ignoreKeys.includes(changedKey))
      return changes.length > 0
    },
    canteenUrlComponent() {
      return this.$store.getters.getCanteenUrlComponent(this.canteen)
    },
    isCentralCuisine() {
      return (
        this.originalCanteen.productionType === "central" || this.originalCanteen.productionType === "central_serving"
      )
    },
    receivesGuests() {
      return this.originalCanteen.productionType !== "central"
    },
    hasDiagnostics() {
      return this.originalCanteen.diagnostics && this.originalCanteen.diagnostics.length > 0
    },
    isPublished() {
      return this.canteen.publicationStatus === "published"
    },
    badgeMode() {
      return this.isPublished ? "SUCCESS" : "WARNING"
    },
    badgeText() {
      return this.isPublished ? "EN LIGNE" : "NON PUBLIÉ"
    },
  },
}
</script>
