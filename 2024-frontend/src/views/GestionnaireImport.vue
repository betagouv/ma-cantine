<script setup>
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

const gotTo = (name) => {
  router.push({ name: name })
}
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
      <ImportCard title="Cantines" :icon="canteenPicto">
        <div class="fr-mb-2w">
          <DsfrButton tertiary label="Créer des cantines" icon="fr-icon-add-line" @click="gotTo('GestionnaireImportCantinesCreer')" />
          <p class="fr-text--xs fr-mb-0">Uniquement pour les cantines avec un numéro SIRET.</p>
        </div>
        <div class="fr-mb-2w">
          <DsfrButton tertiary label="Modifier des cantines" icon="fr-icon-edit-fill" @click="gotTo('GestionnaireImportCantinesModifier')" />
        </div>
        <div v-if="store.loggedUser.isStaff">
          <DsfrButton tertiary label="Ajouter des gestionnaires" @click="gotTo('GestionnaireImportCantinesGestionnaires')" icon="fr-icon-user-add-fill"/>
          <p class="fr-text--xs">Uniquement pour les administrateurs et les cantines avec un numéro SIRET.</p>
        </div>
        <DsfrCallout class="fr-mb-0">
          <p class="fr-text--sm">Il n'est pas possible d'utiliser les imports ci-dessous pour des groupes de restaurants satellites.</p>
        </DsfrCallout>
      </ImportCard>
    </div>

    <div class="fr-col-12 fr-col-md-4">
      <ImportCard title="Achats" :icon="purchasesPicto">
        <div class="fr-mb-2w">
          <DsfrButton tertiary label="Créer des achats pour des cantines avec SIRET" icon="fr-icon-shopping-cart-2-fill" @click="gotTo('GestionnaireImportAchatsSIRET')" />
        </div>
        <div class="fr-mb-2w">
          <DsfrButton tertiary label="Créer des achats pour des groupes ou cantines sans SIRET" icon="fr-icon-shopping-cart-2-fill" @click="gotTo('GestionnaireImportAchatsID')" />
        </div>
        <DsfrCallout class="fr-mb-0" >
            <p class="fr-mb-1w fr-text--sm">Le format de données des imports achats à été modifié en 2026. Le précédent format reste disponible sur ces pages : </p>
            <DsfrButton size="sm" tertiary label="Créer des achats pour des cantines avec SIRET (ancien&nbsp;format)" @click="gotTo('GestionnaireImportAchatsIDOld')" />
            <DsfrButton size="sm" tertiary label="Créer des achats pour des groupes ou cantines sans SIRET (ancien&nbsp;format)"  @click="gotTo('GestionnaireImportAchatsIDOld')" />
            <p class="fr-mt-2w fr-text--sm">À la fin de la campagne de télédéclaration 2027 ces pages d'imports seront supprimées.</p>
        </DsfrCallout>
      </ImportCard>
    </div>

    <div class="fr-col-12 fr-col-md-4">
      <ImportCard title="Bilans" :icon="diagnosticsPicto">
        <div class="fr-mb-2w">
          <DsfrButton tertiary label="Renseigner saisie simplifiée pour des cantines avec SIRET" icon="fr-icon-file-text-line" @click="gotTo('GestionnaireImportBilansSimplesSIRET')" />
        </div>
        <div class="fr-mb-2w">
          <DsfrButton tertiary label="Renseigner saisie simplifiée pour des groupes ou cantines sans SIRET" icon="fr-icon-file-text-line" @click="gotTo('GestionnaireImportBilansSimples')" />
        </div>
        <div class="fr-mb-2w">
          <DsfrButton tertiary label="Renseigner saisie détaillée" icon="fr-icon-file-text-fill" @click="gotTo('GestionnaireImportBilansDetailles')" />
          <p class="fr-text--xs fr-mb-0">Uniquement pour les cantines avec un numéro SIRET.</p>
        </div>
        <DsfrCallout class="fr-mb-0">
          <p class="fr-text--sm">Si vous connaissez le total des achats par catégorie EGalim et familles de produits, vous pouvez utiliser la saisie détaillée, sinon utilisez la saisie simplifiée.</p>
        </DsfrCallout>
      </ImportCard>
    </div>
  </section>
</template>
