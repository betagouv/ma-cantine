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

    <div v-if="canteenCount === 0" class="body-2 font-weight-medium">
      <p class="mb-0">
        Prenez connaissance du
        <v-btn
          text
          href="https://1648047458-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F-MSCF7Mdc8yfeIjMxMZr%2Fuploads%2FlNPOtFoTKyfj5UnjZKJj%2FEGAlim%20Bilan%20statistique%202023%20d%C3%A9finitif.pdf?alt=media"
          target="_blank"
          rel="noopener external"
          title="bilan EGAlim pour la campagne de 2022 - ouvre une nouvelle fenêtre"
          class="text-decoration-underline px-0"
          style="margin-top: -5px"
        >
          bilan EGAlim pour la campagne de 2022
          <v-icon small class="ml-2">mdi-open-in-new</v-icon>
        </v-btn>
      </p>
    </div>
    <div v-if="canteenCount > 0" class="mt-4">
      <SuccessBanner v-if="showSuccessBanner" />
      <TeledeclarationBanner v-else-if="teledeclarationCampaignActive && !correctionCampaignActive" />
      <ActionsBanner v-else />
    </div>
    <div class="mt-4">
      <h2 class="my-4 text-h5 font-weight-black">Mes cantines</h2>
      <CanteensPagination v-on:canteen-count="canteenCount = $event" />
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
import UserTools from "./UserTools"
import TeledeclarationBanner from "./TeledeclarationBanner"
import CanteenCreationDialog from "./CanteenCreationDialog"
import ActionsBanner from "./ActionsBanner"
import SuccessBanner from "./SuccessBanner"
import validators from "@/validators"
import { lastYear } from "@/utils"

export default {
  name: "ManagementPage",
  components: {
    CanteensPagination,
    UserTools,
    PageSatisfaction,
    TeledeclarationBanner,
    ActionsBanner,
    SuccessBanner,
    CanteenCreationDialog,
  },
  data() {
    return {
      validators,
      canteenCount: undefined,
      hasActions: false,
      showCanteenCreationPrompt: null,
      teledeclarationCampaignActive: window.ENABLE_TELEDECLARATION,
      correctionCampaignActive: window.TELEDECLARATION_CORRECTION_CAMPAIGN,
      actionsLoading: true,
      resources: [
        {
          title: "Les 5 points essentiels à connaître sur la loi EGAlim en restauration collective",
          text:
            "Les mesures pour la restauration collective de la loi EGAlim en restauration collective sont un volet important dans l’ensemble de la loi EGAlim. Celles-ci ont vocation à...",
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
    }
  },
  computed: {
    loggedUser() {
      return this.$store.state.loggedUser
    },
    showSuccessBanner() {
      return !this.actionsLoading && !this.hasActions
    },
  },
  mounted() {
    return fetch(`/api/v1/actionableCanteens/${lastYear()}?limit=1&offset=0`)
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
    },
  },
}
</script>
