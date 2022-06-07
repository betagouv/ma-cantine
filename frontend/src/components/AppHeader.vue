<template>
  <div v-if="!!this.$route.name">
    <v-app-bar
      v-mutate.attr="updateExtended"
      prominent
      elevate-on-scroll
      :elevation="showScrollShadow ? undefined : 0"
      app
      clipped-right
      color="white"
      ref="appbar"
    >
      <v-toolbar-title class="align-self-center">
        <router-link :to="{ name: 'LandingPage' }" class="text-decoration-none d-flex">
          <v-img src="/static/images/Marianne.png" height="90" contain alt="Page d'accueil ma cantine"></v-img>
        </router-link>
      </v-toolbar-title>
      <div style="height: 100%" class="d-flex flex-column">
        <v-spacer></v-spacer>
        <div>
          <span v-if="$vuetify.breakpoint.smAndUp" id="ma-cantine-header">ma cantine</span>
          <v-chip v-if="chipInfo" label outlined :color="chipInfo.color" class="font-weight-bold ml-3" small>
            {{ chipInfo.text }}
          </v-chip>
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
            <span class="d-sr-only">Menu</span>
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
    showScrollShadow() {
      const viewNames = ["LandingPage", "BlogsHome"]
      return this.$vuetify.breakpoint.name !== "xs" && viewNames.includes(this.$route.name)
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
#ma-cantine-header {
  font-size: 1.25rem;
  line-height: 1.75rem;
  font-weight: 700;
}
</style>
