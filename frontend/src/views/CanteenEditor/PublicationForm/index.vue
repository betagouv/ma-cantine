<template>
  <div class="text-left">
    <h1 class="font-weight-black text-h4 my-4">{{ pageTitle }}</h1>
    <PublicationStateNotice v-if="receivesGuests" :canteen="originalCanteen" class="my-4" />
    <div v-if="isPublished">
      <p>
        <v-icon color="green">$checkbox-circle-fill</v-icon>
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
      </p>
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
        class="mt-4"
        :to="{
          name: 'NewDiagnosticForCanteen',
          params: { canteenUrlComponent: $store.getters.getCanteenUrlComponent(originalCanteen) },
        }"
      >
        Ajouter un diagnostic
      </v-btn>
    </div>
    <div v-if="receivesGuests">
      <h2 class="mt-8 mb-2" v-if="isPublished">Modifier la publication</h2>
      <v-form ref="form" @submit.prevent>
        <label for="general">
          Décrivez si vous le souhaitez le fonctionnement, l'organisation, l'historique de votre établissement...
          <br />
          <span class="caption grey--text text--darken-1">
            Vous pouvez par exemple raconter l'histoire du lieu, du bâtiment, de l'association ou de l'entreprise ou des
            personnes qui gérent cet établissement, ses spécificités, ses caractéristiques techniques, logistiques...
            Cela peut aussi être une anecdote dont vous êtes fiers, une certification, un label...
          </span>
        </label>
        <DsfrTextarea id="general" class="my-2" rows="5" counter="500" v-model="canteen.publicationComments" />
        <PublicationField class="mb-4" :canteen="canteen" v-model="acceptPublication" />
      </v-form>
      <v-sheet rounded color="grey lighten-4 pa-3 my-6" class="d-flex">
        <v-spacer></v-spacer>
        <v-btn x-large outlined color="primary" class="mr-4 align-self-center" :to="{ name: 'ManagementPage' }">
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
import { getObjectDiff, isDiagnosticComplete, lastYear } from "@/utils"
import PublicationStateNotice from "../PublicationStateNotice"
import DsfrTextarea from "@/components/DsfrTextarea"
import AddPublishedCanteenWidget from "@/components/AddPublishedCanteenWidget"

const LEAVE_WARNING = "Voulez-vous vraiment quitter cette page ? Vos changements n'ont pas été sauvegardés."

export default {
  name: "PublicationForm",
  props: {
    originalCanteen: {
      type: Object,
    },
  },
  components: { PublicationField, PublicationStateNotice, DsfrTextarea, AddPublishedCanteenWidget },
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
          this.$store.dispatch("notify", { title, status: "success" })
          this.bypassLeaveWarning = true
          if (toPublish) {
            this.$router.push({
              name: "CanteenPage",
              params: { canteenUrlComponent: this.$store.getters.getCanteenUrlComponent(this.canteen) },
            })
          } else {
            this.$router.push({ name: "ManagementPage" })
          }
        })
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
    pageTitle() {
      if (this.isPublished) {
        return "Votre publication"
      } else {
        return "Publier votre lieu de service"
      }
    },
    hasChanged() {
      const diff = getObjectDiff(this.originalCanteen, this.canteen)
      return Object.keys(diff).length > 0
    },
    currentDiagnosticComplete() {
      const diagnostic = this.originalCanteen.diagnostics.find((x) => x.year === this.publicationYear)
      return !!diagnostic && isDiagnosticComplete(diagnostic)
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
  },
}
</script>
