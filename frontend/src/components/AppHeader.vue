<template>
  <div v-if="!!this.$route.name">
    <v-app-bar
      v-mutate.attr="updateExtended"
      :shrink-on-scroll="dynamicSizingEnabled"
      :prominent="dynamicSizingEnabled"
      :short="dynamicSizingEnabled"
      :elevate-on-scroll="elevateOnScroll"
      :elevation="elevateOnScroll ? undefined : 0"
      app
      clipped-right
      color="white"
      ref="appbar"
    >
      <v-toolbar-title class="align-self-center">
        <router-link :to="{ name: 'LandingPage' }" class="text-decoration-none d-flex">
          <v-img :src="`/static/images/${imageFilename}`" :width="imageWidth" alt="Page d'accueil ma cantine"></v-img>
        </router-link>
      </v-toolbar-title>
      <div style="height: 100%" class="d-flex flex-column">
        <v-spacer></v-spacer>
        <v-chip v-if="chipInfo" label outlined :color="chipInfo.color" class="font-weight-bold ml-3" small>
          {{ chipInfo.text }}
        </v-chip>
        <v-spacer></v-spacer>
      </div>

      <div class="ml-6 mr-4 fill-height d-flex flex-column" v-if="$vuetify.breakpoint.mdAndUp && !this.loggedUser">
        <v-spacer></v-spacer>
        <div class="divider"></div>
        <v-spacer></v-spacer>
      </div>

      <div
        class="fill-height d-flex flex-column text-left"
        v-if="!loggedUser && userDataReady && $vuetify.breakpoint.smAndUp"
      >
        <v-spacer></v-spacer>
        <div class="caption grey--text ml-0 ml-md-n2">
          <v-btn
            text
            class="align-self-center mt-n1"
            v-if="!loggedUser && userDataReady && $vuetify.breakpoint.smAndUp"
            href="https://calendly.com/jennifer-stephan-betagouv/ma-cantine-aide-info-a-la-connexion-l-inscription-la-creation-de-cantine"
            target="_blank"
            rel="noopener"
          >
            <span>Demander une démo</span>
          </v-btn>
        </div>
        <v-spacer></v-spacer>
      </div>

      <v-spacer></v-spacer>

      <v-btn
        text
        elevation="0"
        class="align-self-center header-login-button ml-2"
        v-if="!loggedUser && userDataReady && $vuetify.breakpoint.mdAndUp"
        href="/s-identifier"
      >
        <span>S'identifier</span>
      </v-btn>

      <v-btn
        text
        elevation="0"
        v-if="!loggedUser && userDataReady && $vuetify.breakpoint.mdAndUp"
        href="/creer-mon-compte"
        class="d-none d-sm-flex align-self-center header-signup-button"
      >
        <span>Créer mon compte</span>
      </v-btn>

      <v-menu v-if="userDataReady" left bottom offset-y>
        <template v-slot:activator="{ on }">
          <v-btn v-if="loggedUser" class="mr-2 ml-2 align-self-center" id="profile" plain v-on="on">
            <v-avatar size="36" class="mr-2 pt-1" v-if="loggedUser && loggedUser.avatar">
              <v-img :src="loggedUser.avatar"></v-img>
            </v-avatar>
            <v-icon v-else>mdi-account</v-icon>
            <span class="font-subtitle-3 mx-2 d-none d-sm-inline">Profil</span>
            <v-icon class="ml-1 pt-1" small>mdi-menu-down</v-icon>
          </v-btn>

          <v-btn v-else icon class="mr-2 ml-2 align-self-center" v-on="on">
            <v-icon>mdi-menu</v-icon>
          </v-btn>
        </template>

        <HeaderDropdownList />
      </v-menu>
    </v-app-bar>
  </div>
</template>

<script>
import HeaderDropdownList from "@/components/HeaderDropdownList"

export default {
  name: "AppHeader",
  data() {
    return {
      extended: true,
    }
  },
  components: { HeaderDropdownList },
  computed: {
    loggedUser() {
      return this.$store.state.loggedUser
    },
    userDataReady() {
      return !!this.$store.state.initialDataLoaded
    },
    useLargeImage() {
      return !this.$vuetify.breakpoint.xs && this.extended && this.dynamicSizingEnabled
    },
    imageFilename() {
      return this.useLargeImage ? "header-logos-extended.png" : "header-logos-compact.svg"
    },
    imageWidth() {
      return this.useLargeImage ? "300" : "210"
    },
    dynamicSizingEnabled() {
      const viewNames = ["LandingPage", "BlogsHome"]
      return this.$vuetify.breakpoint.name !== "xs" && viewNames.includes(this.$route.name)
    },
    elevateOnScroll() {
      return this.dynamicSizingEnabled
    },
    chipInfo() {
      const env = window.ENVIRONMENT
      if (env === "dev") return { text: "Dev", color: "pink" }
      if (env === "staging") return { text: "Staging", color: "purple" }
      if (env === "demo") return { text: "Démo", color: "green darken-2" }
      return null
    },
  },
  methods: {
    updateExtended() {
      this.extended = this.$refs && this.$refs.appbar && !this.$refs.appbar.classes["v-app-bar--is-scrolled"]
    },
  },
}
</script>

<style scoped lang="scss">
.v-application header.elevation-0 {
  box-shadow: inset 0px -1px 0px rgba(178, 181, 194, 0.48) !important;
}
#profile::v-deep .v-btn__content {
  opacity: 1;
}
.divider {
  height: 60%;
  max-height: 30px;
  border-left: solid 1px #ccc;
}
</style>
