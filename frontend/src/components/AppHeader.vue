<template>
  <div v-if="!!this.$route.name">
    <v-app-bar
      v-mutate.attr="updateExtended"
      prominent
      app
      clipped-right
      color="white"
      ref="appbar"
      style="padding: 0 calc((100vw - 1024px)/2);"
      id="header"
    >
      <v-toolbar-title class="align-self-center">
        <router-link :to="{ name: 'LandingPage' }" class="text-decoration-none d-flex">
          <v-img
            src="/static/images/Marianne.png"
            height="90"
            contain
            position="center left"
            alt="Page d'accueil ma cantine"
          ></v-img>
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

      <!-- <v-btn
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
      </v-menu> -->
      <template v-slot:extension v-if="$vuetify.breakpoint.mdAndUp">
        <v-divider style="position:absolute; top:0; width:100%;"></v-divider>
        <v-tabs align-with-title>
          <div v-for="(item, index) in items" :key="index">
            <v-menu v-if="item.items" rounded="0" offset-y>
              <template v-slot:activator="{ on, attrs, value }">
                <v-tab v-bind="attrs" v-on="on" class="mc-tab body-2">
                  {{ item.text }}
                  <v-icon>{{ value ? "mdi-chevron-up" : "mdi-chevron-down" }}</v-icon>
                </v-tab>
              </template>
              <v-list>
                <v-list-item v-for="(subItem, subIndex) in item.items" :key="subIndex" :to="subItem.to">
                  <v-list-item-title>{{ subItem.text }}</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>
            <v-tab v-else :to="item.to" class="mc-tab body-2">
              {{ item.text }}
            </v-tab>
          </div>
        </v-tabs>
      </template>
      <v-menu v-else-if="userDataReady" left bottom offset-y>
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
  components: { HeaderDropdownList },
  data() {
    return {
      extended: true,
      items: [
        {
          text: "Accueil",
          to: { name: "LandingPage" },
        },
        {
          text: "Gérer mes cantines",
          authenticationState: true,
          items: [
            {
              text: "Mes cantines",
              icon: "mdi-chart-bubble",
              to: { name: "ManagementPage" },
            },
            {
              text: "Mes achats",
              icon: "mdi-food-apple",
              to: { name: "PurchasesHome" },
            },
            {
              text: "Générer mon affiche",
              icon: "mdi-cloud-print-outline",
              to: { name: "GeneratePosterPage" },
            },
          ],
        },
        {
          text: "Mesures phares",
          icon: "mdi-playlist-check",
          to: { name: "KeyMeasuresHome" },
        },
        {
          text: "Communauté",
          items: [
            {
              text: "Nos cantines",
              icon: "mdi-silverware-fork-knife",
              to: { name: "CanteensHome" },
            },
            {
              text: "Notre communauté",
              icon: "mdi-account-group",
              to: { name: "CommunityPage" },
            },
            {
              text: "Blog",
              icon: "mdi-newspaper-variant-outline",
              to: { name: "BlogsHome" },
            },
            {
              text: "Statistiques régionales",
              icon: "mdi-chart-bar",
              to: { name: "PublicCanteenStatisticsPage" },
            },
          ],
        },
        // {
        //   text: "S'identifier",
        //   icon: "mdi-key",
        //   breakpoint: "smAndDown",
        //   authenticationState: false,
        //   href: "/s-identifier",
        // },
        // {
        //   text: "Créer un compte",
        //   icon: "mdi-account",
        //   breakpoint: "smAndDown",
        //   authenticationState: false,
        //   href: "/creer-mon-compte",
        // },
        // {
        //   text: "Autodiagnostic",
        //   icon: "mdi-chart-pie",
        //   authenticationState: false,
        //   to: { name: "DiagnosticPage" },
        // },
        // {
        //   text: "Générer mon affiche",
        //   icon: "mdi-cloud-print-outline",
        //   to: { name: "GeneratePosterPage" },
        // },
        // {
        //   text: "Mon compte",
        //   icon: "mdi-account",
        //   authenticationState: true,
        //   to: { name: "AccountSummaryPage" },
        // },
        // {
        //   type: "divider",
        // },
        // {
        //   text: "Documentation",
        //   icon: "mdi-file-document-outline",
        //   href: "https://ma-cantine-1.gitbook.io/ma-cantine-egalim/",
        //   target: "_blank",
        //   rel: "noopener",
        // },
        // {
        //   type: "divider",
        // },
        {
          text: "Contactez-nous",
          icon: "mdi-help-circle-outline",
          to: { name: "ContactPage" },
        },
      ],
    }
  },
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
.mc-tab {
  height: 100%;
  text-transform: none;
}
</style>
