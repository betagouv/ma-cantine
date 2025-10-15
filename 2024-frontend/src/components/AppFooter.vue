<script setup>
const logoText = ["Ministère", "de l'Agriculture", "et de la Souveraineté", "alimentaire"]

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
      {text: 'Statistiques', href: 'https://ma-cantine-metabase.cleverapps.io/public/dashboard/0589649a-fabc-4001-82d6-f5f4fc15710d'}
    ]"
    :desc-text
    licenceTo="https://github.com/betagouv/ma-cantine/blob/staging/LICENSE"
    licenceName="licence MIT"
  />
</template>
