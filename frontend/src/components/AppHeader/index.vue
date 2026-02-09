<template>
  <div v-if="!!this.$route.name">
    <SkipLinks />
    <v-app-bar
      app
      clipped-right
      color="white"
      ref="appbar"
      :style="dashboardEnabled ? 'padding: 0 calc((100vw - 79.3rem)/2);' : 'padding: 0 calc((100vw - 78rem)/2);'"
      height="116px"
      extension-height="56px"
      id="en-tete"
      hide-on-scroll
      role="banner"
    >
      <v-toolbar-title class="align-self-center outline-focus-within">
        <router-link
          :to="{ name: 'LandingPage' }"
          class="text-decoration-none d-flex align-center"
          aria-label="ma cantine (aller à l'accueil) - République Française"
        >
          <img src="/static/images/Marianne-Republique-Francaise.svg" height="100" alt="" />
          <img src="/static/images/ma-cantine-logo-light.svg" height="65" alt="" />
        </router-link>
      </v-toolbar-title>

      <v-spacer></v-spacer>

      <div v-if="$vuetify.breakpoint.mdAndUp" class="d-flex">
        <div v-for="(link, idx) in quickLinks" :key="idx">
          <LogoutButton v-if="link.logout" />
          <v-btn v-else-if="link.href" :href="link.href" text elevation="0" class="ml-2 primary--text">
            {{ link.text }}
          </v-btn>
          <v-btn v-else :to="link.to" text elevation="0" class="ml-2 primary--text">
            {{ link.text }}
          </v-btn>
        </div>
      </div>

      <template v-slot:extension v-if="$vuetify.breakpoint.mdAndUp">
        <nav class="fr-nav my-n1" id="navigation-773" role="navigation" aria-label="Menu principal">
          <ul class="fr-nav__list no-bullets d-flex fill-height">
            <li
              v-for="(navItem, parentIdx) in displayNavLinks"
              :key="parentIdx"
              :id="`nav-${parentIdx}`"
              :class="{ 'fr-nav__item fill-height mc-tab': true, 'mc-active-tab': navItem.isActive }"
            >
              <v-menu v-if="navItem.children" :attach="`#nav-${parentIdx}`" offset-y tile>
                <template v-slot:activator="{ on, attrs }">
                  <v-btn class="fr-nav__link body-2" color="white" v-bind="attrs" v-on="on">
                    {{ navItem.text }}
                    <v-icon v-if="attrs['aria-expanded'] === 'true'" small class="menu-arrow ml-2">
                      $arrow-up-s-line
                    </v-icon>
                    <v-icon v-else small class="menu-arrow ml-2">$arrow-down-s-line</v-icon>
                  </v-btn>
                </template>
                <v-list role="list" class="pa-0">
                  <v-list-item
                    v-for="(child, childIdx) in navItem.children"
                    :key="`${parentIdx}-${childIdx}`"
                    role="listitem"
                    class="pa-0"
                  >
                    <v-btn
                      v-if="child.to"
                      class="fr-nav__link-child body-2"
                      active-class="mc-active-item"
                      color="white"
                      :to="child.to"
                    >
                      {{ child.text }}
                    </v-btn>
                    <v-btn
                      v-else
                      class="fr-nav__link-child body-2"
                      color="white"
                      :href="child.href"
                      target="_blank"
                      rel="noopener external"
                      :title="`${child.text} - ouvre une nouvelle fenêtre`"
                    >
                      {{ child.text }}
                      <v-icon small color="grey darken-3" class="ml-1">mdi-open-in-new</v-icon>
                    </v-btn>
                  </v-list-item>
                </v-list>
              </v-menu>
              <v-btn
                v-else
                class="fr-nav__link body-2"
                active-class="stealt !importanth-active-tab"
                color="white"
                :to="navItem.to"
              >
                {{ navItem.text }}
              </v-btn>
            </li>
          </ul>
        </nav>
      </template>
      <v-dialog v-if="$vuetify.breakpoint.smAndDown" v-model="overlayMenu" fullscreen hide-overlay id="navigation-menu">
        <template v-slot:activator="{ on, attrs }">
          <v-app-bar-nav-icon v-bind="attrs" v-on="on"></v-app-bar-nav-icon>
        </template>
        <v-card class="text-right">
          <v-btn @click="overlayMenu = false" aria-controls="navigation-menu" text color="primary" class="mt-4">
            <span class="d-flex align-center">
              Fermer
              <v-icon small color="primary" class="ml-2">
                $close-line
              </v-icon>
            </span>
          </v-btn>
          <nav role="navigation" aria-label="Menu secondaire" class="text-left py-2" id="menu-quick-links">
            <ul class="no-bullets">
              <li v-for="(link, idx) in quickLinks" :key="idx">
                <LogoutButton v-if="link.logout" />
                <v-btn v-else-if="link.href" :href="link.href" text class="primary--text">
                  {{ link.text }}
                </v-btn>
                <v-btn v-else :to="link.to" text class="primary--text" @click="overlayMenu = false">
                  {{ link.text }}
                </v-btn>
              </li>
            </ul>
          </nav>
          <nav role="navigation" aria-label="Menu principal" class="text-left py-2">
            <ul class="no-bullets">
              <li v-for="(link, idx) in displayNavLinks" :key="idx" class="menu-item py-1">
                <v-btn
                  v-if="link.children"
                  @click="childMenu = childMenu === idx ? null : idx"
                  :aria-controls="`child-menu-${idx}`"
                  :aria-expanded="childMenu === idx"
                  text
                  :class="{
                    'body-2 font-weight-bold': true,
                    'mc-active-item': link.isActive,
                  }"
                  style="width: 100%;"
                >
                  {{ link.text }}
                  <v-spacer />
                  <v-icon v-if="childMenu === idx" small class="menu-arrow ml-2">$arrow-up-s-line</v-icon>
                  <v-icon v-else small class="menu-arrow ml-2">$arrow-down-s-line</v-icon>
                </v-btn>
                <v-btn
                  v-else
                  :to="link.to"
                  text
                  class="body-2 font-weight-bold"
                  active-class="mc-active-item"
                  @click="overlayMenu = false"
                >
                  {{ link.text }}
                </v-btn>
                <div v-if="link.children" :id="`child-menu-${idx}`">
                  <v-expand-transition>
                    <ul v-if="childMenu === idx" class="no-bullets ml-2">
                      <li v-for="(child, childIdx) in link.children" :key="childIdx">
                        <v-btn
                          v-if="child.to"
                          :to="child.to"
                          class="fr-nav__link-child body-2"
                          color="white"
                          @click="overlayMenu = false"
                        >
                          {{ child.text }}
                        </v-btn>
                        <v-btn
                          v-else
                          :href="child.href"
                          class="fr-nav__link-child body-2"
                          color="white"
                          target="_blank"
                          rel="noopener external"
                          :title="`${child.text} - ouvre une nouvelle fenêtre`"
                        >
                          {{ child.text }}
                          <v-icon small color="grey darken-3" class="ml-1">mdi-open-in-new</v-icon>
                        </v-btn>
                      </li>
                    </ul>
                  </v-expand-transition>
                </div>
              </li>
            </ul>
          </nav>
        </v-card>
      </v-dialog>
    </v-app-bar>
  </div>
