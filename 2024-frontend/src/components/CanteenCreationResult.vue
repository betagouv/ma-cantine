<script setup>
import { computed, ref } from "vue"
import { useRouter } from "vue-router"
import { useRootStore } from "@/stores/root"
import canteensService from "@/services/canteens"
import AppLinkRouter from "@/components/AppLinkRouter.vue"
import AppSeparator from "@/components/AppSeparator.vue"

const loading = ref(false)

/* Props */
const props = defineProps(["name", "siret", "city", "department", "status", "id", "siren", "linkedCanteens"])

/* Content */
const linkedCanteensLabel = computed(() => {
  const count = props.linkedCanteens.length
  const establishment = count === 1 ? "établissement" : "établissements"
  const exist = count === 1 ? "existe" : "existent"
  return `${count} ${establishment} ${exist} déjà pour cette unité locale`
})

/* Store and Router */
const store = useRootStore()
const router = useRouter()

/* Claim a canteen */
const claimCanteen = (id) => {
  loading.value = true
  canteensService
    .claimCanteen(id)
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
        message: `Nous avons contacté l'équipe de la cantine ${props.name}. Ces derniers reviendront vers vous pour accepter ou non votre demande.`,
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
        <DsfrBadge v-if="status === 'selected'" type="success" :label="siret ? 'sélectionné' : 'rattaché'" small />
      </div>
      <div class="fr-col-offset-1"></div>
      <ul class="ma-cantine--unstyled-list fr-my-0 fr-col-6">
        <li>
          <p class="fr-mb-0 fr-text--xs">{{ siret ? "SIRET" : "SIREN" }} : {{ siret || siren }}</p>
        </li>
        <li>
          <p class="fr-mb-0 fr-text--xs">Ville : {{ city }} ({{ department }})</p>
        </li>
      </ul>
    </div>
    <div v-if="status === 'can-be-linked'" class="fr-mt-1w">
      <div v-if="linkedCanteens.length > 0" class="fr-mb-2w">
        <DsfrBadge type="warning" :label="linkedCanteensLabel" />
        <AppSeparator class="fr-my-1w" />
        <ul class="fr-pl-0">
          <li
            v-for="canteen in linkedCanteens"
            :key="canteen.id"
            class="canteen-creation-result__tertiary-action fr-mt-1v"
          >
            <div>
              <p class="fr-text--bold fr-mb-0">{{ canteen.name }}</p>
              <p class="fr-mb-0 fr-text--xs">{{ canteen.city }} ({{ canteen.department }})</p>
              <p v-if="canteen.isManagedByUser" class="fr-mb-0 fr-text--xs">
                Vous êtes gestionnaire de cet établissement.
              </p>
              <p v-if="!canteen.isManagedByUser && canteen.canBeClaimed" class="fr-mb-0 fr-text--xs">
                Cet établissement n’a pas de gestionnaire.
              </p>
            </div>
            <DsfrButton
              v-if="!canteen.isManagedByUser && canteen.canBeClaimed"
              tertiary
              label="Revendiquer la cantine"
              @click="claimCanteen(canteen.id)"
              :disabled="loading"
            />
          </li>
        </ul>
      </div>
      <div class="fr-grid-row fr-grid-row--center">
        <DsfrButton
          label="Créer un nouvel établissement rattaché à cette unité légale"
          icon="fr-icon-add-circle-fill"
          secondary
          @click="$emit('select')"
        />
      </div>
    </div>
    <div v-else-if="status === 'can-be-created'" class="fr-grid-row fr-grid-row--center fr-mt-1w">
      <DsfrButton
        label="Sélectionner cet établissement"
        icon="fr-icon-add-circle-fill"
        secondary
        @click="$emit('select')"
      />
    </div>
    <div v-else-if="status === 'managed-by-user'" class="fr-mt-1v">
      <DsfrBadge type="success" label="cantine déjà existante" small />
      <p class="fr-mb-0 fr-text--xs">
        La cantine avec le numéro SIRET {{ siret }} existe déjà et fait déjà partie de vos cantines.
        <AppLinkRouter
          :to="{ name: 'DashboardManager', params: { canteenUrlComponent: id } }"
          title="Accéder à sa fiche"
        />
      </p>
    </div>
    <div v-else-if="status === 'can-be-claimed'" class="canteen-creation-result__tertiary-action fr-mt-1v">
      <div>
        <DsfrBadge type="success" label="cantine déjà existante" small />
        <p class="fr-mb-0 fr-text--xs">
          La cantine avec le numéro SIRET {{ siret }} est déjà référencée sur notre site, mais n'a pas de gestionnaire
          enregistré.
        </p>
      </div>
      <DsfrButton tertiary label="Revendiquer la cantine" @click="claimCanteen(props.id)" :disabled="loading" />
    </div>
    <div v-else-if="status === 'ask-to-join'" class="canteen-creation-result__tertiary-action fr-mt-1v">
      <div>
        <DsfrBadge type="success" label="cantine déjà existante" small />
        <p class="fr-mb-0 fr-text--xs">
          La cantine avec le numéro SIRET {{ siret }} est déjà référencée sur notre site. Vous n’êtes pas enregistré en
          tant que gestionnaire.
        </p>
      </div>
      <DsfrButton tertiary :label="joinLabel" @click="joinCanteen()" :disabled="loading" />
    </div>
  </div>
</template>

<style lang="scss">
.canteen-creation-result {
  &__tertiary-action {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;

    @media (min-width: 576px) {
      flex-direction: row;
      justify-content: space-between;
      align-items: center;
    }

    p {
      flex-grow: 1;
    }

    button {
      flex-shrink: 0;
    }
  }
}
</style>
