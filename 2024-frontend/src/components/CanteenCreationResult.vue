<script setup>
defineProps(["name", "siret", "city", "department", "status", "id"])
import AppLinkRouter from "@/components/AppLinkRouter.vue"
</script>

<template>
  <div class="fr-card fr-p-3v">
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
        La cantine avec le numéro SIRET {{ siret }}, existe déjà et fait déjà partie de vos cantines.
        <AppLinkRouter
          :to="{ name: 'DashboardManager', params: { canteenUrlComponent: id } }"
          title="Accéder à sa fiche"
        />
      </p>
    </div>
  </div>
</template>
