<template>
  <v-footer color="white" app :absolute="!showSmallFooter" height="280">
    <v-divider style="position: absolute; top: 0; left: 0; width: 100%"></v-divider>
    <v-container class="constrained pb-4 pb-sm-0 pt-0 text-left">
      <v-row v-if="!showSmallFooter" class="pt-12 pt-sm-0">
        <v-col cols="12" sm="3" :class="{ 'd-flex': true, 'flex-column': $vuetify.breakpoint.name != 'xs' }">
          <v-img src="/static/images/Marianne.png" contain class="mb-4" max-width="230"></v-img>
          <v-spacer />
        </v-col>
        <v-spacer></v-spacer>
        <v-col cols="12" sm="8" md="6" class="text-body-2">
          <p>
            « ma cantine » est un outil pour accompagner les acteurs de la restauration collective à proposer une
            alimentation de qualité, saine et durable.
            <a href="https://beta.gouv.fr/startups/ma-cantine-egalim.html">
              Découvrez notre page produit
              <v-icon small color="primary" class="ml-1">mdi-open-in-new</v-icon>
            </a>
          </p>
          <p>
            Le code source est ouvert et les contributions sont bienvenues.
            <a href="https://github.com/betagouv/ma-cantine/">
              Voir le code source
              <v-icon small color="primary" class="ml-1">mdi-open-in-new</v-icon>
            </a>
          </p>
          <ul class="d-flex justify-space-between font-weight-bold pl-0 flex-wrap link-group">
            <li class="mr-1 mt-2">
              <a href="https://legifrance.gouv.fr">legifrance.gouv.fr</a>
            </li>
            <li class="mr-1 mt-2">
              <a href="https://gouvernement.fr">gouvernement.fr</a>
            </li>
            <li class="mr-1 mt-2">
              <a href="https://service-public.fr">service-public.fr</a>
            </li>
            <li class="mr-1 mt-2">
              <a href="https://data.gouv.fr">data.gouv.fr</a>
            </li>
          </ul>
        </v-col>
      </v-row>
      <v-divider v-if="!showSmallFooter" class="mt-6"></v-divider>
      <ul class="d-flex justify-sm-space-between flex-wrap link-group pl-0">
        <li v-for="(link, index) in bottomLinks" :key="link.text" class="d-flex">
          <v-btn class="caption px-0" :to="link.to" :ripple="false" text plain>{{ link.text }}</v-btn>
          <div class="footer-divider mt-3 mx-4" v-if="index < bottomLinks.length - 1"></div>
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
      ],
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
  height: 16px;
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
</style>
