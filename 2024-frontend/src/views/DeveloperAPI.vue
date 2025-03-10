<script setup>
import { useRoute } from "vue-router"
import { useRootStore } from "@/stores/root"
import profileService from "@/services/profile"
const route = useRoute()

/* Store */
const store = useRootStore()

/* Data */
const env = window.ENVIRONMENT

const toggleDevMode = (value) => {
  const payload = { isDev: value }
  profileService.updateProfile(store.loggedUser.id, payload).then(() => {
    store.loggedUser.isDev = value
  })
}
</script>

<template>
  <h1>{{ route.meta.title }}</h1>

  <div v-if="!store.loggedUser">
    <p>
      Pour accéder à la documentation des APIs et enregistrer votre application, vous devez créer un compte.
    </p>
    <router-link class="fr-btn fr-btn--primary" to="/creer-mon-compte">
      <span class="fr-icon-account-circle-fill fr-mr-1w"></span>
      Créer mon compte
    </router-link>
  </div>
  <div v-else-if="store.loggedUser.isDev">
    <DsfrCallout v-if="['prod', 'demo'].includes(env)">
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
    </DsfrCallout>
    <h2>Gérer mes applications</h2>
    <p>
      <router-link to="/o/applications/" target="_blank" class="fr-link fr-icon-arrow-right-line fr-link--icon-right">
        Enregistrez vos applications pour obtenir l'accès à l'API avec Oauth2
      </router-link>
    </p>
    <h2>API</h2>
    <p>
      <router-link to="/swagger-ui/" target="_blank" class="fr-link fr-icon-arrow-right-line fr-link--icon-right">
        Consultez la documentation Swagger de notre APIs
      </router-link>
    </p>
    <h2>Exemple d'application</h2>
    <p>
      Une application exemple est disponible en
      <a
        href="https://github.com/betagouv/ma-cantine-demo-integration"
        target="_blank"
        rel="noopener external"
        title="open source - ouvre une nouvelle fenêtre"
      >
        open source
      </a>
      . L'application est basée sur Python/Flask et utilise les APIs ma cantine.
    </p>
    <DsfrCallout>
      <p>
        Cette page ne vous parle pas ?
      </p>
      <DsfrButton
        secondary
        label="Désactiver le mode développeur"
        icon="fr-icon-code-box-line"
        @click="toggleDevMode(false)"
      />
    </DsfrCallout>
  </div>
  <div v-else>
    <p>
      Pour accéder à la documentation des APIs et enregistrer votre application, vous devez activer le mode développeur.
    </p>
    <p>
      Un compte développeur vous permettra toujours d'accéder aux autres pages, mais certaines fonctionnalités de suivi
      seront désactivées.
    </p>
    <DsfrButton primary label="Activer le mode développeur" icon="fr-icon-code-box-line" @click="toggleDevMode(true)" />
  </div>
</template>
