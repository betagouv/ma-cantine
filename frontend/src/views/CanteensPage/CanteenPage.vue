<template>
  <div class="text-left">
    <div v-if="canteen" id="canteen-dashboard">
      <BreadcrumbsNav
        :links="[{ to: { name: 'CanteenSearchLanding' } }, { to: { name: 'CanteensHome' } }]"
        :title="canteen.name"
      />
      <ImageGallery :images="canteen.images.slice(0, imageLimit)" />
      <v-card elevation="0" class="pa-0 mb-8 text-left">
        <v-row class="align-center">
          <v-col
            v-if="canteen.logo"
            class="mr-4 d-none d-sm-block"
            cols="4"
            sm="3"
            md="2"
            style="border-right: solid 1px #dfdfdf;"
          >
            <v-img class="rounded" :src="canteen.logo" contain></v-img>
          </v-col>
          <v-col>
            <v-card-title class="text-h4 font-weight-black pa-0">
              <h1 class="text-h4 font-weight-black">
                {{ canteen.name }}
              </h1>
            </v-card-title>
            <v-spacer></v-spacer>
            <v-card-subtitle class="pa-0 pt-4 d-flex">
              <v-img
                v-if="canteen.logo"
                max-width="100px"
                max-height="80px"
                class="mr-4 rounded d-sm-none"
                :src="canteen.logo"
                contain
              ></v-img>
              <div>
                <CanteenIndicators :useCategories="true" :canteen="canteen" class="grey--text text--darken-3" />
                <router-link to="#contact" v-if="!canteen.canBeClaimed">
                  <v-icon small>mdi-email-outline</v-icon>
                  Contactez-nous
                </router-link>
              </div>
            </v-card-subtitle>
          </v-col>
        </v-row>
      </v-card>

      <div v-if="showClaimCanteen">
        <v-alert colored-border color="primary" elevation="2" border="left" type="success" v-if="undoSucceeded">
          Vous n'êtes plus gestionnaire de cet établissement.
        </v-alert>
        <v-alert colored-border color="primary" elevation="2" border="left" type="success" v-else-if="claimSucceeded">
          <p>
            Vous êtes maintenant gestionnaire.
            <router-link
              :to="{
                name: 'DashboardManager',
                params: {
                  canteenUrlComponent: $store.getters.getCanteenUrlComponent(canteen),
                },
              }"
            >
              Évaluez cet établissement
            </router-link>
          </p>
          <p class="mb-0">
            S'agit-il d'une erreur ?
            <v-btn @click="undoClaim" outlined color="primary" class="ml-2">
              Je ne suis pas gestionnaire de cet établissement
            </v-btn>
          </p>
        </v-alert>
        <DsfrCallout v-else>
          <div>Cet établissement n'a pas de gestionnaire associé. C'est votre établissement ?</div>
          <div v-if="loggedUser" class="mt-2">
            <v-btn @click="claimCanteen" outlined color="primary">Rejoindre cet établissement</v-btn>
          </div>
          <div v-else>
            <a :href="`/creer-mon-compte?next=${currentPage}`">Créez votre compte</a>
            ou
            <a :href="`/s-identifier?next=${currentPage}`">connectez-vous</a>
            pour le rejoindre.
          </div>
        </DsfrCallout>
      </div>

      <CanteenPublication :canteen="canteen" />

      <ContactForm id="contact" :canteen="canteen" class="mt-16" />
    </div>
    <v-progress-circular indeterminate v-else style="position: absolute; left: 50%; top: 50%"></v-progress-circular>
  </div>
</template>

<script>
import CanteenPublication from "@/components/CanteenPublication"
import ContactForm from "./ContactForm"
import CanteenIndicators from "@/components/CanteenIndicators"
import BreadcrumbsNav from "@/components/BreadcrumbsNav"
import labels from "@/data/quality-labels.json"
import DsfrCallout from "@/components/DsfrCallout"
import ImageGallery from "@/components/ImageGallery"

export default {
  data() {
    return {
      canteen: undefined,
      labels,
      canteensHomeBacklink: { name: "CanteensHome" },
      claimSucceeded: false,
      undoSucceeded: false,
      showCopySuccessMessage: false,
    }
  },
  components: {
    CanteenPublication,
    ContactForm,
    CanteenIndicators,
    BreadcrumbsNav,
    DsfrCallout,
    ImageGallery,
  },
  props: {
    canteenUrlComponent: {
      type: String,
      required: true,
    },
  },
  computed: {
    loggedUser() {
      return this.$store.state.loggedUser
    },
    showClaimCanteen() {
      return this.canteen && this.canteen.canBeClaimed
    },
    currentPage() {
      return window.location.pathname
    },
    isCanteenManager() {
      return this.canteen.isManagedByUser
    },
    imageLimit() {
      return this.$vuetify.breakpoint.xs ? 0 : 3
    },
  },
  methods: {
    setCanteen(canteen) {
      this.canteen = canteen
      if (canteen) document.title = `${this.canteen.name} - ${this.$store.state.pageTitleSuffix}`
    },
    claimCanteen() {
      const canteenId = this.canteen.id
      return this.$store
        .dispatch("claimCanteen", { canteenId })
        .then(() => (this.claimSucceeded = true))
        .catch((e) => this.$store.dispatch("notifyServerError", e))
    },
    undoClaim() {
      this.$store
        .dispatch("undoClaimCanteen", { canteenId: this.canteen.id })
        .then(() => {
          this.undoSucceeded = true
        })
        .catch(() => {
          this.undoSucceeded = false
          this.$store.dispatch("notify", {
            message:
              "Une erreur est survenue, vous pouvez réessayer plus tard ou nous contacter directement à support-egalim@beta.gouv.fr",
            status: "error",
          })
        })
    },
    loadCanteen() {
      const previousIdVersion = this.canteenUrlComponent.indexOf("--") === -1
      const id = previousIdVersion ? this.canteenUrlComponent : this.canteenUrlComponent.split("--")[0]
      return fetch(`/api/v1/publishedCanteens/${id}`)
        .then((response) => {
          if (response.status != 200) throw new Error()
          response.json().then(this.setCanteen)
        })
        .catch(() => {
          this.$router.push({ name: "CanteensHome" }).then(() => {
            this.$store.dispatch("notify", {
              message: "Nous n'avons pas trouvé cette cantine",
              status: "error",
            })
          })
        })
    },
  },
  beforeMount() {
    this.loadCanteen()
  },
  beforeRouteEnter(to, from, next) {
    next((vm) => {
      if (from.name == "CanteensHome") {
        // keep filter settings in URL params
        vm.canteensHomeBacklink = from
      }
    })
  },
  watch: {
    canteenUrlComponent() {
      this.canteen = null
      this.loadCanteen()
    },
  },
}
</script>