</template>

<script>
import LogoutButton from "./LogoutButton"
import SkipLinks from "./SkipLinks"
import documentation from "../../../../2024-frontend/src/data/documentation.json"

export default {
  name: "AppHeader",
  components: { LogoutButton, SkipLinks },
  data() {
    return {
      dashboardEnabled: window.ENABLE_DASHBOARD,
      overlayMenu: false,
      navLinks: [
        {
          text: "Mon tableau de bord",
          to: { name: "GestionnaireTableauDeBord" },
          authenticationState: true,
        },
        {
          text: "Mes achats",
          to: { name: "PurchasesHome" },
          authenticationState: true,
        },
        {
          text: "M'auto-évaluer",
          to: { name: "DiagnosticPage" },
          authenticationState: false,
        },
        {
          text: "M'améliorer",
          children: [
            {
              text: "Acteurs de l'éco-système",
              to: { name: "PartnersHome" },
            },
            {
              text: "Actions anti-gaspi",
              to: { name: "WasteActionsHome" },
            },
            {
              text: "Générer mon affiche",
              to: { name: "GeneratePosterPage" },
            },
            {
              text: "Webinaires",
              to: { name: "CommunityPage" },
            },
            {
              text: "Blog",
              to: { name: "BlogsHome" },
            },
          ],
        },
        {
          text: "Toutes les cantines",
          children: [
            {
              text: "Dans mon territoire",
              to: { name: "TerritoryCanteens" },
              forElected: true,
            },
            {
              text: "Trouver une cantine",
              to: { name: "CanteenSearchLanding" },
            },
            {
              text: "Observatoire EGalim",
              to: { name: "Observatoire" },
            },
          ],
        },
        {
          text: "Comprendre mes obligations",
          to: { name: "ComprendreMesObligations" },
        },
        {
          text: "Aide",
          children: [
            {
              text: "Contactez-nous",
              to: { name: "Contact" },
            },
            {
              text: "Documentation",
              href: documentation.accueil,
            },
          ],
        },
        {
          text: "Mon compte",
          to: { name: "AccountSummaryPage" },
          authenticationState: true,
        },
      ],
      childMenu: null,
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
      if (this.loggedUser) {
        const navlinks = this.navLinks.filter((link) => link.authenticationState !== false)
        if (!this.loggedUser.isElectedOfficial)
          navlinks.forEach((x) => (x.children = x.children?.filter((y) => !y.forElected)))
        return navlinks
      } else {
        const navlinks = this.navLinks.filter((link) => !link.authenticationState)
        navlinks.forEach((x) => (x.children = x.children?.filter((y) => !y.forElected)))
        return navlinks
      }
    },
    quickLinks() {
      if (!this.userDataReady) return []
      if (!this.loggedUser) {
        const login = { href: "/s-identifier", text: "S'identifier" }
        const signup = { href: "/creer-mon-compte", text: "Créer mon compte" }
        return [login, signup]
      }
      const logout = { logout: true }
      if (this.loggedUser.isDev) {
        const apis = { to: { name: "Developpeurs" }, text: "Développement et APIs" }
        return [apis, logout]
      }
      const mesCantines = { to: { name: "GestionnaireTableauDeBord" }, text: "Mon tableau de bord" }
      return [mesCantines, logout]
    },
  },
  methods: {
    shouldDisplayChild(child) {
      if (child.authenticationState === undefined && !child.forElected) return true
      if (!this.loggedUser) return child.authenticationState === false
      if (child.forElected) return this.loggedUser.isElectedOfficial
      return child.authenticationState === true
    },
  },
  watch: {
    loggedUser() {
      // user may have logged out from overlay menu, so it should be closed
      this.overlayMenu = false
    },
  },
}
</script>

