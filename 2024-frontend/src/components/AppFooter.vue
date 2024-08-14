<script setup>
const logoText = ["Ministère", "de l’Agriculture", "et de la Souveraineté", "Alimentaire"]

const descText =
  "« ma cantine » est un outil pour accompagner les acteurs de la restauration collective à proposer une alimentation de qualité, saine et durable."
</script>

<template>
  <DsfrFooter
    :logo-text
    a11yCompliance="partiellement conforme"
    :a11yComplianceLink="{ name: 'AccessibilityDeclaration' }"
    :personalDataLink="{ name: 'PrivacyPolicy' }"
    :cookiesLink="{ name: 'Cookies' }"
    :afterMandatoryLinks="[{ text: 'Plan du site', to: { name: 'SiteMap' } }]"
    :desc-text
    licenceTo="https://github.com/betagouv/ma-cantine/blob/staging/LICENSE"
    licenceName="licence MIT"
  />
</template>
