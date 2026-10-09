<script setup>
import { ref } from "vue"
import documentation from "@/data/documentation.json"
import TunnelTeledeclarationField from "@/components/TunnelTeledeclarationField.vue"
import AppModalIframe from "@/components/AppModalIframe.vue"

const bioFields = ["valeurBio", "valeurBioDontCommerceEquitable"]
const autresEgalimFields = ["valeurEgalimAutres", "valeurEgalimAutresDontCommerceEquitable"]
const viandeFamilleFields = ["valeurViandesVolailles", "valeurViandesVolaillesEgalim"]
const poissonFamilleFields = ["valeurProduitsDeLaMer", "valeurProduitsDeLaMerEgalim"]
const autresFamillesFields = ["valeurCharcuterie", "valeurFruitsEtLegumes", "valeurProduitsLaitiers", "valeurBoulangerie", "valeurAutres", "valeurBoissons"]

/* Modal */
const siqoDocumentation = `${documentation.qualiteDurabiliteProduits}#3-2-a-5-les-produits-sous-signes-didentification-de-la-qualite-et-de-lorigine-siqo-hors-bio`
const autresEgalimDocumentation = `${documentation.qualiteDurabiliteProduits}#3-6-a-10-les-autres-labels-compatibles-egalim`
const opened = ref(false)
const modal = ref({})
const openModal = (title, src) => {
  modal.value = { title, src }
  opened.value = true
}
</script>
<template>
  <div class="fr-mb-6w">
    <div class="ma-cantine--flex-between ma-cantine--flex-top ma-cantine--flex-gap-1 fr-mb-2w">
      <h3 class="fr-h5 fr-mb-0">Achats bio ou avec mention « en conversion vers l’agriculture biologique »</h3>
      <DsfrButton class="ma-cantine--flex-shrink-0" label="En savoir plus" icon="fr-icon-add-line" icon-right tertiary size="sm" @click="openModal('Achats bio ou avec mention « en conversion vers l’agriculture biologique »', documentation.commerceEquitable)" />
    </div>
    <p>
      Les achats en produits bio et issus du commerce équitable sont à renseigner dans le champ principal (achat bio ou en conversion) et, si vous en avez la possibilité, dans le champ facultatif « [...] dont bio équitable ». Ce sont les seuls achats qui peuvent être comptabilisés dans deux champs distincts de cette étape (double comptabilisation).
    </p>
    <TunnelTeledeclarationField v-for="field in bioFields" :key="field" :name="field" />
  </div>
  <div class="fr-mb-6w">
    <div class="ma-cantine--flex-between ma-cantine--flex-top ma-cantine--flex-gap-1 fr-mb-2w">
      <div>
        <h3 class="fr-h5 fr-mb-1w">Achats SIQO (hors bio)</h3>
        <DsfrBadge label="Nouveauté loi UPSA" type="new" small />
      </div>
      <DsfrButton class="ma-cantine--flex-shrink-0" label="En savoir plus" icon="fr-icon-add-line" icon-right tertiary size="sm" @click="openModal('Achats SIQO (hors bio)', siqoDocumentation)" />
    </div>
    <p>
      SIQO = Signes officiels d'identification de la qualité et de l'origine.
      <br />
      Renseigner ici le montant total des achats SIQO hors bio : Label Rouge, AOC/AOP, IGP, STG
    </p>
    <TunnelTeledeclarationField name="valeurSiqo" />
  </div>
  <div class="fr-mb-6w">
    <div class="ma-cantine--flex-between ma-cantine--flex-top ma-cantine--flex-gap-1 fr-mb-2w">
      <div>
        <h3 class="fr-h5 fr-mb-1w">Autres achats EGalim</h3>
        <DsfrBadge label="Nouveauté loi UPSA" type="new" small />
      </div>
      <DsfrButton class="ma-cantine--flex-shrink-0" label="En savoir plus" icon="fr-icon-add-line" icon-right tertiary size="sm" @click="openModal('Autres achats EGalim', autresEgalimDocumentation)" />
    </div>
    <TunnelTeledeclarationField v-for="field in autresEgalimFields" :key="field" :name="field" />
  </div>
  <div class="fr-mb-6w">
    <div class="ma-cantine--flex-between ma-cantine--flex-top ma-cantine--flex-gap-1 fr-mb-2w">
      <h3 class="fr-h5 fr-mb-0">Approvisionnements sélectionnés via des critères d'achat</h3>
      <DsfrButton class="ma-cantine--flex-shrink-0" label="En savoir plus" icon="fr-icon-add-line" icon-right tertiary size="sm" @click="openModal('Approvisionnements sélectionnés via des critères d’achat', documentation.criteresSelection)" />
    </div>
    <TunnelTeledeclarationField name="valeurExternalitesPerformance" />
  </div>
  <div class="fr-mb-6w">
    <h3 class="fr-h5">Famille de produits « Viandes et volailles fraîches ou surgelées »</h3>
    <TunnelTeledeclarationField v-for="field in viandeFamilleFields" :key="field" :name="field" />
  </div>
  <div class="fr-mb-6w">
    <h3 class="fr-h5">Famille de produits « Poissons, produits de la mer et de l'aquaculture frais et surgelés »</h3>
    <TunnelTeledeclarationField v-for="field in poissonFamilleFields" :key="field" :name="field" />
  </div>
  <div class="fr-mb-6w">
    <h2 class="fr-h5">6. Zoom sur les autres familles</h2>
    <TunnelTeledeclarationField v-for="field in autresFamillesFields" :key="field" :name="field" />
  </div>
  <AppModalIframe :opened="opened" :title="modal.title" :src="modal.src" @close="opened = false" />
</template>
