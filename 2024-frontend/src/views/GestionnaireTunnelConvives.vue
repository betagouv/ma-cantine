<script setup>
import documentation from "@/data/documentation.json"
import AppHelpCard from "@/components/AppHelpCard.vue"
import TunnelTeledeclarationGroupTitle from "@/components/TunnelTeledeclarationGroupTitle.vue"
import TunnelTeledeclarationField from "@/components/TunnelTeledeclarationField.vue"

/* Documentation */
const informationEgalimDocumentation = `${documentation.informationsConvives}#3-1-information-obligatoire-des-usagers`
const informationNutritionnelleDocumentation = `${documentation.informationsConvives}#3-2-informations-nutritionnelles`
</script>

<template>
  <h2>Information des convives</h2>
  <div class="fr-grid-row fr-grid-row--gutters fr-grid-row--top fr-mb-4w">
    <div class="fr-col-12 fr-col-md-7">
      <p class="fr-mb-1w">
        Vos avancées en regard des objectifs de la loi EGalim doivent faire l’objet d’un affichage permanent à l’entrée
        du restaurant collectif lisible par tous les usager et par communication électronique, actualisé au moins une
        fois par an, les établissements concernées :
      </p>
      <ul class="fr-mb-0">
        <li>
          <span class="fr-text--bold">sur la part des produits EGalim :</span> les restaurants collectifs, publics ou
          privés, y compris les restaurants administratifs ou restaurants d’entreprises.
        </li>
        <li>
          <span class="fr-text--bold">sur l'information nutritionnelle</span> les restaurants collectifs, publics et
          privés, des établissements scolaire et universitaire, des établissements d'accueil des enfants de moins de six
          ans, des établissements de santé, des établissements sociaux et médico-sociaux et des établissements
          pénitentiaires
        </li>
      </ul>
    </div>
    <div class="fr-col-12 fr-col-md-5">
      <AppHelpCard title="Pour en savoir plus sur vos obligations">
        <ul class="ma-cantine--unstyled-list fr-mb-0">
          <li class="fr-mb-1w">Référence juridique : article L. 230-5-1 du Code rural et de la pêche maritime.</li>
          <li class="fr-mb-1w">
            <a :href="documentation.informationsConvivesObligations" target="_blank">Consultez la documentation</a>
          </li>
          <li>
            <a href="https://france-pat.fr/carte-des-pats/" target="_blank">Carte des PAT - France PAT</a>
          </li>
        </ul>
      </AppHelpCard>
    </div>
  </div>
  <div class="fr-mb-6w ma-cantine--fields-group">
    <TunnelTeledeclarationGroupTitle
      title="Information des usagers sur la part des produits EGalim (dont bio) et/ou issus de Projets alimentaires territoriaux"
      :documentation="informationEgalimDocumentation"
    />
    <TunnelTeledeclarationField name="informationAffichagePermanent" />
    <TunnelTeledeclarationField name="informationElectroniqueAnnuelle" />
    <TunnelTeledeclarationField name="informationPartEgalim" />
    <TunnelTeledeclarationField name="informationPartPat" />
  </div>
  <div class="fr-mb-6w ma-cantine--fields-group">
    <TunnelTeledeclarationGroupTitle title="Information nutritionnelle" :documentation="informationNutritionnelleDocumentation" />
    <TunnelTeledeclarationField name="informationConsultationQualite" />
  </div>
</template>
