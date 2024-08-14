<script setup>
const descText =
  "« ma cantine » est un outil pour accompagner les acteurs de la restauration collective à proposer une alimentation de qualité, saine et durable."
</script>

<template>
  <DsfrFooter
    a11yCompliance="partiellement conforme"
    :a11yComplianceLink="{ name: 'AccessibilityDeclaration' }"
    :personalDataLink="{ name: 'PrivacyPolicy' }"
    :cookiesLink="{ name: 'Cookies' }"
    :afterMandatoryLinks="[{ text: 'Plan du site', to: { name: 'SiteMap' } }]"
    :desc-text
  />
</template>
