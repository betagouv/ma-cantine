<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import { useRootStore } from "@/stores/root"
import canteensService from "@/services/canteens"
import AppLinkRouter from "@/components/AppLinkRouter.vue"

const loading = ref(false)

/* Props */
const props = defineProps(["name", "siret", "city", "department", "status", "id"])

/* Store and Router */
const store = useRootStore()
const router = useRouter()

/* Claim a canteen */
const claimCanteen = () => {
  loading.value = true
  canteensService
    .claimCanteen(props.id)
    .then((response) => {
      loading.value = false
      if (response.id) {
        router.push({
          name: "DashboardManager",
          params: { canteenUrlComponent: response.id },
        })
      }
    })
    .catch((e) => {
      loading.value = false
      store.notifyServerError(e)
    })
}

/* Ask to join */
const joinLabel = ref("Rejoindre la cantine")
const joinCanteen = () => {
  loading.value = true
  const userInfos = {
    email: store.loggedUser.email,
    name: `${store.loggedUser.firstName} ${store.loggedUser.lastName}`,
  }
  canteensService
    .joinCanteen(props.id, userInfos)
    .then(() => {
      store.notify({
        title: "Demande envoyée",
        message: `Nous avons contacté l'équipe de la cantine ${props.name}, ces derniers reviendrons vers vous pour accepter ou non votre demande.`,
      })
      joinLabel.value = "Demande envoyée"
    })
    .catch((e) => {
      loading.value = false
      store.notifyServerError(e)
    })
}
</script>

<template>
  <div class="canteen-creation-result fr-card fr-p-3v">
    <div class="fr-grid-row fr-grid-row--top fr-grid-row--left">
      <div class="fr-col-5">
        <p class="fr-h6 fr-mb-1v">{{ name }}</p>
        <DsfrBadge v-if="status === 'selected'" type="success" label="sélectionné" small />
      </div>
      <div class="fr-col-offset-1"></div>
      <ul class="ma-cantine--unstyled-list fr-my-0 fr-col-6">
        <li>
          <p class="fr-mb-0 fr-text--xs">SIRET : {{ siret }}</p>
        </li>
        <li>
          <p class="fr-mb-0 fr-text--xs">Ville : {{ city }} ({{ department }})</p>
        </li>
      </ul>
    </div>
    <div v-if="status === 'can-be-created'" class="fr-grid-row fr-grid-row--center fr-mt-1w">
      <DsfrButton
        label="Sélectionner cet établissement"
        icon="fr-icon-add-circle-fill"
        secondary
        @click="$emit('select')"
      />
    </div>
    <div v-if="status === 'managed-by-user'" class="fr-mt-1v">
      <DsfrBadge type="success" label="cantine déjà existante" small />
      <p class="fr-mb-0 fr-text--xs">
        La cantine avec le numéro SIRET {{ siret }} existe déjà et fait déjà partie de vos cantines.
        <AppLinkRouter
          :to="{ name: 'DashboardManager', params: { canteenUrlComponent: id } }"
          title="Accéder à sa fiche"
        />
      </p>
    </div>
    <div v-if="status === 'can-be-claimed'" class="fr-mt-1v">
      <DsfrBadge type="success" label="cantine déjà existante" small />
      <div class="canteen-creation-result__tertiary-action">
        <p class="fr-mb-0 fr-text--xs fr-col-7">
          La cantine avec le numéro SIRET {{ siret }} est déjà référencée sur notre site, mais n'a pas de gestionnaire
          enregistré.
        </p>
        <DsfrButton tertiary label="Revendiquer la cantine" @click="claimCanteen()" :disabled="loading" />
      </div>
    </div>
    <div v-if="status === 'ask-to-join'" class="fr-mt-1v">
      <DsfrBadge type="success" label="cantine déjà existante" small />
      <div class="canteen-creation-result__tertiary-action">
        <p class="fr-mb-0 fr-text--xs fr-col-7">
          La cantine avec le numéro SIRET {{ siret }} est déjà référencée sur notre site. Vous n’êtes pas enregistré en
          tant que gestionnaire.
        </p>
        <DsfrButton tertiary :label="joinLabel" @click="joinCanteen()" :disabled="loading" />
      </div>
    </div>
  </div>
</template>

<style lang="scss">
.canteen-creation-result {
  &__tertiary-action {
    display: flex;
    justify-content: space-between;
    column-gap: 0.5rem;
    align-items: flex-start;

    p {
      flex-grow: 1;
    }
  }
}
</style>
