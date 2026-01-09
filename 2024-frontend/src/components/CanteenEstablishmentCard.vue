<script setup>
import { computed } from "vue"
import AppLinkRouter from "@/components/AppLinkRouter.vue"
import AppSeparator from "@/components/AppSeparator.vue"
import CanteenButtonClaim from "@/components/CanteenButtonClaim.vue"
import CanteenButtonJoin from "@/components/CanteenButtonJoin.vue"
import CanteenButtonLink from "@/components/CanteenButtonLink.vue"

/* Props */
const props = defineProps(["name", "siret", "city", "department", "status", "id", "siren", "linkedCanteens", "groupId"])

/* Content */
const linkedCanteensLabel = computed(() => {
  const count = props.linkedCanteens.length
  const establishment = count === 1 ? "établissement" : "établissements"
  const exist = count === 1 ? "existe" : "existent"
  return `${count} ${establishment} ${exist} déjà pour cette unité légale`
})
</script>

<template>
  <div class="canteen-establishment-card fr-card fr-p-3v">
    <div class="fr-grid-row fr-grid-row--top fr-grid-row--left">
      <div class="fr-col-5">
        <p class="fr-h6 fr-mb-1v">{{ name }}</p>
        <DsfrBadge v-if="status === 'selected'" type="success" label="sélectionné" small />
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
            class="canteen-establishment-card__tertiary-action fr-mt-2w"
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
              <p v-if="canteen.canBeClaimed" class="fr-mb-0 fr-text--xs">
                Cet établissement a déjà des gestionnaires.
              </p>
            </div>
            <CanteenButtonClaim v-if="!canteen.isManagedByUser && canteen.canBeClaimed" :id="canteen.id" />
            <CanteenButtonJoin
              v-if="!canteen.isManagedByUser && !canteen.canBeClaimed"
              :id="canteen.id"
              :name="canteen.name"
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
    <div v-else-if="status === 'can-be-claimed'" class="canteen-establishment-card__tertiary-action fr-mt-1v">
      <div>
        <DsfrBadge type="success" label="cantine déjà existante" small />
        <p class="fr-mb-0 fr-text--xs">
          La cantine avec le numéro SIRET {{ siret }} est déjà référencée sur notre site, mais n'a pas de gestionnaire
          enregistré.
        </p>
      </div>
      <CanteenButtonClaim :id="props.id" />
    </div>
    <div v-else-if="status === 'ask-to-join'" class="canteen-establishment-card__tertiary-action fr-mt-1v">
      <div>
        <DsfrBadge type="success" label="cantine déjà existante" small />
        <p class="fr-mb-0 fr-text--xs">
          La cantine avec le numéro SIRET {{ siret }} est déjà référencée sur notre site. Vous n’êtes pas enregistré en
          tant que gestionnaire.
        </p>
      </div>
      <CanteenButtonJoin :id="props.id" :name="props.name" />
    </div>
    <div v-else-if="status === 'not-a-satellite'" class="fr-mt-1w">
      <DsfrBadge type="error" label="Erreur" small />
      <p class="fr-mb-0 fr-mt-1v fr-text--sm">Cet établissement n'est pas de type restaurant satellite, veuillez vous rapprocher du gestionnaire.</p>
    </div>
    <div v-else-if="status === 'other-group'" class="fr-mt-1w">
      <DsfrBadge type="error" label="Erreur" small />
      <p class="fr-mb-0 fr-mt-1v fr-text--sm">Ce restaurant satellite est déjà intégré dans un groupe, veuillez vous rapprocher du gestionnaire.</p>
    </div>
    <div v-else-if="status === 'my-group'" class="fr-mt-1w">
      <DsfrBadge type="success" label="Ce restaurant satellite est dans le groupe" small />
    </div>
    <div v-else-if="status === 'add-satellite'" class="fr-mt-1w">
      <CanteenButtonLink :satId="id" :groupId="groupId" @satelliteAdded="$emit('select')" />
    </div>
  </div>
</template>

<style lang="scss">
.canteen-establishment-card {
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