<style scoped lang="scss">
#en-tete {
  filter: drop-shadow(0 1px 3px rgba(0, 0, 18, 0.16));

  // DSFR navigation
  nav {
    width: 100%;
    border-top: solid 1px #e0e0e0;
    height: 56px; // same height as toolbar extension
  }
}

.fr-nav__link {
  height: 100% !important;
}

.fr-nav__link-child {
  height: 48px;
  width: 100%;
  justify-content: left;
}
.mc-tab {
  height: 100%;
  line-height: 24px;
  text-transform: none;
}
.mc-active-tab {
  border-bottom: 2px solid;
  color: #000091;
}
.mc-active-item {
  border-left: 2px solid;
  border-left-color: currentColor !important;
  color: #000091;
}
button {
  color: inherit;
}
.stealth-active-tab {
  color: rgb(22, 22, 22) !important;
  caret-color: rgb(22, 22, 22);
  outline-color: #fff;
  text-decoration-color: #fff;
}
.quick-link.v-btn--active::before {
  opacity: 0;
}
.v-btn--active::before {
  opacity: 0; // get rid of the change in background colour
}
.v-btn--active:hover::before {
  opacity: 0.08;
}

#menu-quick-links {
  border-bottom: solid 1px #e0e0e0;
}

.menu-item {
  border-bottom: solid 1px #e0e0e0;
}
</style>
