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
      <p v-if="env === 'prod'">
        Vous êtes dans l'environnement
        <b>production</b>
        de
        <i>ma cantine</i>
        . Veuillez utiliser
        <a href="https://ma-cantine-demo.cleverapps.io">le site démo</a>
        pour les tests.
      </p>
      <p v-else-if="env === 'demo'">
        Vous êtes dans l'environnement
        <b>démo</b>
        de
        <i>ma cantine</i>
        . Cet environnement est un bac à sable dédié aux tests.
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
            <v-card-title><h2 class="fr-h5 mb-1">Gérer mes applications</h2></v-card-title>
            <v-card-text>
              <p class="mb-0">Enregistrez vos applications pour obtenir l'accès à l'API avec Oauth2</p>
            </v-card-text>
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
            <v-card-title><h2 class="fr-h5 mb-1">API</h2></v-card-title>
            <v-card-text><p class="mb-0">Consultez la documentation Swagger de notre API</p></v-card-text>
            <v-spacer></v-spacer>
            <v-card-actions class="px-4 py-4">
              <v-spacer></v-spacer>
              <v-icon color="primary">$arrow-right-line</v-icon>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
      <p class="mt-4">
        Une application exemple est disponible en
        <a
          href="https://github.com/betagouv/ma-cantine-demo-integration"
          target="_blank"
          rel="noopener external"
          title="open source - ouvre une nouvelle fenêtre"
        >
          open source
          <v-icon small color="primary">$external-link-line</v-icon>
        </a>
        . L'application est basée sur Python/Flask et utilise les APIs ma cantine.
      </p>
      <p>
        Cette page ne vous parle pas ?
        <a @click="toggleDevMode(false)" text>Désactiver le mode développeur de votre compte</a>
        .
      </p>
      <v-divider aria-hidden="true" role="presentation" class="my-10"></v-divider>

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
    env() {
      return window.ENVIRONMENT
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
