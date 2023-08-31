<template>
  <v-footer id="pied-de-page" color="white" app :absolute="!showSmallFooter" height="280">
    <v-divider style="position: absolute; top: 0; left: 0; width: 100%"></v-divider>
    <v-container class="constrained pb-4 pb-sm-0 pt-0 text-left">
      <v-row v-if="!showSmallFooter" class="pt-12 pt-sm-0">
        <v-col cols="12" sm="3" :class="{ 'd-flex': true, 'flex-column': $vuetify.breakpoint.name != 'xs' }">
          <v-img src="/static/images/Marianne.png" contain class="mb-4" max-width="230"></v-img>
          <v-spacer />
        </v-col>
        <v-spacer></v-spacer>
        <v-col cols="12" sm="8" md="7" class="text-body-2">
          <p>
            « ma cantine » est un outil pour accompagner les acteurs de la restauration collective à proposer une
            alimentation de qualité, saine et durable.
            <a href="https://beta.gouv.fr/startups/ma-cantine-egalim.html" class="grey--text text--darken-3">
              Découvrez notre page produit
              <v-icon small color="grey darken-3" class="ml-1">mdi-open-in-new</v-icon>
            </a>
          </p>
          <p>
            Le code source est ouvert et les contributions sont bienvenues.
            <a href="https://github.com/betagouv/ma-cantine/" class="grey--text text--darken-3">
              Voir le code source
              <v-icon small color="grey darken-3" class="ml-1">mdi-open-in-new</v-icon>
            </a>
            . Vous pouvez également obtenir des informations concernant la
            <a href="https://updown.io/2l7f" class="grey--text text--darken-3">
              disponibilité de la plateforme
              <v-icon small color="grey darken-3" class="ml-1">mdi-open-in-new</v-icon>
            </a>
          </p>
          <!-- ml-n1 here makes up for the a11y need of ::before on li elements for them to be recognised by all screen readers -->
          <ul class="d-flex justify-space-between font-weight-bold pl-0 ml-n1 flex-wrap link-group">
            <li class="mr-1 mt-2" v-for="link in govLinks" :key="link">
              <a class="grey--text text--darken-4 font-weight-bold" :href="`https://${link}`">
                {{ link }}
              </a>
              <v-icon small color="grey darken-4">mdi-open-in-new</v-icon>
            </li>
          </ul>
        </v-col>
      </v-row>
      <v-divider v-if="!showSmallFooter" class="mt-6 mb-2"></v-divider>
      <ul class="d-flex justify-sm-space-between flex-wrap link-group pl-0">
        <li v-for="(link, index) in bottomLinks" :key="link.text" class="d-flex my-1">
          <router-link class="caption px-0 grey--text text--darken-2" :to="link.to">{{ link.text }}</router-link>
          <div class="footer-divider mx-4" v-if="index < bottomLinks.length - 1"></div>
        </li>
        <v-spacer></v-spacer>
      </ul>
      <p class="caption mt-2 mb-0 grey--text text--darken-2">
        Sauf mention contraire, tous les contenus de ce site sont sous
        <a href="https://github.com/betagouv/ma-cantine/blob/staging/LICENSE" class="grey--text text--darken-2">
          licence MIT
          <v-icon small color="grey-darken-2" class="ml-1">mdi-open-in-new</v-icon>
        </a>
      </p>
    </v-container>
  </v-footer>
</template>

<script>
export default {
  name: "AppFooter",
  data() {
    return {
      bottomLinks: [
        {
          text: "Mentions légales",
          to: { name: "LegalNotices" },
        },
        {
          text: "Conditions générales",
          to: { name: "CGU" },
        },
        {
          text: "Politique de confidentialité",
          to: { name: "PrivacyPolicy" },
        },
        {
          text: "Accessibilité : non conforme",
          to: { name: "AccessibilityDeclaration" },
        },
        {
          text: "Plan du site",
          to: { name: "SiteMap" },
        },
      ],
      govLinks: ["legifrance.gouv.fr", "gouvernement.fr", "service-public.fr", "data.gouv.fr"],
    }
  },
  computed: {
    showSmallFooter() {
      const viewsWithSmallFooter = []
      return viewsWithSmallFooter.indexOf(this.$route.name) > -1
    },
  },
}
</script>

<style scoped>
.footer-divider {
  background-color: #d7d8de;
  width: 1px;
  height: inherit;
}
.tab-bar-spacer {
  height: 56px;
}
.link-group {
  list-style-type: none;
}
/* https://developer.mozilla.org/en-US/docs/Web/CSS/list-style-type#accessibility_concerns */
.link-group li::before {
  content: "\200B";
}
.link-group > li > a {
  text-decoration: none;
}
.link-group > li > a:hover,
.link-group > li > a:focus {
  text-decoration: underline;
}
</style>
