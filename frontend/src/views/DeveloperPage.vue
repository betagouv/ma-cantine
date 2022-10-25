<template>
  <div class="text-left">
    <BreadcrumbsNav />
    <h1 class="text-h4 font-weight-black mb-6">Développement et APIs</h1>
    <div v-if="!loggedUser">
      <p>
        Pour accéder à la documentation des APIs et enregistrer votre application, vous devez créer un compte.
      </p>
      <v-btn href="/creer-mon-compte" large color="primary" class="mt-2">
        <v-icon class="mr-2">$account-circle-fill</v-icon>
        Créer mon compte
      </v-btn>
    </div>
    <div v-else-if="loggedUser.isDev">
      <p>Sur cette page vous pouvez gérer vos applications et consulter la documentation de notre API.</p>
      <p>
        Vous pouvez aussi
        <a @click="toggleDevMode(false)" text>désactiver le mode développeur de votre compte</a>
        .
      </p>
      <v-row class="mt-6">
        <v-col cols="12" sm="6">
          <v-card
            href="/o/applications/"
            target="_blank"
            outlined
            :ripple="false"
            class="dsfr d-flex flex-column fill-height"
          >
            <v-card-title class="font-weight-bold">Gérer mes applications</v-card-title>
            <v-card-text>Enregistrez vos applications pour obtenir l'accès à l'API avec Oauth2</v-card-text>
            <v-spacer></v-spacer>
            <v-card-actions class="px-4 py-4">
              <v-spacer></v-spacer>
              <v-icon color="primary">$arrow-right-line</v-icon>
            </v-card-actions>
          </v-card>
        </v-col>
        <v-col cols="12" sm="6">
          <v-card
            outlined
            href="/swagger-ui/"
            target="_blank"
            :ripple="false"
            class="dsfr d-flex flex-column fill-height"
          >
            <v-card-title class="font-weight-bold">API</v-card-title>
            <v-card-text>Consultez la documentation Swagger de notre API</v-card-text>
            <v-spacer></v-spacer>
            <v-card-actions class="px-4 py-4">
              <v-spacer></v-spacer>
              <v-icon color="primary">$arrow-right-line</v-icon>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
      <p class="mt-4">
        On a aussi créé une petite application Python/Flask
        <a href="https://github.com/betagouv/ma-cantine-demo-integration" target="_blank" rel="noopener">
          open source
          <v-icon small color="primary">$external-link-line</v-icon>
        </a>
        pour démontrer comment l'intégration pourrait être fait.
      </p>
      <v-divider class="my-10"></v-divider>

      <h2 class="text-h6 font-weight-black mt-10 mb-6">Une question ? Contactez-nous</h2>
      <GeneralContactForm></GeneralContactForm>
    </div>
    <div v-else>
      <p>
        Pour accéder à la documentation des APIs et enregistrer votre application, vous devez activer le mode
        développeur.
      </p>
      <p>
        Un compte développeur vous permettra toujours d'accéder aux autres pages, mais certaines fonctionnalités de
        suivi seront désactivées.
      </p>
      <v-btn @click="toggleDevMode(true)" large color="primary" class="mt-2">
        <v-icon class="mr-2">$code-box-line</v-icon>
        Activer le mode développeur
      </v-btn>
    </div>
  </div>
</template>

<script>
import GeneralContactForm from "@/components/GeneralContactForm"
import BreadcrumbsNav from "@/components/BreadcrumbsNav"

export default {
  components: { BreadcrumbsNav, GeneralContactForm },
  name: "DeveloperPage",
  computed: {
    loggedUser() {
      return this.$store.state.loggedUser
    },
  },
  methods: {
    toggleDevMode(enable) {
      const payload = { isDev: enable }
      this.$store
        .dispatch("updateProfile", { payload })
        .then(() => {
          this.$store.dispatch("notify", {
            title: `Le mode développeur à été ${enable ? "activé" : "désactivé"} sur votre compte`,
            status: "success",
          })
        })
        .catch((e) => {
          this.$store.dispatch("notifyServerError", e)
        })
    },
  },
}
</script>
