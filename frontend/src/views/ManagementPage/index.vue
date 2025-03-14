<template>
  <div class="text-left">
    <h1
      class="mt-4 mb-2 text-h6 font-weight-black"
      :style="$vuetify.breakpoint.mdAndUp ? 'font-size: 2rem !important;' : ''"
    >
      Bienvenue dans votre espace, {{ loggedUser.firstName }}
    </h1>

    <router-link class="fr-text-xs d-flex align-center" :to="{ name: 'AccountEditor' }">
      Modifier mon profil
      <v-icon class="ml-1" color="primary" x-small>mdi-pencil</v-icon>
    </router-link>

    <p v-if="loggedUser.isElectedOfficial" class="mt-2 mb-0">
      Vous avez un compte élu / élue, voir
      <router-link text :to="{ name: 'TerritoryCanteens' }">
        les cantines de votre territoire
      </router-link>
    </p>
    <InformationBanner v-if="showInformationBanner" />
    <div v-if="canteenCount > 0" class="mt-4">
      <SuccessBanner v-if="showSuccessBanner" />
      <ActionsBanner v-else />
    </div>
    <div class="mt-4">
      <v-row class="justify-space-between">
        <v-col>
          <h2 class="my-4 text-h5 font-weight-black">Mes cantines</h2>
        </v-col>
        <v-col class="flex-shrink-1 flex-grow-0">
          <DsfrSegmentedControl
            v-model="viewStyle"
            legend="Vue"
            :noLegend="true"
            :items="viewStyles"
            @input="updatePreference"
          />
        </v-col>
      </v-row>
      <div v-if="showListView">
        <p>Actions en attente en {{ year }}</p>
        <AnnualActionableCanteensTable v-on:canteen-count="canteenCount = $event" />
        <v-btn large color="primary" outlined :to="{ name: 'CanteenCreation' }">
          <v-icon class="mr-2">mdi-plus</v-icon>
          Ajouter une cantine
        </v-btn>
        <v-btn large text color="primary" :to="{ name: 'ImportCanteens' }">
          <v-icon class="mr-2">mdi-file-upload-outline</v-icon>
          Créer plusieurs cantines depuis un fichier
        </v-btn>
      </div>
      <CanteensPagination v-else v-on:canteen-count="canteenCount = $event" />
    </div>
    <PageSatisfaction v-if="canteenCount" class="my-12" />
    <div class="mt-12 mb-8" v-if="canteenCount > 0">
      <h2 class="text-h5 font-weight-black mb-4">Mes outils</h2>
      <UserTools />
    </div>
    <div class="mt-12 mb-8" v-else>
      <h2 class="text-h5 font-weight-black mb-4">Quelques outils pour commencer</h2>
      <v-row>
        <v-col cols="12" sm="6" v-for="(resource, idx) in resources" :key="idx">
          <v-card outlined class="d-flex flex-column fill-height pa-4" :style="resource.style">
            <v-card-title class="font-weight-bold" v-html="resource.title"></v-card-title>
            <v-card-text>
              <p class="mb-0">{{ resource.text }}</p>
            </v-card-text>
            <v-spacer></v-spacer>
            <v-card-actions class="px-4 justify-end">
              <v-btn text color="primary" :to="resource.links[1].to" v-if="resource.links[1]">
                {{ resource.links[1].text }}
              </v-btn>
              <v-btn outlined color="primary" :to="resource.links[0].to" :href="resource.links[0].href">
                {{ resource.links[0].text }}
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </div>
    <CanteenCreationDialog
      v-if="showCanteenCreationPrompt !== null"
      :organizations="loggedUser.mcpOrganizations"
      v-model="showCanteenCreationPrompt"
    />
  </div>
</template>

