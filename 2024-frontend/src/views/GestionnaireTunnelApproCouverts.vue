<script setup>
import documentation from "@/data/documentation.json"
import AppHelpCard from "@/components/AppHelpCard.vue"
import TunnelTeledeclarationField from "@/components/TunnelTeledeclarationField.vue"
</script>

<template>
  <div class="fr-grid-row fr-grid-row--gutters">
    <div class="fr-col-12 fr-col-md-7">
      <p>Ce chiffre doit refléter la réalité des approvisionnements sur l’année, en tenant compte des périodes d’ouverture et de fermeture de la cantine et de ce qui compte comme un repas complet ou un repas partiel (petit-déjeuner, collation…).</p>
      <TunnelTeledeclarationField name="nombreRepasAn"/>
    </div>
    <div class="fr-col-12 fr-col-md-5">
      <AppHelpCard title="Bien estimer son nombre de couverts" content="Pour comprendre comment estimer son nombre de couverts et utiliser notre simulateur de calcul :">
        <a target="_blank" :href="documentation.calculerNombreCouverts">Consultez notre article dédié</a>
      </AppHelpCard>
    </div>
  </div>
</template>
