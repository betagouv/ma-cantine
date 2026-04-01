<script setup>
import documentation from "@/data/documentation.json"
const metabaseStatsUrl = "https://ma-cantine-metabase.cleverapps.io/public/dashboard/0589649a-fabc-4001-82d6-f5f4fc15710d"
</script>

<template>
  <main class="statistiques">
    <section class="fr-col-12 fr-col-md-8 fr-mb-2w">
      <h1>Statistiques publiques</h1>
      <p>
        Cette page présente les chiffres clés de la plateforme ma cantine mis à jour en temps réel.<br/>
        Pour plus d'informations sur les données télédéclarées, consulter <a :href="documentation.rapportsBilansStatistiquesEgalim" target="_blank">les rapports annuels</a>.
      </p>
    </section>
    <iframe class="statistiques__iframe fr-mt-4w" :src="metabaseStatsUrl" title="Statistiques d'usage du poduit ma-cantine"></iframe>
  </main>
</template>

<style scoped>
.statistiques__iframe {
  width: 100%;
  height: 90vh;
}
</style>
