<script setup>
import documentation from "@/data/documentation.json"
import TunnelTeledeclarationField from "@/components/TunnelTeledeclarationField.vue"
import TunnelTeledeclarationGroupTitle from "@/components/TunnelTeledeclarationGroupTitle.vue"

const totalAchatsFields = [
  "valeurViandesVolailles",
  "valeurProduitsDeLaMer",
  "valeurCharcuterie",
  "valeurFruitsEtLegumes",
  "valeurProduitsLaitiers",
  "valeurBoulangerie",
  "valeurAutres",
  "valeurBoissons",
]
const bioFields = [
  "valeurViandesVolaillesBio",
  "valeurViandesVolaillesBioDontCommerceEquitable",
  "valeurProduitsDeLaMerBio",
  "valeurProduitsDeLaMerBioDontCommerceEquitable",
  "valeurCharcuterieBio",
  "valeurCharcuterieBioDontCommerceEquitable",
  "valeurFruitsEtLegumesBio",
  "valeurFruitsEtLegumesBioDontCommerceEquitable",
  "valeurProduitsLaitiersBio",
  "valeurProduitsLaitiersBioDontCommerceEquitable",
  "valeurBoulangerieBio",
  "valeurBoulangerieBioDontCommerceEquitable",
  "valeurAutresBio",
  "valeurAutresBioDontCommerceEquitable",
  "valeurBoissonsBio",
  "valeurBoissonsBioDontCommerceEquitable",
]
const labelRougeFields = [
  "valeurViandesVolaillesLabelRouge",
  "valeurProduitsDeLaMerLabelRouge",
  "valeurCharcuterieLabelRouge",
  "valeurFruitsEtLegumesLabelRouge",
  "valeurProduitsLaitiersLabelRouge",
  "valeurBoulangerieLabelRouge",
  "valeurAutresLabelRouge",
]
const aocaopFields = [
  "valeurViandesVolaillesAocaop",
  "valeurProduitsDeLaMerAocaop",
  "valeurCharcuterieAocaop",
  "valeurFruitsEtLegumesAocaop",
  "valeurProduitsLaitiersAocaop",
  "valeurBoulangerieAocaop",
  "valeurAutresAocaop",
  "valeurBoissonsAocaop",
]
const igpFields = [
  "valeurViandesVolaillesIgp",
  "valeurProduitsDeLaMerIgp",
  "valeurCharcuterieIgp",
  "valeurFruitsEtLegumesIgp",
  "valeurProduitsLaitiersIgp",
  "valeurBoulangerieIgp",
  "valeurAutresIgp",
  "valeurBoissonsIgp",
]
const stgFields = [
  "valeurViandesVolaillesStg",
  "valeurProduitsDeLaMerStg",
  "valeurCharcuterieStg",
  "valeurFruitsEtLegumesStg",
  "valeurProduitsLaitiersStg",
  "valeurBoulangerieStg",
  "valeurAutresStg",
  "valeurBoissonsStg",
]
const hveFields = [
  "valeurViandesVolaillesHve",
  "valeurProduitsDeLaMerHve",
  "valeurCharcuterieHve",
  "valeurFruitsEtLegumesHve",
  "valeurProduitsLaitiersHve",
  "valeurBoulangerieHve",
  "valeurAutresHve",
  "valeurBoissonsHve",
]
const pecheDurableFields = ["valeurProduitsDeLaMerPecheDurable"]
const rupFields = [
  "valeurViandesVolaillesRup",
  "valeurProduitsDeLaMerRup",
  "valeurCharcuterieRup",
  "valeurFruitsEtLegumesRup",
  "valeurProduitsLaitiersRup",
  "valeurBoulangerieRup",
  "valeurAutresRup",
  "valeurBoissonsRup",
]
const commerceEquitableFields = [
  "valeurViandesVolaillesCommerceEquitable",
  "valeurProduitsDeLaMerCommerceEquitable",
  "valeurCharcuterieCommerceEquitable",
  "valeurFruitsEtLegumesCommerceEquitable",
  "valeurProduitsLaitiersCommerceEquitable",
  "valeurBoulangerieCommerceEquitable",
  "valeurAutresCommerceEquitable",
  "valeurBoissonsCommerceEquitable",
]
const fermierFields = [
  "valeurViandesVolaillesFermier",
  "valeurProduitsDeLaMerFermier",
  "valeurCharcuterieFermier",
  "valeurFruitsEtLegumesFermier",
  "valeurProduitsLaitiersFermier",
  "valeurBoulangerieFermier",
  "valeurAutresFermier",
  "valeurBoissonsFermier",
]
const externalitesFields = [
  "valeurViandesVolaillesExternalites",
  "valeurProduitsDeLaMerExternalites",
  "valeurCharcuterieExternalites",
  "valeurFruitsEtLegumesExternalites",
  "valeurProduitsLaitiersExternalites",
  "valeurBoulangerieExternalites",
  "valeurAutresExternalites",
  "valeurBoissonsExternalites",
]
const performanceFields = [
  "valeurViandesVolaillesPerformance",
  "valeurProduitsDeLaMerPerformance",
  "valeurCharcuteriePerformance",
  "valeurFruitsEtLegumesPerformance",
  "valeurProduitsLaitiersPerformance",
  "valeurBoulangeriePerformance",
  "valeurAutresPerformance",
  "valeurBoissonsPerformance",
]

