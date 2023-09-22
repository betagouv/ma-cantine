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
      style="padding: 0 calc((100vw - 78rem)/2);"
      height="116px"
      extension-height="56px"
      id="en-tete"
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
          <div v-if="$vuetify.breakpoint.smAndUp" style="height: 90px" class="d-flex align-center">
            <p id="ma-cantine-header" class="my-0">ma cantine</p>
          </div>
        </router-link>
      </v-toolbar-title>
      <div v-if="chipInfo">
        <v-chip label outlined :color="chipInfo.color" class="font-weight-bold ml-3" small>
          {{ chipInfo.text }}
        </v-chip>
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
            Voulez-vous vous déconnecter de votre compte ma cantine ?
          </v-card-text>

          <v-divider></v-divider>

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
                    {{ value ? "$arrow-up-s-line" : "$arrow-down-s-line" }}
                  </v-icon>
                </v-tab>
              </template>
              <v-list class="py-0">
                <div v-for="(subItem, subIndex) in navLink.children" :key="subIndex">
                  <v-list-item
                    v-if="shouldDisplayChild(subItem)"
                    :to="subItem.to"
                    :href="subItem.href"
                    :target="subItem.target"
                    :rel="subItem.rel"
                  >
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
            <v-icon v-else>$account-circle-fill</v-icon>
            <span class="font-subtitle-3 mx-2 d-none d-sm-inline">Profil</span>
            <v-icon class="ml-1 pt-1" small>$arrow-down-s-line</v-icon>
          </v-btn>

          <v-btn v-else icon class="mr-2 ml-2 align-self-center" v-on="on">
            <v-icon>$menu-fill</v-icon>
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
import keyMeasures from "@/data/key-measures.json"

export default {
  name: "AppHeader",
  components: { HeaderDropdownList },
  data() {
    return {
      logoutWarningDialog: false,
      navLinks: [
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
              text: "Documentation",
              href: "https://ma-cantine-1.gitbook.io/ma-cantine-egalim/",
              target: "_blank",
              rel: "noopener",
            },
          ],
        },
        {
          text: "Comprendre mes obligations",
          children: keyMeasures.map((x) => ({
            text: x.shortTitle,
            to: { name: "KeyMeasurePage", params: { id: x.id } },
          })),
        },
        {
          text: "Toutes les cantines",
          children: [
            {
              text: "Mes cantines",
              to: { name: "ManagementPage" },
              authenticationState: true,
            },
            {
              text: "Dans mon territoire",
              to: { name: "TerritoryCanteens" },
              elected: true,
            },
            {
              text: "Nos cantines publiées",
              to: { name: "CanteensHome" },
            },
            {
              text: "Dans ma collectivité",
              to: { name: "PublicCanteenStatisticsPage" },
            },
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
              text: "Webinaires",
              to: { name: "CommunityPage" },
            },
            {
              text: "Blog",
              to: { name: "BlogsHome" },
            },
            {
              text: "Documentation",
              href: "https://ma-cantine-1.gitbook.io/ma-cantine-egalim/",
              target: "_blank",
              rel: "noopener",
            },
            {
              text: "Mesures de notre impact",
              to: { name: "ImpactMeasuresPage" },
            },
            {
              text: "Indicateurs de résultats de la plateforme",
              href: "https://ma-cantine-metabase.cleverapps.io/public/dashboard/3dab8a21-c4b9-46e1-84fa-7ba485ddfbbb",
            },
            {
              text: "Usage du site",
              href: "https://stats.data.gouv.fr/index.php?idSite=162",
              target: "_blank",
              rel: "noopener",
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
          navlinks.forEach((x) => (x.children = x.children?.filter((y) => !y.elected)))
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
      if (child.authenticationState === undefined && !child.elected) return true
      if (!this.loggedUser) return child.authenticationState === false
      if (child.elected) return this.loggedUser.isElectedOfficial
      return child.authenticationState === true
    },
  },
}
</script>

<style scoped lang="scss">
#en-tete {
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
