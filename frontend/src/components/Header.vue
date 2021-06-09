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
      <v-app-bar-title class="align-self-center">
        <router-link :to="{ name: 'LandingPage' }" class="text-decoration-none d-flex">
          <!-- All three widths are needed because of a Firefox display bug -->
          <v-img
            :class="{ 'ml-4': $vuetify.breakpoint.xs }"
            :width="extended && dynamicSizingEnabled ? 130 : 87"
            :max-width="extended && dynamicSizingEnabled ? 130 : 87"
            :min-width="extended && dynamicSizingEnabled ? 130 : 87"
            contain
            :src="`/static/images/${marianneFilename}`"
          ></v-img>
          <v-img
            :width="extended && dynamicSizingEnabled ? 135 : 114"
            :min-width="extended && dynamicSizingEnabled ? 135 : 114"
            :max-width="extended && dynamicSizingEnabled ? 135 : 114"
            contain
            :class="{ 'ml-4': $vuetify.breakpoint.xs }"
            src="/static/images/logo_transparent.png"
          ></v-img>
        </router-link>
      </v-app-bar-title>

      <div class="mx-4 fill-height d-flex flex-column">
        <v-spacer></v-spacer>
        <div class="divider"></div>
        <v-spacer></v-spacer>
      </div>

      <div class="fill-height d-flex flex-column text-left">
        <v-spacer></v-spacer>
        <div class="caption grey--text mt-n1" v-if="extended && dynamicSizingEnabled">Site en expérimentation</div>
        <a class="text-caption grey--text text--darken-4 text-decoration-underline">Devenir testeur</a>
        <v-spacer></v-spacer>
      </div>

      <v-spacer v-if="$vuetify.breakpoint.name != 'xs'"></v-spacer>

      <v-btn
        text
        elevation="0"
        class="align-self-center header-login-button"
        v-if="!loggedUser && userDataReady"
        href="/s-identifier"
        active-class="header-nav-active"
      >
        <span>S'identifier</span>
      </v-btn>

      <v-btn
        text
        elevation="0"
        v-if="!loggedUser && userDataReady"
        href="/creer-mon-compte"
        class="d-none d-sm-flex align-self-center header-signup-button"
      >
        <span>Créer un compte</span>
      </v-btn>

      <v-menu v-if="loggedUser && userDataReady" left bottom offset-y open-on-hover>
        <template v-slot:activator="{ on }">
          <v-btn class="mr-2 ml-2 align-self-center" id="profile" plain v-on="on">
            <v-avatar size="36" class="mr-2 pt-1" v-if="loggedUser && loggedUser.avatar">
              <v-img :src="loggedUser.avatar"></v-img>
            </v-avatar>
            <v-icon v-else>mdi-account</v-icon>
            <span class="font-subtitle-3 mx-2 d-none d-sm-inline">Profil</span>
            <v-icon class="ml-1 pt-1" small>mdi-menu-down</v-icon>
          </v-btn>
        </template>

        <v-list rounded>
          <v-list-item-group active-class="menu-item--active">
            <v-list-item :ripple="false" :to="{ name: 'AccountSummaryPage' }">
              <v-list-item-title class="body-2">Mon compte</v-list-item-title>
            </v-list-item>
            <v-list-item :ripple="false" :to="{ name: 'CanteenInfo' }">
              <v-list-item-title class="body-2">Publier</v-list-item-title>
            </v-list-item>
            <v-list-item :ripple="false" href="mailto:contact@egalim.beta.gouv.fr" target="_blank">
              <v-list-item-title class="body-2">Donner son avis</v-list-item-title>
            </v-list-item>
            <v-list-item :ripple="false" href="/se-deconnecter">
              <v-list-item-title class="body-2">Fermer ma session</v-list-item-title>
            </v-list-item>
          </v-list-item-group>
        </v-list>
      </v-menu>
    </v-app-bar>
  </div>
</template>

<script>
export default {
  name: "Header",
  data() {
    return {
      extended: true,
    }
  },
  computed: {
    loggedUser() {
      return this.$store.state.loggedUser
    },
    userDataReady() {
      return !!this.$store.state.initialDataLoaded
    },
    marianneFilename() {
      return this.extended && this.dynamicSizingEnabled ? "Marianne.png" : "Marianne-logo.svg"
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
.beta-chip {
  align-items: center;
  width: 51px;
  height: 72px;
  outline: none;
  overflow: hidden;
  position: relative;
  vertical-align: middle;
  white-space: nowrap;
  font-weight: 700;
  font-size: 13px;
}
.beta-chip--little {
  margin-top: -10px;
}
.v-application header.elevation-0 {
  box-shadow: inset 0px -1px 0px rgba(178, 181, 194, 0.48) !important;
}
.v-list--rounded .v-list-item,
.v-list--rounded .v-list-item::before,
.v-list--rounded .v-list-item > .v-ripple__container {
  border-radius: 12px !important;
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
