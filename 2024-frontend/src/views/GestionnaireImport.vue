<script setup>
import { computed } from "vue"
import { useRoute, useRouter } from "vue-router"
import { useRootStore } from "@/stores/root"
import ImportCard from "@/components/ImportCard.vue"

const router = useRouter()

/* Picto */
const canteenPicto = "/static/images/picto-dsfr/companie.svg"
const purchasesPicto = "/static/images/picto-dsfr/food.svg"
const diagnosticsPicto = "/static/images/picto-dsfr/money.svg"

/* Data */
const route = useRoute()
const store = useRootStore()

const goTo = (name) => router.push({ name })

const canteenButtons = computed(() => {
  const buttons = [
    {
      label: "Créer des cantines",
      icon: "fr-icon-add-line",
      route: "GestionnaireImportCantinesCreer",
      description: "Uniquement pour les cantines avec un numéro SIRET.",
    },
    {
      label: "Modifier des cantines",
      icon: "fr-icon-edit-fill",
      route: "GestionnaireImportCantinesModifier",
    },
  ]
  if (store.loggedUser.isStaff) {
    buttons.push({
      label: "Ajouter des gestionnaires",
      icon: "fr-icon-user-add-fill",
      route: "GestionnaireImportCantinesGestionnaires",
      description: "Uniquement pour les administrateurs et les cantines avec un numéro SIRET.",
    })
  }
  return buttons
})

const purchasesButtons = [
  {
    label: "Créer des achats pour des cantines avec SIRET",
    icon: "fr-icon-shopping-cart-2-fill",
    route: "GestionnaireImportAchatsSIRET",
  },
  {
    label: "Créer des achats pour des groupes ou cantines sans SIRET",
    icon: "fr-icon-shopping-cart-2-fill",
    route: "GestionnaireImportAchatsID",
  },
]

const diagnosticsButtons = [
  {
    label: "Renseigner saisie simplifiée pour des cantines avec SIRET",
    icon: "fr-icon-file-text-line",
    route: "GestionnaireImportBilansSimplesSIRET",
  },
  {
    label: "Renseigner saisie simplifiée pour des groupes ou cantines sans SIRET",
    icon: "fr-icon-file-text-line",
    route: "GestionnaireImportBilansSimples",
  },
  {
    label: "Renseigner saisie détaillée",
    icon: "fr-icon-file-text-fill",
    route: "GestionnaireImportBilansDetailles",
    description: "Uniquement pour les cantines avec un numéro SIRET.",
  },
]
</script>

<template>
  <section class="gestionnaire-import fr-col-12 fr-col-md-7">
    <h1>{{ route.meta.title }}</h1>
    <p>
      Notre solution d'import par tableur vous permet d'importer vos données directement dans <em>ma cantine</em> pour les établissements dont vous êtes gestionnaire.
      Nous acceptons les fichiers au format <DsfrBadge class="fr-mr-1v" type="info" label="Excel" no-icon /> ou
      <DsfrBadge class="fr-mr-1v" type="info" label="CSV" no-icon />.
    </p>
  </section>
  <section class="fr-grid-row fr-grid-row--gutters fr-grid-row--top fr-mt-4w">
    <div class="fr-col-12 fr-col-md-4">
      <ImportCard title="Cantines" :icon="canteenPicto" :buttons="canteenButtons">
        <template #callout>
          <p class="fr-text--sm">Il n'est pas possible d'utiliser les imports ci-dessous pour des groupes de restaurants satellites.</p>
        </template>
      </ImportCard>
    </div>

    <div class="fr-col-12 fr-col-md-4">
      <ImportCard title="Achats" :icon="purchasesPicto" :buttons="purchasesButtons">
        <template #callout>
          <p class="fr-mb-1w fr-text--sm">Le format de données des imports achats à été modifié en 2026. Le précédent format reste disponible sur ces pages : </p>
          <DsfrButton size="sm" tertiary label="Créer des achats pour des cantines avec SIRET (ancien&nbsp;format)" @click="goTo('GestionnaireImportAchatsIDOld')" />
          <DsfrButton size="sm" tertiary label="Créer des achats pour des groupes ou cantines sans SIRET (ancien&nbsp;format)" @click="goTo('GestionnaireImportAchatsIDOld')" />
          <p class="fr-mt-2w fr-text--sm">À la fin de la campagne de télédéclaration 2027 ces pages d'imports seront supprimées.</p>
        </template>
      </ImportCard>
    </div>

    <div class="fr-col-12 fr-col-md-4">
      <ImportCard title="Bilans" :icon="diagnosticsPicto" :buttons="diagnosticsButtons">
        <template #callout>
          <p class="fr-text--sm">Si vous connaissez le total des achats par catégorie EGalim et familles de produits, vous pouvez utiliser la saisie détaillée, sinon utilisez la saisie simplifiée.</p>
        </template>
      </ImportCard>
    </div>
  </section>
</template>
