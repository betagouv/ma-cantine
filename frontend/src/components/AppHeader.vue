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

      <div class="mx-4 fill-height d-flex flex-column" v-if="$vuetify.breakpoint.smAndUp && !this.loggedUser">
        <v-spacer></v-spacer>
        <div class="divider"></div>
        <v-spacer></v-spacer>
      </div>

      <div class="fill-height d-flex flex-column text-left" v-if="$vuetify.breakpoint.smAndUp && !this.loggedUser">
        <v-spacer></v-spacer>
        <div class="caption grey--text mt-n1" v-if="extended && dynamicSizingEnabled">
          Site en expérimentation
        </div>
        <router-link
          :to="{ name: 'TesterParticipation' }"
          class="text-caption grey--text text--darken-4 text-decoration-underline"
        >
          Devenir testeur
        </router-link>
        <v-spacer></v-spacer>
      </div>

      <v-spacer></v-spacer>

      <v-btn
        text
        elevation="0"
        class="align-self-center header-login-button"
        v-if="!loggedUser && userDataReady && $vuetify.breakpoint.mdAndUp"
        href="/s-identifier"
        active-class="header-nav-active"
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
        <span>Créer un compte</span>
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
