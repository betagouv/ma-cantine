<template>
  <div class="text-left">
    <div class="mt-4 mb-0 mb-md-6">
      <p
        class="my-2 text-h6 font-weight-black"
        :style="$vuetify.breakpoint.mdAndUp ? 'font-size: 2rem !important;' : ''"
      >
        Bienvenue dans votre espace, {{ loggedUser.firstName }}
        <v-btn text class="text-decoration-underline text-caption mb-1 mb-md-n1" :to="{ name: 'AccountEditor' }">
          <v-icon class="mr-1" small>mdi-pencil</v-icon>
          Modifier mon profil
        </v-btn>
      </p>
      <CanteenCreationDialog
        v-if="showCanteenCreationPrompt !== null"
        :organizations="loggedUser.mcpOrganizations"
        v-model="showCanteenCreationPrompt"
      />
    </div>
    <TeledeclarationBanner v-if="showPendingTeledeclarationBanner" />
    <ActionsBanner v-else-if="showActionsBanner" />
    <SuccessBanner v-else-if="showSuccessBanner" />
    <div class="mt-4">
      <h1 class="my-4 text-h5 font-weight-black">Mes cantines</h1>
      <CanteensPagination v-on:canteen-count="canteenCount = $event" />
    </div>
    <PageSatisfaction v-if="canteenCount" class="my-12" />
    <div class="mt-12 mb-8">
      <h2 class="text-h5 font-weight-black mb-4">Mes outils</h2>
      <UserTools />
    </div>
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
    }
  },
  computed: {
    loggedUser() {
      return this.$store.state.loggedUser
    },
    showActionsBanner() {
      return this.canteenCount > 0 && this.hasActions && !this.showTeledeclarationBanner
    },
    showPendingTeledeclarationBanner() {
      return this.canteenCount > 0 && this.hasActions && this.showTeledeclarationBanner
    },
    showSuccessBanner() {
      return this.canteenCount > 0 && !this.hasActions
    },
  },
  mounted() {
    return fetch(`/api/v1/actionableCanteens/${lastYear()}`)
      .then((response) => {
        if (response.status < 200 || response.status >= 400) throw new Error(`Error encountered : ${response}`)
        return response.json()
      })
      .then((response) => (this.hasActions = response.count > 0))
      .catch(() => (this.hasActions = true))
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
