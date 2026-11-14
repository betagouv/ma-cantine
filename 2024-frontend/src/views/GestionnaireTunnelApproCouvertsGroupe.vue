<script setup>
import documentation from "@/data/documentation.json"
import AppHelpCard from "@/components/AppHelpCard.vue"
import TunnelTeledeclarationCallout from "@/components/TunnelTeledeclarationCallout.vue"
import TunnelTeledeclarationLockedInput from "@/components/TunnelTeledeclarationLockedInput.vue"
</script>

<template>
  <div class="fr-grid-row fr-grid-row--gutters">
    <div class="fr-col-12 fr-col-md-7">
      <h2>Estimer le nombre de couverts de mon groupe</h2>
      <p>Vous devez renseigner le nombre annuel moyen et dans un second temps, détailler la répartition entre toutes les cantines du groupe l’ajuster à l’aide du tableau ou du fichier d’import dédié.</p>
      <p>Par défaut, le nombre de couverts de chaque cantine est prérempli à partir des précédentes télédéclarations.</p>
    </div>
    <div class="fr-col-12 fr-col-md-5">
      <AppHelpCard title="Ajuster mes établissements">
        <ul class="ma-cantine--unstyled-list">
          <li><a target="_blank" :href="documentation.calculerNombreCouverts">Utiliser l’outil de calcul</a></li>
          <li><a target="_blank" :href="documentation.couvertsGroupeCantineManquante">Il me manque une cantine dans ma répartition de couvert, que faire ?</a></li>
        </ul>
      </AppHelpCard>
    </div>
  </div>
  <div class="fr-mt-4w">
    <h3>Renseigner la répartition de mes couverts annuels entre mes cantines :</h3>
    <p>Pour avoir une donnée de qualité vous devez ajuster la répartition du nombre de couvert pour chaque cantine, votre estimation et la répartition des couverts entre vos établissement doit correspondre. Elle peut se faire manuellement, ou via fichier d’import dédié.</p>
    <TunnelTeledeclarationCallout>
      <div class="fr-grid-row fr-grid-row--gutters fr-grid-row--middle">
        <div class="fr-col-12 fr-col-md-10">
          <p class="fr-mb-0">Total des couverts annuels répartis entre vos cantines</p>
          <p class="fr-text--sm fr-text-mention--grey fr-mb-0">A partir des données couverts de chaque restaurant</p>
        </div>
        <div class="fr-col-12 fr-col-md-2">
          <TunnelTeledeclarationLockedInput :value="0" label="Total des couverts annuels répartis entre vos cantines" />
        </div>
      </div>
    </TunnelTeledeclarationCallout>
  </div>
</template>
