<script setup>
import documentation from "@/data/documentation.json"
import AppHelpCard from "@/components/AppHelpCard.vue"
import TunnelTeledeclarationButtonReset from "@/components/TunnelTeledeclarationButtonReset.vue"
import TunnelTeledeclarationVoletThematiqueBanner from "@/components/TunnelTeledeclarationVoletThematiqueBanner.vue"
import TunnelTeledeclarationGroupTitle from "@/components/TunnelTeledeclarationGroupTitle.vue"
import TunnelTeledeclarationField from "@/components/TunnelTeledeclarationField.vue"
import AppFormMentionOptionalFields from "@/components/AppFormMentionOptionalFields.vue"

/* Documentation */
const diversificationDocumentation = `${documentation.diversificationSourcesProteines}#2-1-la-diversification-des-sources-de-proteines-une-obligation-pour-tous-des-200-couverts-par-jour`
const menuVegetarienDocumentation = `${documentation.diversificationSourcesProteines}#2-2-le-menu-vegetarien-une-obligation-ciblee-pour-certains-restaurants-collectifs`
</script>

<template>
  <h2>Diversification des sources de protéines <br /> et menus végétariens</h2>
  <TunnelTeledeclarationVoletThematiqueBanner />
  <div class="fr-grid-row fr-grid-row--gutters fr-grid-row--top fr-mb-4w">
    <div class="fr-col-12 fr-col-md-7">
      <p class="fr-mb-1w">
        Ce volet de la télédéclaration permet de s’auto-évaluer et informer vos convives en regard des obligations de
        la loi.
      </p>
      <p class="fr-mb-0">
        En télédéclarant ce volet, vous contribuez à l’Observatoire EGalim en restauration collective et aux
        statistiques du rapport annuel au Parlement (données anonymisées).
      </p>
      <AppFormMentionOptionalFields class="fr-mt-2w fr-mb-0" />
    </div>
    <div class="fr-col-12 fr-col-md-5">
      <AppHelpCard title="En savoir plus sur vos obligations">
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
      <TunnelTeledeclarationButtonReset />
    </div>
  </div>
  <div class="fr-mb-6w ma-cantine--fields-group">
    <TunnelTeledeclarationGroupTitle title="Diversification des sources de protéines" :documentation="diversificationDocumentation" />
    <DsfrHighlight class="fr-ml-0">
      <p>
        <span class="fr-text--bold">Établissements concernés :</span><br />
        tous les restaurants collectifs servant plus de 200 couverts par jour en moyenne, y compris ceux du secteur privé
        (entreprises, prestataires…).
      </p>
    </DsfrHighlight>
    <TunnelTeledeclarationField name="planDiversificationEnPlace" />
    <TunnelTeledeclarationField name="planDiversificationActions" />
  </div>
  <div class="fr-mb-6w ma-cantine--fields-group">
    <TunnelTeledeclarationGroupTitle title="Menu végétarien" :documentation="menuVegetarienDocumentation" />
    <DsfrHighlight class="fr-ml-0">
      <p>
        <span class="fr-text--bold">Pour les cantines scolaires de la maternelle au lycée :</span><br />
        publics et privés : un menu végétarien obligatoire chaque semaine.
      </p>
      <p>
        <span class="fr-text--bold">Pour les cantines de l’État et ses opérateurs :</span><br />
        une option végétarienne quotidienne en cas de choix multiple de menus.
      </p>
    </DsfrHighlight>
    <TunnelTeledeclarationField name="serviceType" />
    <TunnelTeledeclarationField name="menuVegetarienFrequence" />
    <TunnelTeledeclarationField name="menuVegetarienBases" />
  </div>
</template>
