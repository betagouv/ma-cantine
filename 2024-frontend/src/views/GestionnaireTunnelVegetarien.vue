<script setup>
import documentation from "@/data/documentation.json"
import AppHelpCard from "@/components/AppHelpCard.vue"
import TunnelTeledeclarationGroupTitle from "@/components/TunnelTeledeclarationGroupTitle.vue"
import TunnelTeledeclarationField from "@/components/TunnelTeledeclarationField.vue"
</script>

<template>
  <h2>Diversification des sources de protéines <br /> et menus végétariens</h2>
  <div class="fr-grid-row fr-grid-row--gutters fr-grid-row--top fr-mb-4w">
    <div class="fr-col-12 fr-col-md-7">
      <p class="fr-mb-1w">
        Ce volet de la télédéclaration permet de s’auto-évaluer et informer vos convives en regard des obligations de
        la loi :
      </p>
      <ul class="fr-mb-2w">
        <li>
          <strong>diversification des sources de protéines</strong> : obligatoire pour les restaurants collectifs servant plus de 200
          couverts par jour en moyenne
        </li>
        <li><strong>menu végétarien hebdomadaire</strong> : cantines scolaires de la maternelle au lycée</li>
        <li>
          <strong>option végétarienne quotidienne en cas de choix multiple de menus</strong> : cantines de l’État et de ses opérateurs
        </li>
      </ul>
      <p class="fr-mb-0">
        En télédéclarant ce volet, vous contribuez à l’Observatoire EGalim en restauration collective et aux
        statistiques du rapport annuel au Parlement (données anonymisées).
      </p>
    </div>
    <div class="fr-col-12 fr-col-md-5">
      <AppHelpCard title="En savoir plus sur ce volet thématique">
        <ul class="ma-cantine--unstyled-list fr-mb-0">
          <li class="fr-mb-1w">
            <a :href="documentation.diversificationSourcesProteinesMenusVegetariens" target="_blank">Consultez la documentation</a>
          </li>
          <li>
            Pour en savoir plus sur le plan pluriannuel de diversification des sources de protéines, veuillez consulter
            <a href="https://ma-cantine.agriculture.gouv.fr/static/documents/2103_plandiversificationproteines_bro.pdf" target="_blank">
              le guide CNRC
            </a>
          </li>
        </ul>
      </AppHelpCard>
    </div>
  </div>
  <div class="fr-mb-6w">
    <TunnelTeledeclarationGroupTitle title="Diversification des sources de protéines" :documentation="documentation.diversificationSourcesProteinesObligation" />
    <TunnelTeledeclarationField name="planDiversificationEnPlace" />
    <TunnelTeledeclarationField name="planDiversificationActions" />
  </div>
  <div class="fr-mb-6w">
    <TunnelTeledeclarationGroupTitle title="Menu végétarien" :documentation="documentation.menuVegetarienObligation" />
    <TunnelTeledeclarationField name="serviceType" />
    <TunnelTeledeclarationField name="menuVegetarienFrequence" />
    <TunnelTeledeclarationField name="menuVegetarienBases" />
  </div>
</template>
