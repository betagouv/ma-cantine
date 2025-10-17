<script setup>
const logoText = ["République", "française"]

const descText =
  "« ma cantine » est un outil pour accompagner les acteurs de la restauration collective à proposer une alimentation de qualité, saine et durable."
</script>

<template>
  <DsfrFooter
    :logo-text
    a11yCompliance="partiellement conforme"
    :a11yComplianceLink="{ name: 'Accessibilite' }"
    :legalLink="{ name: 'MentionsLegales' }"
    :personalDataLink="{ name: 'DonneesPersonnelles' }"
    :cookiesLink="{ name: 'DonneesPersonnelles', hash: '#cookies' }"
    :afterMandatoryLinks="[
      { text: 'Conditions générales d\'utilisation', to: { name: 'ConditionsGeneralesUtilisation' } },
      { text: 'Plan du site', to: { name: 'PlanDuSite' } },
    ]"
    :desc-text
    licenceTo="https://github.com/betagouv/ma-cantine/blob/staging/LICENSE"
    licenceName="licence MIT"
  />
</template>
