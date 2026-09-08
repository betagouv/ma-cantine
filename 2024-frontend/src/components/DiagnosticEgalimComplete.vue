<script setup>
import TunnelTeledeclarationField from "@/components/TunnelTeledeclarationField.vue"
import AppHelpCard from "@/components/AppHelpCard.vue"
import documentation from "@/data/documentation.json"

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
  "valeurBioBoissonsDontCommerceEquitable",
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
  "valeurCoutsExternalitesBoissons",
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
const nonEgalimFields = [
  "valeurViandesVolaillesNonEgalim",
  "valeurProduitsDeLaMerNonEgalim",
  "valeurFruitsEtLegumesNonEgalim",
  "valeurCharcuterieNonEgalim",
  "valeurProduitsLaitiersNonEgalim",
  "valeurBoulangerieNonEgalim",
  "valeurBoissonsNonEgalim",
  "valeurAutresNonEgalim",
]
</script>
<template>
  <div class="fr-mb-4w">
    <h2 class="fr-h5">2. Total des achats par famille de produit</h2>
    <div class="fr-mb-4w fr-grid-row fr-grid-row--gutters">
      <TunnelTeledeclarationField v-for="field in totalAchatsFields" :key="field" :name="field" size="inline" />
    </div>
  </div>
  <div class="fr-mb-4w">
    <h2 class="fr-h5">3. Bio ou en conversion Bio</h2>
    <TunnelTeledeclarationField v-for="field in bioFields" :key="field" :name="field" size="half" />
  </div>
  <div class="fr-mb-4w">
    <h2 class="fr-h5">4. Label rouge</h2>
    <div class="fr-mb-4w fr-grid-row fr-grid-row--gutters">
      <TunnelTeledeclarationField v-for="field in labelRougeFields" :key="field" :name="field" size="inline" />
    </div>
  </div>
  <div class="fr-mb-4w">
    <h2 class="fr-h5">5. AOC / AOP</h2>
    <div class="fr-mb-4w fr-grid-row fr-grid-row--gutters">
      <TunnelTeledeclarationField v-for="field in aocaopFields" :key="field" :name="field" size="inline" />
    </div>
  </div>
  <div class="fr-mb-4w">
    <h2 class="fr-h5">6. IGP</h2>
    <div class="fr-mb-4w fr-grid-row fr-grid-row--gutters">
      <TunnelTeledeclarationField v-for="field in igpFields" :key="field" :name="field" size="inline" />
    </div>
  </div>
  <div class="fr-mb-4w">
    <h2 class="fr-h5">7. STG</h2>
    <div class="fr-mb-4w fr-grid-row fr-grid-row--gutters">
      <TunnelTeledeclarationField v-for="field in stgFields" :key="field" :name="field" size="inline" />
    </div>
  </div>
  <div class="fr-mb-4w">
    <h2 class="fr-h5">8. Certification environnementale - niveau 2 ou 3 (HVE)</h2>
    <div class="fr-grid-row fr-grid-row--gutters fr-grid-row--top fr-mb-4w">
      <div class="fr-col-12 fr-col-md-7">
        <TunnelTeledeclarationField v-for="field in hveFields" :key="field" :name="field" size="full" />
      </div>
      <div class="fr-col-12 fr-col-md-5">
        <AppHelpCard title="Comment comptabiliser les produits avec la certification environnementale (HVE) ?">
          <a :href="documentation.hveCertificationEnvironnementale" target="_blank">Consultez la documentation</a>
        </AppHelpCard>
      </div>
    </div>
  </div>
  <div class="fr-mb-4w">
    <h2 class="fr-h5">9. Ecolabel pêche durable</h2>
    <div class="fr-grid-row fr-grid-row--gutters fr-grid-row--top fr-mb-4w">
      <div class="fr-col-12 fr-col-md-7">
        <TunnelTeledeclarationField v-for="field in pecheDurableFields" :key="field" :name="field" size="full" />
      </div>
      <div class="fr-col-12 fr-col-md-5">
        <AppHelpCard title="Comment comptabiliser les produits de pêche durable ?">
          <a :href="documentation.pecheDurable" target="_blank">Consultez la documentation</a>
          <br />
          <a :href="documentation.mscPeche" target="_blank">Les produits MSC entrent-ils dans les 50% ?</a>
        </AppHelpCard>
      </div>
    </div>
  </div>
  <div class="fr-mb-4w">
    <h2 class="fr-h5">10. RUP</h2>
    <div class="fr-mb-4w fr-grid-row fr-grid-row--gutters">
      <TunnelTeledeclarationField v-for="field in rupFields" :key="field" :name="field" size="inline" />
    </div>
  </div>
  <div class="fr-mb-4w">
    <h2 class="fr-h5">11. Commerce équitable non Bio</h2>
    <div class="fr-grid-row fr-grid-row--gutters fr-grid-row--top fr-mb-4w">
      <div class="fr-col-12 fr-col-md-7">
        <TunnelTeledeclarationField v-for="field in commerceEquitableFields" :key="field" :name="field" size="full" />
      </div>
      <div class="fr-col-12 fr-col-md-5">
        <AppHelpCard title="Comment comptabiliser les produits issus du commerce équitable ?">
          <a :href="documentation.commerceEquitable" target="_blank">Consultez la documentation</a>
        </AppHelpCard>
      </div>
    </div>
  </div>
  <div class="fr-mb-4w">
    <h2 class="fr-h5">12. Produits fermiers ou de montagne</h2>
    <div class="fr-grid-row fr-grid-row--gutters fr-grid-row--top fr-mb-4w">
      <div class="fr-col-12 fr-col-md-7">
        <TunnelTeledeclarationField v-for="field in fermierFields" :key="field" :name="field" size="full" />
      </div>
      <div class="fr-col-12 fr-col-md-5">
        <AppHelpCard title="Comment comptabiliser les produits fermiers ou de montagne ?">
          <a :href="documentation.fermier" target="_blank">Consultez la documentation</a>
        </AppHelpCard>
      </div>
    </div>
  </div>
  <div class="fr-mb-4w">
    <h2 class="fr-h5">13. Critères d’externalités environnementales</h2>
    <div class="fr-grid-row fr-grid-row--gutters fr-grid-row--top fr-mb-4w">
      <div class="fr-col-12 fr-col-md-7">
        <TunnelTeledeclarationField v-for="field in externalitesFields" :key="field" :name="field" size="full" />
      </div>
      <div class="fr-col-12 fr-col-md-5">
        <AppHelpCard title="Comment comptabiliser les produits selon les critères d’externalités environnementales ?">
          <a :href="documentation.externalites" target="_blank">Consultez la documentation</a>
        </AppHelpCard>
      </div>
    </div>
  </div>
  <div class="fr-mb-4w">
    <h2 class="fr-h5">14. Critères de performance environnementale et d’approvisionnements directs</h2>
    <div class="fr-grid-row fr-grid-row--gutters fr-grid-row--top fr-mb-4w">
      <div class="fr-col-12 fr-col-md-7">
        <TunnelTeledeclarationField v-for="field in performanceFields" :key="field" :name="field" size="full" />
      </div>
      <div class="fr-col-12 fr-col-md-5">
        <AppHelpCard title="Comment comptabiliser les produits selon des critères de performance environnementale ?">
          <a :href="documentation.performance" target="_blank">Consultez la documentation</a>
        </AppHelpCard>
      </div>
    </div>
  </div>
  <div class="fr-mb-4w">
    <h2 class="fr-h5">15. Non-EGalim</h2>
    <div class="fr-mb-4w fr-grid-row fr-grid-row--gutters">
      <TunnelTeledeclarationField v-for="field in nonEgalimFields" :key="field" :name="field" size="inline" />
    </div>
  </div>
</template>
