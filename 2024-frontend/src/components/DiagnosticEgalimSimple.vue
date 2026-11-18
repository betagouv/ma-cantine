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
const bioDocumentation = `${documentation.qualiteDurabiliteProduits}#3-1-les-produits-issus-de-lagriculture-biologique-bio`
const siqoDocumentation = `${documentation.qualiteDurabiliteProduits}#3-2-a-5-les-produits-sous-signes-didentification-de-la-qualite-et-de-lorigine-siqo-hors-bio`
const autresEgalimDocumentation = `${documentation.qualiteDurabiliteProduits}#3-6-a-10-les-autres-labels-compatibles-egalim`
</script>
<template>
  <div class="fr-mb-6w">
    <TunnelTeledeclarationGroupTitle
      title="Achats bio ou avec mention « en conversion vers l’agriculture biologique »"
      :logo="bioImage"
      logo-alt="Label bio"
      :documentation="bioDocumentation"
    />
    <p>
      Renseignez ici la totalité de vos achats bio ou « en conversion vers l’agriculture biologique ». Pour le champ facultatif « Dont achats bio issus du commerce équitable », indiquez le montant de la part « commerce équitable » de vos achats bio. Ex : vous avez acheté 50€ de tomates bio et 50€ de café bio et équitable donc vous devez renseigner 100€ dans le total des achats bio et 50€ dans le champ « Dont achats bio issus du commerce équitable ».
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
      :logo="siqoImage"
      logo-alt="Labels SIQO : Label Rouge, AOC, AOP, IGP, STG"
      :documentation="siqoDocumentation"
    />
    <p>
      SIQO = Signes officiels d'identification de la qualité et de l'origine.
      <br />
      Renseignez ici le montant total des achats SIQO hors bio : Label Rouge, AOC/AOP, IGP, STG
    </p>
    <div class="fr-grid-row fr-grid-row--gutters">
      <div class="fr-col-12 fr-col-md-6">
        <TunnelTeledeclarationField name="valeurSiqo" />
      </div>
    </div>
  </div>
  <div class="fr-mb-6w">
    <TunnelTeledeclarationGroupTitle title="Famille de produits « Viandes et volailles fraîches et surgelées »" />
    <div class="fr-grid-row fr-grid-row--gutters">
      <div v-for="field in viandeFamilleFields" :key="field" class="fr-col-12 fr-col-md-6">
        <TunnelTeledeclarationField :name="field" />
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
  <div class="fr-mb-6w">
    <TunnelTeledeclarationGroupTitle
      title="Autres achats EGalim"
      badge="Nouveauté loi UPSA"
      :documentation="autresEgalimDocumentation"
    />
    <p>
      Renseignez ici la totalité de vos autres achats compatibles EGalim (HVE, CE2, RUP, Écolabel pêche durable, « produit de la ferme », commerce équitable, etc.) non comptabilisables dans les champs Bio et SIQO (hors bio) précédents. Pour le champ facultatif « Dont achats issus du commerce équitable », indiquez le montant de la part « commerce équitable » de vos achats compatibles EGalim non bio et non SIQO (hors bio). Ex : vous avez acheté 50€ de poissons Écolabel pêche durable, 25€ de haricots verts RUP et 25€ de sucre du commerce équitable, vous devez renseigner 100€ dans le total des autres achats EGalim et 25€ dans « Dont total des achats non bio non SIQO (hors bio) issus du commerce équitable »
    </p>
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
      Pour les produits répondant à des critères d'achat dans le cadre d’un marché public. Ces achats sont réalisés selon des modalités de sélection prenant en compte les coûts imputés aux externalités environnementales ou les performances environnementales et d’approvisionnements directs.
    </p>
    <div class="fr-grid-row fr-grid-row--gutters">
      <div class="fr-col-12 fr-col-md-6">
        <TunnelTeledeclarationField name="valeurExternalitesPerformance" />
      </div>
    </div>
  </div>
</template>
