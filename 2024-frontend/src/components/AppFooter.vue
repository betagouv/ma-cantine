<script setup>
const logoText = ["Ministère", "de l'Agriculture", "et de la Souveraineté", "alimentaire"]

const descText =
  "« ma cantine » est un outil pour accompagner les acteurs de la restauration collective à proposer une alimentation de qualité, saine et durable."
</script>

<template>
  <DsfrFooter
    :logo-text
    a11yCompliance="partiellement conforme"
    :a11yComplianceLink="{ name: 'AccessibilityDeclaration' }"
    :legalLink="{ name: 'LegalNotices' }"
    :personalDataLink="{ name: 'PersonalData' }"
    :cookiesLink="{ name: 'PersonalData', hash: '#cookies' }"
    :afterMandatoryLinks="[
      { text: 'Conditions générales d\'utilisation', to: { name: 'CGU' } },
      { text: 'Plan du site', to: { name: 'SiteMap' } },
    ]"
    :desc-text
    licenceTo="https://github.com/betagouv/ma-cantine/blob/staging/LICENSE"
    licenceName="licence MIT"
  />
</template>
