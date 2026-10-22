<script setup>
import documentation from "@/data/documentation.json"
import TunnelTeledeclarationField from "@/components/TunnelTeledeclarationField.vue"
import TunnelTeledeclarationGroupTitle from "@/components/TunnelTeledeclarationGroupTitle.vue"

const bioFields = ["valeurBio", "valeurBioDontCommerceEquitable"]
const autresEgalimFields = ["valeurEgalimAutres", "valeurEgalimAutresDontCommerceEquitable"]
const viandeFamilleFields = ["valeurViandesVolailles", "valeurViandesVolaillesEgalim"]
const poissonFamilleFields = ["valeurProduitsDeLaMer", "valeurProduitsDeLaMerEgalim"]

/* Liens */
const bioImage = "/static/images/quality-labels/egalim-bio.jpg"
const siqoImage = "/static/images/quality-labels/egalim-siqo.jpg"
const siqoDocumentation = `${documentation.qualiteDurabiliteProduits}#3-2-a-5-les-produits-sous-signes-didentification-de-la-qualite-et-de-lorigine-siqo-hors-bio`
const autresEgalimDocumentation = `${documentation.qualiteDurabiliteProduits}#3-6-a-10-les-autres-labels-compatibles-egalim`
</script>
<template>
  <div class="fr-mb-6w">
    <TunnelTeledeclarationGroupTitle
      title="Achats bio ou avec mention « en conversion vers l’agriculture biologique »"
      :logo="bioImage"
      logo-alt="Label bio"
      :documentation="documentation.commerceEquitable"
    />
    <p>
      Les achats en produits bio et issus du commerce équitable sont à renseigner dans le champ principal (achat bio ou en conversion) et, si vous en avez la possibilité, dans le champ facultatif « [...] dont bio équitable ». Ce sont les seuls achats qui peuvent être comptabilisés dans deux champs distincts de cette étape (double comptabilisation).
    </p>
    <div class="fr-grid-row fr-grid-row--gutters">
      <div v-for="field in bioFields" :key="field" class="fr-col-12 fr-col-md-6">
        <TunnelTeledeclarationField :name="field" />
      </div>
    </div>
  </div>
  <div class="fr-mb-6w">
    <TunnelTeledeclarationGroupTitle
      title="Achats SIQO (hors bio)"
      badge="Nouveauté loi UPSA"
      :logo="siqoImage"
      logo-alt="Labels SIQO : Label Rouge, AOC, AOP, IGP, STG"
      :documentation="siqoDocumentation"
    />
    <p>
      SIQO = Signes officiels d'identification de la qualité et de l'origine.
      <br />
      Renseigner ici le montant total des achats SIQO hors bio : Label Rouge, AOC/AOP, IGP, STG
    </p>
    <div class="fr-grid-row fr-grid-row--gutters">
      <div class="fr-col-12 fr-col-md-6">
        <TunnelTeledeclarationField name="valeurSiqo" />
      </div>
    </div>
  </div>
  <div class="fr-mb-6w">
    <TunnelTeledeclarationGroupTitle title="Famille de produits « Viandes et volailles fraîches ou surgelées »" />
    <div class="fr-grid-row fr-grid-row--gutters">
      <div v-for="field in viandeFamilleFields" :key="field" class="fr-col-12 fr-col-md-6">
        <TunnelTeledeclarationField :name="field" />
      </div>
    </div>
  </div>
  <div class="fr-mb-6w">
    <TunnelTeledeclarationGroupTitle
      title="Autres achats EGalim"
      badge="Nouveauté loi UPSA"
      :documentation="autresEgalimDocumentation"
    />
    <div class="fr-grid-row fr-grid-row--gutters">
      <div v-for="field in autresEgalimFields" :key="field" class="fr-col-12 fr-col-md-6">
        <TunnelTeledeclarationField :name="field" />
      </div>
    </div>
  </div>
  <div class="fr-mb-6w">
    <TunnelTeledeclarationGroupTitle
      title="Approvisionnements sélectionnés via des critères d'achat"
      :documentation="documentation.criteresSelection"
    />
    <p>
      Critères d'achat : total des achats réalisés selon des modalités de sélection prenant en compte les coûts imputés aux externalités environnementales ou les performances environnementales et d’approvisionnements directs
    </p>
    <div class="fr-grid-row fr-grid-row--gutters">
      <div class="fr-col-12 fr-col-md-6">
        <TunnelTeledeclarationField name="valeurExternalitesPerformance" />
      </div>
    </div>
  </div>
  <div class="fr-mb-6w">
    <TunnelTeledeclarationGroupTitle title="Famille de produits « Poissons, produits de la mer et de l'aquaculture frais et surgelés »" />
    <div class="fr-grid-row fr-grid-row--gutters">
      <div v-for="field in poissonFamilleFields" :key="field" class="fr-col-12 fr-col-md-6">
        <TunnelTeledeclarationField :name="field" />
      </div>
    </div>
  </div>
</template>
