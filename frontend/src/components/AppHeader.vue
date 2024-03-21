<template>
  <div v-if="!!this.$route.name">
    <!-- <div class="fr-skiplinks" ref="skiplinks">
      <nav class="fr-container" role="navigation" aria-label="Accès rapide">
        <ul class="fr-skiplinks__list">
          <li><a class="fr-link" href="#contenu">Contenu</a></li>
          <li><a class="fr-link" href="#en-tete">Menu</a></li>
          <li><a class="fr-link" href="#pied-de-page">Pied de page</a></li>
        </ul>
      </nav>
    </div> -->
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
      <v-toolbar-title class="align-self-center">
        <router-link
          :to="{ name: 'LandingPage' }"
          class="text-decoration-none d-flex align-center pl-4"
          aria-label="ma cantine (aller à l'accueil) - Ministère de l'Agriculture et de la Souveraineté Alimentaire"
          :aria-description="chipInfo && `environnement ${chipInfo.text}`"
        >
          <img src="/static/images/Marianne.png" height="90" alt="" />
          <img v-if="$vuetify.breakpoint.smAndUp" src="/static/images/ma-cantine-logo-light.jpg" height="65" alt="" />
          <v-chip v-if="chipInfo" label outlined :color="chipInfo.color" class="font-weight-bold ml-3" small>
            {{ chipInfo.text }}
          </v-chip>
        </router-link>
      </v-toolbar-title>

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
        v-if="loggedUser && loggedUser.isDev && userDataReady && $vuetify.breakpoint.mdAndUp"
        :to="{ name: 'DeveloperPage' }"
        class="d-none d-sm-flex align-self-center header-signup-button primary--text"
      >
        <span>Développement et APIs</span>
      </v-btn>

      <v-btn
        text
        elevation="0"
        v-if="loggedUser && !loggedUser.isDev && userDataReady && $vuetify.breakpoint.mdAndUp"
        :to="{ name: 'ManagementPage' }"
        class="d-none d-sm-flex align-self-center header-signup-button primary--text"
      >
        <span>Mes cantines</span>
      </v-btn>

      <v-dialog
        v-if="loggedUser && userDataReady && $vuetify.breakpoint.mdAndUp"
        v-model="logoutWarningDialog"
        max-width="500"
      >
        <template v-slot:activator="{ on, attrs }">
          <v-btn
            v-bind="attrs"
            v-on="on"
            text
            elevation="0"
            class="d-none d-sm-flex align-self-center header-signup-button primary--text"
          >
            <span>Me déconnecter</span>
          </v-btn>
        </template>

        <v-card>
          <v-card-text class="pa-8 text-left">
            <p class="mb-0">Voulez-vous vous déconnecter de votre compte ma cantine ?</p>
          </v-card-text>

          <v-divider aria-hidden="true" role="presentation"></v-divider>

          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="grey darken-2" text @click="logoutWarningDialog = false" class="mr-1">
              Non, revenir en arrière
            </v-btn>
            <v-btn color="red darken-2" text href="/se-deconnecter">
              Oui, je confirme
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

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
                      class="fr-nav__link-child body-2"
                      active-class="mc-active-item"
                      color="white"
                      :to="child.to"
                      target="_self"
                    >
                      {{ child.text }}
                    </v-btn>
                  </v-list-item>
                </v-list>
              </v-menu>
              <v-btn
                v-else
                class="fr-nav__link body-2"
                active-class="stealth-active-tab"
                color="white"
                :to="navItem.to"
                target="_self"
              >
                {{ navItem.text }}
              </v-btn>
            </li>
          </ul>
        </nav>
      </template>
    </v-app-bar>
  </div>
</template>

<script>
import keyMeasures from "@/data/key-measures.json"

export default {
  name: "AppHeader",
  data() {
    return {
      logoutWarningDialog: false,
      dashboardEnabled: window.ENABLE_DASHBOARD,
      navLinks: [
        {
          text: "Mon tableau de bord",
          to: { name: "ManagementPage" },
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
            {
              text: "Pour aller plus loin",
              href: "https://ma-cantine-1.gitbook.io/ma-cantine-egalim/",
              target: "_blank",
              rel: "noopener external",
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
              text: "Nos cantines publiées",
              to: { name: "CanteensHome" },
            },
            {
              text: "Dans ma collectivité",
              to: { name: "PublicCanteenStatisticsPage" },
            },
            {
              text: "Indicateurs clés",
              href: "https://ma-cantine-metabase.cleverapps.io/public/dashboard/3dab8a21-c4b9-46e1-84fa-7ba485ddfbbb",
              target: "_blank",
              rel: "noopener external",
            },
          ],
        },
        {
          text: "Comprendre mes obligations",
          children: [
            ...keyMeasures.map((x) => ({
              text: x.shortTitle,
              to: { name: "KeyMeasurePage", params: { id: x.id } },
            })),
            ...[
              {
                text: "Pour aller plus loin",
                href: "https://ma-cantine-1.gitbook.io/ma-cantine-egalim/",
                target: "_blank",
                rel: "noopener external",
              },
            ],
          ],
        },
        {
          text: "Aide",
          children: [
            {
              text: "Foire aux questions",
              to: { name: "FaqPage" },
            },
            {
              text: "Contactez-nous",
              to: { name: "ContactPage" },
            },
            {
              text: "Documentation",
              href: "https://ma-cantine-1.gitbook.io/ma-cantine-egalim/",
              target: "_blank",
              rel: "noopener external",
            },
          ],
        },
        {
          text: "Mon compte",
          to: { name: "AccountSummaryPage" },
          authenticationState: true,
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
      if (this.loggedUser) {
        const navlinks = this.navLinks.filter((link) => link.authenticationState !== false)
        if (!this.loggedUser.isElectedOfficial)
          navlinks.forEach((x) => (x.children = x.children?.filter((y) => !y.forElected)))
        return navlinks
      } else {
        return this.navLinks.filter((link) => !link.authenticationState)
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
    shouldDisplayChild(child) {
      if (child.authenticationState === undefined && !child.forElected) return true
      if (!this.loggedUser) return child.authenticationState === false
      if (child.forElected) return this.loggedUser.isElectedOfficial
      return child.authenticationState === true
    },
  },
}
</script>

<style scoped lang="scss">
#en-tete {
  box-shadow: 0 8px 8px 0 rgba(0, 0, 0, 0.1), 0 8px 16px -16px rgba(0, 0, 0, 0.32) !important;

  // DSFR navigation
  nav {
    width: 100%;
    border-top: solid 1px #e0e0e0;
    height: 56px; // same height as toolbar extension
  }

  .fr-nav__link {
    height: 100%;
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
    .v-btn--active::before {
      opacity: 0; // get rid of the change in background colour
    }
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
  .header-signup-button.v-btn--active::before {
    opacity: 0;
  }
  .header-signup-button.v-btn--active:hover::before {
    opacity: 0.08;
  }
}

.fr-skiplinks {
  top: 0;
  left: 0;
  position: absolute;
  padding: 1rem 0;
  background-color: #ddd;
  width: 100%;
  z-index: 1;
}

// focus-within not currently supported by IE but I think skiplinks are mostly helpful for people
// using screenreaders, which will read out the link whether or not it is visible on screen.
.fr-skiplinks:focus-within {
  z-index: 7;
}

.fr-skiplinks__list {
  display: flex;

  list-style-type: none;
  li {
    margin: 1em 1em;
  }
  /* https://developer.mozilla.org/en-US/docs/Web/CSS/list-style-type#accessibility_concerns */
  li::before {
    content: "\200B";
  }
}
</style>
