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
        avant de publier vos données.
      </span>
    </v-alert>
    <v-form ref="form" v-model="formIsValid">
      <PublicationStateNotice :canteen="originalCanteen" class="my-4" />
      <label class="body-2" for="general">
        Décrivez si vous le souhaitez le fonctionnement, l'organisation, l'historique de votre établissement...
      </label>
      <v-textarea
        id="general"
        solo
        class="my-2"
        rows="3"
        counter="255"
        v-model="canteen.publicationComments"
        hint="Vous pouvez par exemple raconter l'histoire du lieu, du bâtiment, de l'association ou de l'entreprise ou des personnes qui gérent cet établissement, ses spécificités, ses caractéristiques techniques, logistiques... Cela peut aussi être une anecdote dont vous êtes fiers, une certification, un label..."
      ></v-textarea>
      <label class="body-2" for="quality">
        Vous avez peut-être des choses et actions à préciser sur la gestion de vos achats et de vos appros...
      </label>
      <v-textarea
        id="quality"
        solo
        class="my-2"
        rows="3"
        counter="255"
        v-model="canteen.qualityComments"
        hint="Vous pouvez par exemple détailler votre stratégie afin d'accroître la part de bio dans vos repas, évoquer vos succès dans vos démarches pour plus de qualité, ou au contraire les difficultés que vous avez rencontré; témoigner de vos actions..."
      ></v-textarea>
      <label class="body-2" for="waste">
        Vous avez peut-être des choses et actions à préciser sur vos initiatives pour réduire le gaspillage...
      </label>
      <v-textarea
        id="waste"
        solo
        class="my-2"
        rows="3"
        counter="255"
        v-model="canteen.wasteComments"
        hint="Vous avez fait l'acquisition d'une machine de pesée ou imaginé une solution innovante afin de sensibiliser vos convives sur les kg de gaspillage ? C'est le moment de le communiquer ! Vous pouvez également, si vous le souhaitez, donner des chiffres de la réduction de déchets dans votre établissement... Vous pouvez également évoquer les relations établies avec les associations de votre secteur... votre façon de valoriser les repas cuisinés mais non consommés..."
      ></v-textarea>
      <label class="body-2" for="diversification">A propos des protéines et de leur diversification...</label>
      <v-textarea
        id="diversification"
        solo
        class="my-2"
        rows="3"
        counter="255"
        v-model="canteen.diversificationComments"
        hint="Ici peut être le lieu pour évoquer quand et comment vous avez choisi de servir des repas végétariens gourmands. Peut-être donner le secret de vos recettes préférées ? Pourquoi pas nous révéler votre ingrédient sans protéines animales qui révolutionne vos menus... ?"
      ></v-textarea>
      <label class="body-2" for="plastics">Sur le plastique...</label>
      <v-textarea
        id="plastics"
        solo
        class="my-2"
        rows="3"
        counter="255"
        v-model="canteen.plasticsComments"
        hint="Même chose que pour les champs ci-dessus. Vous commencez à avoir l'habitude... :) C'est l'occasion et le lieu de nous faire rêver d'un monde sans plastique, de nous raconter vos démarches et actions afin de réduire son usage dans votre établissement..."
      ></v-textarea>
      <label class="body-2" for="information">
        Vous communiquez avec vos convives ? par quels moyens ? quelles infos ?
      </label>
      <v-textarea
        id="information"
        solo
        class="my-2"
        rows="3"
        counter="255"
        v-model="canteen.informationComments"
        hint="Réfléchir à faire de bonnes assiettes de qualité, c'est tout un art. Est-ce que vos convives ont connaissance des actions que vous menez ? Comment les sensibilisez-vous à vos part de bio, produits durables... ? Par quel biais ? Avez-vous un site internet de référence, une infolettre, des affiches sur les lieux de restauration ?"
      ></v-textarea>
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
import { getObjectDiff, isDiagnosticComplete, lastYear } from "@/utils"
import PublicationStateNotice from "./PublicationStateNotice"

const LEAVE_WARNING = "Voulez-vous vraiment quitter cette page ? Votre cantine n'a pas été sauvegardée."

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
      this.$refs.form.validate()

      if (!this.formIsValid) {
        this.$store.dispatch("notifyRequiredFieldsError")
        return
      }

      this.$store
        .dispatch(this.publicationRequested ? "publishCanteen" : "unpublishCanteen", {
          id: this.canteen.id,
          payload: this.canteen,
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
