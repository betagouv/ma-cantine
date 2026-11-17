<script setup>
import { computed } from "vue"
import { storeToRefs } from "pinia"
import { useStoreTeledeclaration } from "@/stores/teledeclaration"
import documentation from "@/data/documentation.json"
import AppHelpCard from "@/components/AppHelpCard.vue"
import TunnelTeledeclarationButtonReset from "@/components/TunnelTeledeclarationButtonReset.vue"
import TunnelTeledeclarationVoletThematiqueBanner from "@/components/TunnelTeledeclarationVoletThematiqueBanner.vue"
import TunnelTeledeclarationGroupTitle from "@/components/TunnelTeledeclarationGroupTitle.vue"
import TunnelTeledeclarationField from "@/components/TunnelTeledeclarationField.vue"

/* Documentation */
const bouteillesDocumentation = `${documentation.interdictionPlastique}#3-1-interdiction-des-bouteilles-en-plastique-et-obligation-de-mise-a-disposition-de-fontaines-a-eau`
const ustensilesDocumentation = `${documentation.interdictionPlastique}#1-2-interdiction-des-ustensiles-en-plastique-a-usage-unique`
const vaisselleDocumentation = `${documentation.interdictionPlastique}#1-3-obligation-de-vaisselle-reemployable`
const contenantsDocumentation = `${documentation.interdictionPlastique}#1-4-fin-de-lutilisation-des-contenants-alimentaires-de-cuisson-de-rechauffe-et-de-service-en-plastique`
const emporterDocumentation = `${documentation.interdictionPlastique}#1-5-vente-a-emporter`

/* Vente à emporter : les contenants ne sont attendus que si l'établissement propose des repas à emporter */
const storeTeledeclaration = useStoreTeledeclaration()
const { diagnostic } = storeToRefs(storeTeledeclaration)
const isVenteEmporter = computed(() => diagnostic.value.venteEmporter === true)
const updateVenteEmporter = (value) => {
  if (value !== true) storeTeledeclaration.setValue("plastiqueContenantEmporterRemplace", null)
}
</script>

<template>
  <h2>Substitution des plastiques et de l’usage unique</h2>
  <TunnelTeledeclarationVoletThematiqueBanner />
  <div class="fr-grid-row fr-grid-row--gutters fr-grid-row--top fr-mb-4w">
    <div class="fr-col-12 fr-col-md-7">
      <p class="fr-mb-0">
        La mise à disposition de gobelets, de verres et d’assiettes jetables et de nombreux ustensiles en plastique à
        usage unique est interdite pour tout type de restauration (y compris commerciale).
      </p>
    </div>
    <div class="fr-col-12 fr-col-md-5">
      <AppHelpCard title="En savoir plus sur vos obligations">
        <a :href="documentation.interdictionPlastique" target="_blank">Consultez la documentation</a>
      </AppHelpCard>
      <TunnelTeledeclarationButtonReset />
    </div>
  </div>
  <div class="fr-mb-6w ma-cantine--fields-group">
    <TunnelTeledeclarationGroupTitle
      title="Interdiction des bouteilles en plastique et obligation de mise à disposition de fontaines à eau"
      :documentation="bouteillesDocumentation"
    />
    <DsfrHighlight class="fr-ml-0">
      <p>
        <span class="fr-text--bold">Pour l’ensemble des établissements recevant du public :</span><br />
        obligation de mise à disposition d’une fontaine à eau potable et l’interdiction de distribution gratuite de
        bouteilles en plastique
      </p>
      <p>
        <span class="fr-text--bold">Pour les cantines scolaires uniquement :</span><br />
        fin de l'utilisation des bouteilles d'eau plate en plastique
      </p>
    </DsfrHighlight>
    <TunnelTeledeclarationField name="plastiqueBouteilleBoissonRemplace" />
    <TunnelTeledeclarationField name="plastiqueBouteilleRemplace" />
  </div>
  <div class="fr-mb-6w ma-cantine--fields-group">
    <TunnelTeledeclarationGroupTitle
      title="Interdiction des ustensiles en plastique à usage unique"
      :documentation="ustensilesDocumentation"
    />
    <TunnelTeledeclarationField name="plastiqueUstensileRemplace" />
  </div>
  <div class="fr-mb-6w ma-cantine--fields-group">
    <TunnelTeledeclarationGroupTitle title="Obligation de vaisselle réemployable" :documentation="vaisselleDocumentation" />
    <DsfrHighlight class="fr-ml-0">
      <p>
        <span class="fr-text--bold">Établissements concernés :</span><br />
        toute cantine pouvant restaurer simultanément au moins 20 personnes
      </p>
    </DsfrHighlight>
    <TunnelTeledeclarationField name="plastiqueVaisselleJetableRemplace" />
  </div>
  <div class="fr-mb-6w ma-cantine--fields-group">
    <TunnelTeledeclarationGroupTitle
      title="Fin de l’utilisation de contenants de cuisson, réchauffe et service"
      :documentation="contenantsDocumentation"
    />
    <DsfrHighlight class="fr-ml-0">
      <p>
        <span class="fr-text--bold">Établissements concernés :</span><br />
        scolaires et universitaires, accueil d’enfants de moins de six ans, services de pédiatrie, d'obstétrique et de
        maternité, centres périnataux de proximité, services de protection maternelle et infantile.
      </p>
    </DsfrHighlight>
    <TunnelTeledeclarationField name="plastiqueContenantRemplace" />
  </div>
  <div class="fr-mb-6w ma-cantine--fields-group">
    <TunnelTeledeclarationGroupTitle title="Vente à emporter" :documentation="emporterDocumentation" />
    <DsfrHighlight class="fr-ml-0">
      <p>
        <span class="fr-text--bold">Établissements concernés :</span><br />
        tous les services de restauration collective proposant des repas à emporter.
      </p>
    </DsfrHighlight>
    <TunnelTeledeclarationField name="venteEmporter" @change="updateVenteEmporter" />
    <TunnelTeledeclarationField v-if="isVenteEmporter" name="plastiqueContenantEmporterRemplace" />
  </div>
</template>
