<template>
  <div v-if="!!this.$route.name">
    <v-app-bar
      v-mutate.attr="updateExtended"
      app
      clipped-right
      color="white"
      ref="appbar"
      style="padding: 0 calc((100vw - 78rem)/2);"
      height="116px"
      extension-height="56px"
      id="header"
      hide-on-scroll
    >
      <v-toolbar-title class="align-self-center">
        <router-link :to="{ name: 'LandingPage' }" class="text-decoration-none d-flex pl-4">
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

      <v-btn
        text
        elevation="0"
        class="align-self-center header-login-button ml-2 primary--text"
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
        class="d-none d-sm-flex align-self-center header-signup-button primary--text"
      >
        <span>Créer mon compte</span>
      </v-btn>

      <v-btn
        text
        elevation="0"
        v-if="loggedUser && userDataReady && $vuetify.breakpoint.mdAndUp"
        :to="{ name: 'ManagementPage' }"
        class="d-none d-sm-flex align-self-center header-signup-button primary--text"
      >
        <span>Mes cantines</span>
      </v-btn>

      <v-btn
        text
        elevation="0"
        v-if="loggedUser && userDataReady && $vuetify.breakpoint.mdAndUp"
        href="/se-deconnecter"
        class="d-none d-sm-flex align-self-center header-signup-button primary--text"
      >
        <span>Me déconnecter</span>
      </v-btn>

      <template v-slot:extension v-if="$vuetify.breakpoint.mdAndUp">
        <v-divider style="position:absolute; top:0; width:100%;"></v-divider>
        <v-tabs align-with-title id="header-tabs" active-class="stealth-active-tab" hide-slider>
          <div
            v-for="(navLink, index) in displayNavLinks"
            :key="index"
            :class="navLink.isActive ? 'mc-active-tab' : ''"
          >
            <v-menu v-if="navLink.children" rounded="0" offset-y attach="#header-tabs" nudge-right="16">
              <template v-slot:activator="{ on, attrs, value }">
                <v-tab
                  v-bind="attrs"
                  v-on="on"
                  class="mc-tab body-2 text--darken-2"
                  :class="navLink.isActive ? 'primary--text' : 'black--text'"
                >
                  {{ navLink.text }}
                  <v-icon small class="ml-2" :color="navLink.isActive ? 'primary' : 'black'">
                    {{ value ? "mdi-chevron-up" : "mdi-chevron-down" }}
                  </v-icon>
                </v-tab>
              </template>
              <v-list class="py-0">
                <div v-for="(subItem, subIndex) in navLink.children" :key="subIndex">
                  <v-list-item :to="subItem.to" :href="subItem.href">
                    <v-list-item-title class="text-body-2">
                      {{ subItem.text }}
                      <v-icon v-if="subItem.href" small color="rgb(22,22,22)">mdi-open-in-new</v-icon>
                    </v-list-item-title>
                  </v-list-item>
                  <v-divider v-if="subIndex !== navLink.children.length - 1" class="mx-4"></v-divider>
                </div>
              </v-list>
            </v-menu>
            <v-tab
              v-else
              :to="navLink.to"
              class="mc-tab body-2"
              :class="navLink.isActive ? 'primary--text' : 'black--text'"
            >
              {{ navLink.text }}
            </v-tab>
          </div>
        </v-tabs>
      </template>
      <v-menu v-if="$vuetify.breakpoint.smAndDown && userDataReady" left bottom offset-y>
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
      navLinks: [
        {
          text: "Gérer mes cantines",
          authenticationState: true,
          children: [
            {
              text: "Mes cantines",
              to: { name: "ManagementPage" },
            },
            {
              text: "Mes achats",
              to: { name: "PurchasesHome" },
            },
            {
              text: "Générer mon affiche",
              to: { name: "GeneratePosterPage" },
            },
            {
              text: "Mon compte",
              to: { name: "AccountSummaryPage" },
            },
          ],
        },
        {
          text: "M'auto-évaluer",
          to: { name: "DiagnosticPage" },
          authenticationState: false,
        },
        {
          text: "À propos la loi EGAlim",
          children: [
            {
              text: "Mesures phares",
              to: {
                name: "KeyMeasurePage",
                params: {
                  id: "qualite-des-produits",
                },
              },
            },
            {
              text: "Documentation",
              href: "https://ma-cantine-1.gitbook.io/ma-cantine-egalim/",
              target: "_blank",
              rel: "noopener",
            },
          ],
        },
        {
          text: "Nos cantines",
          to: { name: "CanteensHome" },
        },
        {
          text: "Communauté",
          children: [
            {
              text: "Notre communauté",
              to: { name: "CommunityPage" },
            },
            {
              text: "Blog",
              to: { name: "BlogsHome" },
            },
          ],
        },
        {
          text: "Statistiques",
          children: [
            {
              text: "Statistiques régionales",
              to: { name: "PublicCanteenStatisticsPage" },
            },
            {
              text: "Nos données",
              href: "https://ma-cantine-metabase.cleverapps.io/public/dashboard/f65ca7cc-c3bd-4cfb-a3dc-236f81864663",
            },
            {
              text: "Usage du site",
              href: "https://stats.data.gouv.fr/index.php?idSite=162",
            },
          ],
        },
        {
          text: "Contact",
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
    displayNavLinks() {
      const currentRoute = this.$route.name
      this.navLinks.forEach((menuItem) => {
        if (menuItem.to && menuItem.to.name === currentRoute) {
          menuItem.isActive = true
        } else if (menuItem.children && menuItem.children.some((child) => child.to?.name === currentRoute)) {
          menuItem.isActive = true
        } else {
          menuItem.isActive = false
        }
      })
      if (!this.loggedUser) {
        return this.navLinks.filter((link) => !link.authenticationState)
      } else {
        return this.navLinks.filter((link) => link.authenticationState !== false)
      }
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
#header {
  box-shadow: 0 8px 8px 0 rgba(0, 0, 0, 0.1), 0 8px 16px -16px rgba(0, 0, 0, 0.32) !important;
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
  color: rgb(22, 22, 22);
}
.mc-tab {
  height: 100%;
  line-height: 24px;
  text-transform: none;
}
.mc-active-tab {
  border-bottom: 2px solid;
}
.stealth-active-tab {
  color: rgb(22, 22, 22) !important;
  caret-color: rgb(22, 22, 22);
  outline-color: #fff;
  text-decoration-color: #fff;
}
.header-signup-button.v-btn--active::before {
  opacity: 0;
}
.header-signup-button.v-btn--active:hover::before {
  opacity: 0.08;
}
</style>