<script>
import CanteensPagination from "./CanteensPagination.vue"
import PageSatisfaction from "@/components/PageSatisfaction.vue"
import DsfrSegmentedControl from "@/components/DsfrSegmentedControl"
import UserTools from "./UserTools"
import InformationBanner from "./InformationBanner"
import CanteenCreationDialog from "./CanteenCreationDialog"
import ActionsBanner from "./ActionsBanner"
import SuccessBanner from "./SuccessBanner"
import validators from "@/validators"
import { lastYear } from "@/utils"
import AnnualActionableCanteensTable from "@/components/AnnualActionableCanteensTable"
import { readManagerCanteenViewPreference, updateManagerCanteenViewPreference } from "@/utils"

const LIST_VIEW = "list"
const CARD_VIEW_DEFAULT_THRESHOLD = 5 // la pagination de cartes est à partir de 5 cantines

export default {
  name: "ManagementPage",
  components: {
    CanteensPagination,
    UserTools,
    PageSatisfaction,
    InformationBanner,
    ActionsBanner,
    SuccessBanner,
    CanteenCreationDialog,
    DsfrSegmentedControl,
    AnnualActionableCanteensTable,
  },
  data() {
    return {
      validators,
      canteenCount: undefined,
      hasActions: false,
      showCanteenCreationPrompt: null,
      actionsLoading: true,
      resources: [
        {
          title: "Les 5 points essentiels à connaître sur la loi EGalim en restauration collective",
          text:
            "Les mesures pour la restauration collective de la loi EGalim en restauration collective sont un volet important dans l’ensemble de la loi EGalim. Celles-ci ont vocation à...",
          links: [
            {
              text: "Découvrir",
              href: "https://ma-cantine.agriculture.gouv.fr/blog/25",
            },
            {
              text: "Voir tous les articles",
              to: { name: "BlogsHome" },
            },
          ],
        },
        {
          title: "Comment utiliser la plateforme «&nbsp;ma cantine&nbsp;» ?",
          text:
            "Comment créer une cantine sur la plateforme ? Quelles sont mes obligations ? Trouver ces réponses dans nos webinaires enregistrés.",
          links: [
            {
              text: "Découvrir les webinaires",
              to: {
                name: "CommunityPage",
              },
            },
          ],
        },
        {
          title: "SOS",
          text: "Vous avez besoin d'aide sur plusieurs aspects techniques ou légaux ?",
          links: [
            {
              text: "Consulter la FAQ",
              to: {
                name: "FaqPage",
              },
            },
            {
              text: "Nous contacter",
              to: {
                name: "ContactPage",
              },
            },
          ],
          style: "background-color: #E8EDFF; border: none;", // light / background / contrast-info
        },
      ],
      showInformationBanner: window.SHOW_MANAGEMENT_INFORMATION_BANNER,
      viewStyles: [
        {
          text: "Vue cartes",
          icon: "$layout-grid-fill",
          value: "card",
        },
        {
          text: "Vue liste",
          icon: "$list-check",
          value: LIST_VIEW,
        },
      ],
      viewStyle: readManagerCanteenViewPreference(),
      year: lastYear(),
    }
  },
  computed: {
    loggedUser() {
      return this.$store.state.loggedUser
    },
    showSuccessBanner() {
      return !this.actionsLoading && !this.hasActions
    },
    showListView() {
      return this.viewStyle === LIST_VIEW
    },
  },
  methods: {
    updatePreference() {
      updateManagerCanteenViewPreference(this.viewStyle)
    },
  },
  mounted() {
    return fetch(`/api/v1/actionableCanteens/${this.year}?limit=1&offset=0`)
      .then((response) => {
        if (response.status < 200 || response.status >= 400) throw new Error(`Error encountered : ${response}`)
        return response.json()
      })
      .then((response) => (this.hasActions = response.hasPendingActions))
      .catch(() => (this.hasActions = true))
      .finally(() => (this.actionsLoading = false))
  },
  watch: {
    canteenCount(count) {
      if (this.loggedUser.mcpOrganizations && count === 0 && this.showCanteenCreationPrompt === null) {
        this.showCanteenCreationPrompt = true
      }
      if (count > CARD_VIEW_DEFAULT_THRESHOLD && !readManagerCanteenViewPreference()) {
        this.viewStyle = LIST_VIEW
      }
    },
  },
}
</script>
