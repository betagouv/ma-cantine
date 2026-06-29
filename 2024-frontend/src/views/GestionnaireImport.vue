<script setup>
import { computed } from "vue"
import { useRoute } from "vue-router"
import { useRootStore } from "@/stores/root"
import ImportCard from "@/components/ImportCard.vue"
import AppLinkRouter from "@/components/AppLinkRouter.vue"

/* Picto */
const canteenPicto = "/static/images/picto-dsfr/companie.svg"
const purchasesPicto = "/static/images/picto-dsfr/food.svg"
const diagnosticsPicto = "/static/images/picto-dsfr/money.svg"

/* Data */
const route = useRoute()
const store = useRootStore()

/* Links */
const canteenLinks = computed(() => {
  const links = [
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
    links.push({
      label: "Ajouter des gestionnaires",
      icon: "fr-icon-user-add-fill",
      route: "GestionnaireImportCantinesGestionnaires",
      description: "Uniquement pour les administrateurs et les cantines avec un numéro SIRET.",
    })
  }
  return links
})

const purchasesLinks = [
  {
    label: "Créer des achats pour des cantines avec SIRET",
    icon: "fr-icon-add-line",
    route: "GestionnaireImportAchatsSIRET",
  },
  {
    label: "Créer des achats pour des groupes ou cantines sans SIRET",
    icon: "fr-icon-add-line",
    route: "GestionnaireImportAchatsID",
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
  <section class="fr-mt-4w">
    <ImportCard title="Cantines" :icon="canteenPicto" :buttons="canteenLinks">
      <template #callout>
        <p class="fr-text--sm">Il n'est pas possible d'utiliser ces imports pour des groupes de restaurants satellites.</p>
      </template>
    </ImportCard>

    <ImportCard title="Achats" :icon="purchasesPicto" :buttons="purchasesLinks">
      <template #callout>
        <p class="fr-mb-1w fr-text--sm">Le format de données des imports achats à été modifié en 2026. L'import avec l'ancien format reste disponible sur les pages suivantes : </p>
        <ul>
          <li>
            <AppLinkRouter class="fr-text--sm" :to="{name: 'GestionnaireImportAchatsIDOld'}" title="Créer des achats pour des cantines avec SIRET (ancien format)" />
          </li>
          <li>
            <AppLinkRouter class="fr-text--sm" :to="{name: 'GestionnaireImportAchatsIDOld'}" title="Créer des achats pour des groupes ou cantines sans SIRET (ancien format)" />
          </li>
        </ul>
        <p class="fr-mt-2w fr-text--sm">À la fin de la campagne de télédéclaration 2027 ces pages seront supprimées.</p>
      </template>
    </ImportCard>

    <ImportCard
      title="Bilans"
      :icon="diagnosticsPicto"
    >
      <template #disabled>
        <p>
          L'import de bilans est possible uniquement lors des campagnes de télédéclaration EGalim. <br/>
          Les bilans de l'année n ne peuvent être importés qu'en début d'année n+1.
        </p>
      </template>
    </ImportCard>
  </section>
</template>
