<script setup>
import documentation from "@/data/documentation.json"
import TunnelTeledeclarationGroupTitle from "@/components/TunnelTeledeclarationGroupTitle.vue"
import TunnelTeledeclarationField from "@/components/TunnelTeledeclarationField.vue"
</script>

<template>
  <div class="fr-mb-6w">
    <TunnelTeledeclarationGroupTitle title="1. Diversification des sources de protéines" :documentation="documentation.diversificationSourcesProteinesObligation" />
    <p>
      Les établissements concernés sont tous les restaurants collectifs servant plus de 200 couverts par jour en
      moyenne, y compris ceux du secteur privé (entreprises, prestataires…)
    </p>
    <TunnelTeledeclarationField name="planDiversificationEnPlace" />
    <TunnelTeledeclarationField name="planDiversificationActions" />
    <p class="fr-text--sm fr-text-mention--grey">
      Pour en savoir plus, veuillez consulter le guide
      <a href="https://ma-cantine.agriculture.gouv.fr/static/documents/2103_plandiversificationproteines_bro.pdf" target="_blank">
        CNRC - Plan pluriannuel de diversification des sources de protéines - cadre général
      </a>
    </p>
  </div>
  <div class="fr-mb-6w">
    <TunnelTeledeclarationGroupTitle title="2. Menu végétarien" :documentation="documentation.menuVegetarienObligation" />
    <p class="fr-mb-1w">Les établissements concernés par des obligations sont :</p>
    <ul class="fr-mb-3w">
      <li>
        <strong>Cantines scolaires de la maternelle au lycée, publics et privés :</strong>
        un menu végétarien obligatoire chaque semaine
      </li>
      <li>
        <strong>Cantines de l’État et ses opérateurs :</strong>
        une option végétarienne quotidienne en cas de choix multiple de menus
      </li>
    </ul>
    <TunnelTeledeclarationField name="serviceType" />
    <TunnelTeledeclarationField name="menuVegetarienFrequence" />
    <TunnelTeledeclarationField name="menuVegetarienBases" />
  </div>
</template>
