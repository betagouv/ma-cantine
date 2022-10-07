<template>
  <div class="text-left">
    <h1 class="font-weight-black text-h4 my-4">Publier ma cantine</h1>
    <div v-if="isCentralCuisine">
      <p>
        « {{ originalCanteen.name }} » est une cuisine centrale sans lieu de consommation. La publication concerne
        <b>uniquement les lieux de restauration recevant des convives.</b>
      </p>
      <p>
        Vous pouvez
        <router-link :to="{ name: 'NewCanteen' }">ajouter une cantine satellite</router-link>
        ou indiquer que
        <router-link
          :to="{
            name: 'CanteenModification',
            params: { canteenUrlComponent: $store.getters.getCanteenUrlComponent(originalCanteen) },
          }"
        >
          votre cantine reçoit des convives sur place.
        </router-link>
      </p>
      <p v-if="publicationRequested">
        Précédemment vous aviez choisi de publier cette cantine. En tant que cuisine centrale, vous pouvez désormais
        retirer cette publication.
      </p>
      <v-sheet v-if="publicationRequested" rounded color="grey lighten-4 pa-3 my-6" class="d-flex">
        <v-spacer></v-spacer>
        <v-btn x-large color="primary" @click="removeCanteenPublication">
          Retirer la publication
        </v-btn>
      </v-sheet>
    </div>
    <div v-else-if="isDraft && !hasDiagnostics">
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
    <div v-else>
      <v-form ref="form" v-model="formIsValid">
        <PublicationStateNotice :canteen="originalCanteen" class="my-4" />
        <label class="body-2" for="general">
          Décrivez si vous le souhaitez le fonctionnement, l'organisation, l'historique de votre établissement...
        </label>
        <DsfrTextarea
          id="general"
          class="my-2"
          rows="3"
          counter="500"
          v-model="canteen.publicationComments"
          hint="Vous pouvez par exemple raconter l'histoire du lieu, du bâtiment, de l'association ou de l'entreprise ou des personnes qui gérent cet établissement, ses spécificités, ses caractéristiques techniques, logistiques... Cela peut aussi être une anecdote dont vous êtes fiers, une certification, un label..."
        />
        <PublicationField class="mb-4" :canteen="canteen" v-model="publicationRequested" />
      </v-form>
      <v-sheet rounded color="grey lighten-4 pa-3 my-6" class="d-flex">
        <v-spacer></v-spacer>
        <v-btn x-large outlined color="primary" class="mr-4 align-self-center" :to="{ name: 'ManagementPage' }">
          Annuler
        </v-btn>
        <v-btn x-large color="primary" @click="saveCanteen">
          Valider
        </v-btn>
      </v-sheet>
    </div>
  </div>
</template>

<script>
import PublicationField from "./PublicationField"
import { getObjectDiff, isDiagnosticComplete, lastYear } from "@/utils"
import PublicationStateNotice from "./PublicationStateNotice"
import DsfrTextarea from "@/components/DsfrTextarea"

const LEAVE_WARNING = "Voulez-vous vraiment quitter cette page ? Votre cantine n'a pas été sauvegardée."

export default {
  name: "PublicationForm",
  props: {
    originalCanteen: {
      type: Object,
    },
  },
  components: { PublicationField, PublicationStateNotice, DsfrTextarea },
  data() {
    return {
      formIsValid: true,
      publicationRequested: false,
      canteen: {},
      bypassLeaveWarning: false,
      publicationYear: lastYear(),
    }
  },
  beforeMount() {
    const canteen = this.originalCanteen
    if (canteen) {
      this.canteen = JSON.parse(JSON.stringify(canteen))
      this.publicationRequested = !!canteen.publicationStatus && canteen.publicationStatus !== "draft"
    }
  },
  methods: {
    saveCanteen() {
      if (this.$refs.form) {
        this.$refs.form.validate()

        if (!this.formIsValid) {
          this.$store.dispatch("notifyRequiredFieldsError")
          return
        }
      }
      const title = this.publicationRequested ? "Votre cantine est publiée" : "Votre cantine n'est plus publiée"
      this.$store
        .dispatch(this.publicationRequested ? "publishCanteen" : "unpublishCanteen", {
          id: this.canteen.id,
          payload: this.canteen,
        })
        .then(() => {
          this.$store.dispatch("notify", { title, status: "success" })
          this.bypassLeaveWarning = true
          this.$router.push({ name: "ManagementPage" })
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
    removeCanteenPublication() {
      this.publicationRequested = false
      this.saveCanteen()
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
      const publicationRequested =
        this.publicationRequested &&
        (this.originalCanteen.publicationStatus === "draft" || !this.originalCanteen.publicationStatus)
      const unpublicationRequested =
        !this.publicationRequested &&
        !!this.originalCanteen.publicationRequested &&
        this.originalCanteen.publicationRequested !== "draft"
      if (publicationRequested || unpublicationRequested) {
        return true
      }
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
      return this.originalCanteen.productionType === "central"
    },
    hasDiagnostics() {
      return this.originalCanteen.diagnostics && this.originalCanteen.diagnostics.length > 0
    },
    isDraft() {
      return this.canteen.publicationStatus === "draft"
    },
  },
}
</script>
