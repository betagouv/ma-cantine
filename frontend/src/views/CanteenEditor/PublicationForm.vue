<template>
  <div class="text-left">
    <h1 class="font-weight-black text-h4 my-4">Publier ma cantine</h1>
    <v-alert color="amber darken-3" class="mb-1 body-2" v-if="!currentDiagnosticComplete" outlined>
      <span class="grey--text text--darken-2">
        <v-icon class="mb-1 mr-2" color="amber darken-3">mdi-alert-circle-outline</v-icon>
        Nous vous conseillons de remplir des
        <router-link :to="{ name: 'DiagnosticList', params: { canteenUrlComponent } }">
          données d'approvisionnement pour l'année {{ this.publicationYear }}
        </router-link>
        avant que vous publiiez vos données.
      </span>
    </v-alert>
    <v-form ref="form" v-model="formIsValid">
      <PublicationStateNotice :canteen="originalCanteen" />
      <p class="body-2 my-2">
        Décrivez si vous le souhaitez le fonctionnement, l'organisation, l'historique de votre établissement...
      </p>
      <v-textarea
        solo
        rows="3"
        counter="255"
        v-model="canteen.publicationComments"
        hint="Vous pouvez par exemple raconter l'histoire du lieu, du bâtiment, de l'association ou de l'entreprise ou des personnes qui gérent cet établissement, ses spécificités, ses caractéristiques techniques, logistiques... Cela peut aussi être une anecdote dont vous êtes fiers, une certification, un label..."
      ></v-textarea>
      <p class="body-2 my-2">
        Vous avez peut-être des choses et actions à préciser sur la gestion de vos achats et de vos appros...
      </p>
      <v-textarea
        solo
        rows="3"
        counter="255"
        v-model="canteen.qualityComments"
        hint="Vous pouvez par exemple détailler votre stratégie afin d'accroître la part de bio dans vos repas, évoquer vos succès dans vos démarches pour plus de qualité, ou au contraire les difficultés que vous avez rencontré; témoigner de vos actions..."
      ></v-textarea>
      <p class="body-2 my-2">
        Vous avez peut-être des choses et actions à préciser sur vos initiatives pour réduire le gaspillage...
      </p>
      <v-textarea
        solo
        rows="3"
        counter="255"
        v-model="canteen.wasteComments"
        hint="Vous avez fait l'acquisition d'une machine de pesée ou imaginé une solution innovante afin de sensibiliser vos convives sur les kg de gaspillage ? C'est le moment de le communiquer ! Vous pouvez également, si vous le souhaitez, donner des chiffres de la réduction de déchets dans votre établissement... Vous pouvez également évoquer les relations établies avec les associations de votre secteur... votre façon de valoriser les repas cuisinés mais non consommés..."
      ></v-textarea>
      <p class="body-2 my-2">A propos des protéines et de leur diversification...</p>
      <v-textarea
        solo
        rows="3"
        counter="255"
        v-model="canteen.diversificationComments"
        hint="Ici peut être le lieu pour évoquer quand et comment vous avez choisi de servir des repas végétariens gourmands. Peut-être donner le secret de vos recettes préférées ? Pourquoi pas nous révéler votre ingrédient sans protéines animales qui révolutionne vos menus... ?"
      ></v-textarea>
      <p class="body-2 my-2">Sur le plastique...</p>
      <v-textarea
        solo
        rows="3"
        counter="255"
        v-model="canteen.plasticsComments"
        hint="Même chose que pour les champs ci-dessus. Vous commencez à avoir l'habitude... :) C'est l'occasion et le lieu de nous faire rêver d'un monde sans plastique, de nous raconter vos démarches et actions afin de réduire son usage dans votre établissement..."
      ></v-textarea>
      <p class="body-2 my-2">Information</p>
      <v-textarea solo rows="3" counter="255" v-model="canteen.informationComments"></v-textarea>
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
</template>

<script>
import PublicationField from "./PublicationField"
import { getObjectDiff, isDiagnosticComplete } from "@/utils"
import PublicationStateNotice from "./PublicationStateNotice"

const LEAVE_WARNING = "Êtes-vous sûr de vouloir quitter cette page ? Votre cantine n'a pas été sauvegardée."

export default {
  name: "PublicationForm",
  props: {
    originalCanteen: {
      type: Object,
    },
  },
  components: { PublicationField, PublicationStateNotice },
  data() {
    return {
      formIsValid: true,
      publicationRequested: false,
      canteen: {},
      bypassLeaveWarning: false,
      publicationYear: 2020,
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
      this.$refs.form.validate()

      if (!this.formIsValid) {
        this.$store.dispatch("notifyRequiredFieldsError")
        return
      }

      if (!this.publicationRequested) {
        this.canteen.publicationStatus = "draft"
      } else if (this.canteen.publicationStatus === "draft") {
        this.canteen.publicationStatus = "pending"
      }
      const payload = this.originalCanteen ? getObjectDiff(this.originalCanteen, this.canteen) : this.canteen
      this.$store
        .dispatch("publishCanteen", {
          id: this.canteen.id,
          payload,
        })
        .then(() => {
          this.$store.dispatch("notify", {
            title: "Mise à jour prise en compte",
            message: `Votre cantine a bien été modifiée`,
            status: "success",
          })
          this.bypassLeaveWarning = true
          this.$router.push({ name: "ManagementPage" })
        })
        .catch(() => {
          this.$store.dispatch("notifyServerError")
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
    document.title = `Publier - ${this.originalCanteen.name} - ma-cantine.beta.gouv.fr`
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
        console.log("publication change")
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
  },
}
</script>
