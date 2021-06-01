<template>
  <v-footer :height="showSmallFooter ? 50 : 170" color="white" app :absolute="!showSmallFooter">
    <v-divider style="position: absolute; top: 0; left: 0; width: 100%"></v-divider>
    <v-container class="constrained pb-0 pt-0">
      <v-row v-if="!showSmallFooter" class="pt-12">
        <v-col cols="12" sm="2" :class="{ 'd-flex': true, 'flex-column': $vuetify.breakpoint.name != 'xs' }">
          <v-spacer />
          <v-img
            src="/static/images/Marianne.jpg"
            contain
            class="mb-4"
            :max-width="$vuetify.breakpoint.smAndDown ? 70 : 100"
          ></v-img>
          <v-spacer />
          <v-img
            src="/static/images/beta-gouv-logo.png"
            contain
            :max-width="$vuetify.breakpoint.smAndDown ? 80 : 100"
          ></v-img>
          <v-spacer />
        </v-col>
        <v-spacer></v-spacer>
        <v-col cols="12" sm="3" v-for="(column, index) in columns" :key="index" class="caption">
          <p class="text-left font-weight-bold">{{ column.title }}</p>
          <p v-for="(link, index) in column.links" :key="index" class="text-left">
            <a v-if="link.url" :href="link.url" target="_blank">
              {{ link.text }}
            </a>
            <router-link v-if="link.to" :to="link.to">
              {{ link.text }}
            </router-link>
          </p>
        </v-col>
      </v-row>
      <v-row v-if="!showSmallFooter">
        <v-col cols="12" class="d-flex">
          <GiveFeedbackLink />
        </v-col>
      </v-row>
      <v-divider v-if="!showSmallFooter" class="mt-6"></v-divider>
      <div class="d-flex flex-wrap justify-space-between">
        <div class="d-flex justify-space-between" v-for="(link, index) in bottomLinks" :key="link.text">
          <v-btn :class="footerButtonClasses" :to="link.to" :ripple="false" text plain>{{ link.text }}</v-btn>
          <div class="footer-divider mt-3" v-if="index < bottomLinks.length - 1 && showDividers"></div>
        </div>
        <v-spacer v-if="$vuetify.breakpoint.name !== 'sm'"></v-spacer>
        <v-btn v-if="$vuetify.breakpoint.name !== 'sm'" class="caption" text plain disabled>
          © République Française 2021
        </v-btn>
      </div>
    </v-container>
  </v-footer>
</template>

<script>
import GiveFeedbackLink from "@/components/GiveFeedbackLink"

export default {
  data() {
    return {
      bottomLinks: [
        {
          text: "Mentions légales",
          to: { name: "LegalMentions" },
        },
        {
          text: "Politique de confidentialité",
          to: { name: "Confidentiality" },
        },
        {
          text: "Conditions générales d'utilisation",
          to: { name: "CGU" },
        },
      ],
      columns: [
        {
          title: "Ma cantine",
          links: [
            {
              text: "Qui sommes nous ?",
              url: "https://beta.gouv.fr/startups/ma-cantine-egalim.html",
            },
            {
              text: "Nos cantines",
              to: { name: "CanteensHome" },
            },
            {
              text: "Blog",
              to: { name: "BlogsHome" },
            },
            {
              text: "Documentation",
              url: "https://ma-cantine-1.gitbook.io/ma-cantine-egalim/",
            },
            {
              text: "Statistiques",
              to: { name: "StatsPage" },
            },
            {
              text: "Les start-ups d'état",
              url: "https://beta.gouv.fr/approche/",
            },
            {
              text: "Contactez-nous !",
              url: "mailto:contact@egalim.beta.gouv.fr",
            },
          ],
        },
        {
          title: "Aidez-nous à améliorer cet outil",
          links: [
            {
              text: "Contribuer sur Github",
              url: "https://github.com/betagouv/ma-cantine",
            },
            {
              text: "Envoyer une suggestion",
              url: "https://github.com/betagouv/ma-cantine/issues",
            },
          ],
        },
        {
          title: "En collaboration avec",
          links: [
            {
              text: "DGAL (Ministère de l'Agriculture)",
              url: "https://agriculture.gouv.fr/thematique-generale/alimentation",
            },
            {
              text: "beta.gouv.fr",
              url: "https://beta.gouv.fr/",
            },
          ],
        },
      ],
    }
  },
  components: {
    GiveFeedbackLink,
  },
  computed: {
    footerButtonClasses() {
      return {
        caption: true,
        "pl-0": this.$vuetify.breakpoint.name === "sm",
        "pr-0": this.$vuetify.breakpoint.name === "sm",
      }
    },
    showSmallFooter() {
      const viewsWithSmallFooter = []
      return viewsWithSmallFooter.indexOf(this.$route.name) > -1
    },
    showDividers() {
      return this.$vuetify.breakpoint.mdAndUp
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
</style>