/* Logos */
const logosFolder = "/static/images/quality-labels"
const bioImage = `${logosFolder}/egalim-bio.jpg`
const labelRougeImage = `${logosFolder}/label-rouge.png`
const aocaopImage = `${logosFolder}/Logo-AOC-AOP.png`
const igpImage = `${logosFolder}/IGP.png`
const stgImage = `${logosFolder}/STG.png`
const hveImage = `${logosFolder}/hve.png`
const rupImage = `${logosFolder}/rup.png`
</script>
<template>
  <div class="fr-mb-6w">
    <TunnelTeledeclarationGroupTitle title="1. Total des achats par famille de produits" />
    <div class="fr-grid-row fr-grid-row--gutters">
      <div v-for="field in totalAchatsFields" :key="field" class="fr-col-12 fr-col-md-6">
        <TunnelTeledeclarationField :name="field" />
      </div>
    </div>
  </div>
  <div class="fr-mb-6w">
    <TunnelTeledeclarationGroupTitle
      title="2. Achats bio ou avec mention « en conversion vers l’agriculture biologique », par famille de produits"
      :logo="bioImage"
      logo-alt="Label bio"
      :documentation="documentation.commerceEquitable"
    />
    <p>
      Les achats en produits bio et issus du commerce équitable sont à renseigner dans le champ principal (achat bio ou en conversion), par famille. Si vous en avez la possibilité, vous pouvez également les comptabiliser dans le champ facultatif « [...] dont bio équitable ». Les achats bio issus du commerce équitable sont ainsi les seuls achats qui peuvent être comptabilisés dans deux champs distincts de cette étape (double comptabilisation).
    </p>
    <div class="fr-grid-row fr-grid-row--gutters">
      <div v-for="field in bioFields" :key="field" class="fr-col-12 fr-col-md-6">
        <TunnelTeledeclarationField :name="field" />
      </div>
    </div>
  </div>
  <div class="fr-mb-6w">
    <TunnelTeledeclarationGroupTitle title="3. Label rouge, par famille de produits" :logo="labelRougeImage" logo-alt="Label rouge" />
    <div class="fr-grid-row fr-grid-row--gutters">
      <div v-for="field in labelRougeFields" :key="field" class="fr-col-12 fr-col-md-6">
        <TunnelTeledeclarationField :name="field" />
      </div>
    </div>
  </div>
  <div class="fr-mb-6w">
    <TunnelTeledeclarationGroupTitle title="4. AOC / AOP, par famille de produits" :logo="aocaopImage" logo-alt="Labels AOC et AOP" />
    <div class="fr-grid-row fr-grid-row--gutters">
      <div v-for="field in aocaopFields" :key="field" class="fr-col-12 fr-col-md-6">
        <TunnelTeledeclarationField :name="field" />
      </div>
    </div>
  </div>
  <div class="fr-mb-6w">
    <TunnelTeledeclarationGroupTitle title="5. IGP, par famille de produits" :logo="igpImage" logo-alt="Label IGP" />
    <div class="fr-grid-row fr-grid-row--gutters">
      <div v-for="field in igpFields" :key="field" class="fr-col-12 fr-col-md-6">
        <TunnelTeledeclarationField :name="field" />
      </div>
    </div>
  </div>
  <div class="fr-mb-6w">
    <TunnelTeledeclarationGroupTitle title="6. STG, par famille de produits" :logo="stgImage" logo-alt="Label STG" />
    <div class="fr-grid-row fr-grid-row--gutters">
      <div v-for="field in stgFields" :key="field" class="fr-col-12 fr-col-md-6">
        <TunnelTeledeclarationField :name="field" />
      </div>
    </div>
  </div>
  <div class="fr-mb-6w">
    <TunnelTeledeclarationGroupTitle
      title="7. Certification environnementale de niveau 2 ou 3 (Haute Valeur Environnementale - HVE), par famille de produits"
      badge="Nouveauté loi UPSA"
      :logo="hveImage"
      logo-alt="Label Haute Valeur Environnementale"
      :documentation="documentation.hveCertificationEnvironnementale"
    />
    <p>
      En raison de l'intégration de l'HVE dans l'objectif de 30% SIQO/HVE/« fermier », la certification environnementale de niveau 2 (CE2) et le HVE seront deux catégories EGalim distinctes à partir de la télédéclaration 2028. En ce sens, nous vous invitons à initier un suivi séparé des produits CE2 et HVE dès le 1er janvier 2027.
    </p>
    <div class="fr-grid-row fr-grid-row--gutters">
      <div v-for="field in hveFields" :key="field" class="fr-col-12 fr-col-md-6">
        <TunnelTeledeclarationField :name="field" />
      </div>
    </div>
  </div>
  <div class="fr-mb-6w">
    <TunnelTeledeclarationGroupTitle
      title="8. Ecolabel pêche durable, 7°bis ou 7°ter, par famille de produits"
      badge="Nouveauté loi UPSA"
      :documentation="documentation.pecheDurable"
    />
    <p>
      Intégration dans cette catégorie EGalim des produits issus de la pêche (7°bis) ou aquacoles (7°ter) conformes aux exigences de la réglementation européenne et issus d’une démarche collective définie par un cahier des charges garantissant l’origine, la traçabilité et la fraîcheur des produits.
    </p>
    <div class="fr-grid-row fr-grid-row--gutters">
      <div v-for="field in pecheDurableFields" :key="field" class="fr-col-12 fr-col-md-6">
        <TunnelTeledeclarationField :name="field" />
      </div>
    </div>
  </div>
  <div class="fr-mb-6w">
    <TunnelTeledeclarationGroupTitle title="9. RUP, par famille de produits" :logo="rupImage" logo-alt="Logo Région ultrapériphérique" />
    <div class="fr-grid-row fr-grid-row--gutters">
      <div v-for="field in rupFields" :key="field" class="fr-col-12 fr-col-md-6">
        <TunnelTeledeclarationField :name="field" />
      </div>
    </div>
  </div>
  <div class="fr-mb-6w">
    <TunnelTeledeclarationGroupTitle
      title="10. Commerce équitable non bio, par famille de produits"
      :documentation="documentation.commerceEquitable"
    />
    <p>
      Renseigner ici uniquement les achats en produits issus du commerce équitable non bio. Les achats en produits bio équitables sont à renseigner dans les champs « Bio » (obligatoire) ET « Bio issu du commerce équitable » (facultatif, en fonction de vos possibilités de suivi).
    </p>
    <div class="fr-grid-row fr-grid-row--gutters">
      <div v-for="field in commerceEquitableFields" :key="field" class="fr-col-12 fr-col-md-6">
        <TunnelTeledeclarationField :name="field" />
      </div>
    </div>
  </div>
  <div class="fr-mb-6w">
    <TunnelTeledeclarationGroupTitle
      title="11. Produits « fermiers », 3°quater ou 4°bis, par famille de produits"
      badge="Nouveauté loi UPSA"
      :documentation="documentation.fermier"
    />
    <p>
      Les produits répondants aux alinéas 3°quater ou 4°bis de l'article L.230-5-1. du CRPM sont intégrés de manière transitoire à la catégorie « fermier ». En raison de l'intégration des produits « fermiers » dans l'objectif de 30% SIQO/HVE/« fermier », cette catégorie sera divisée en trois catégories distinctes à partir de la télédéclaration 2028. En ce sens, nous vous invitons à réaliser un suivi séparé des produits « fermiers », 3°quater et 4°bis dès le 1er janvier 2027.
    </p>
    <div class="fr-grid-row fr-grid-row--gutters">
      <div v-for="field in fermierFields" :key="field" class="fr-col-12 fr-col-md-6">
        <TunnelTeledeclarationField :name="field" />
      </div>
    </div>
  </div>
  <div class="fr-mb-6w">
    <TunnelTeledeclarationGroupTitle
      title="12. Produits sélectionnés sur la base de critères d’externalités environnementales"
      :documentation="documentation.externalites"
    />
    <div class="fr-grid-row fr-grid-row--gutters">
      <div v-for="field in externalitesFields" :key="field" class="fr-col-12 fr-col-md-6">
        <TunnelTeledeclarationField :name="field" />
      </div>
    </div>
  </div>
  <div class="fr-mb-6w">
    <TunnelTeledeclarationGroupTitle
      title="13. Produits sélectionnés sur la base de critères de performance environnementale et d’approvisionnements directs"
      :documentation="documentation.performance"
    />
    <div class="fr-grid-row fr-grid-row--gutters">
      <div v-for="field in performanceFields" :key="field" class="fr-col-12 fr-col-md-6">
        <TunnelTeledeclarationField :name="field" />
      </div>
    </div>
  </div>
</template>
