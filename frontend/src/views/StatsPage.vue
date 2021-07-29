<template>
  <div>
    <h1 class="font-weight-black text-left my-6">Statistiques</h1>
    <iframe
      src="http://ma-cantine-metabase.cleverapps.io/public/dashboard/54639f66-d6d0-407c-a9db-766b5fb01e3e"
      style="border: 1px solid rgb(204, 204, 204);box-shadow: 3px 3px 7px -3px #999;"
      width="100%"
      height="400"
      class="mb-10"
      allowtransparency
    ></iframe>
    <h2 class="font-weight-black text-left my-6">
      👾 Statistiques d’usage et de comportement des personnes utilisatrices de la plateforme
    </h2>
    <h3 class="text-left my-3">Nombre de visites dans le mois dernier</h3>
    <iframe
      width="100%"
      height="300"
      :src="visits"
      scrolling="yes"
      frameborder="0"
      marginheight="0"
      marginwidth="0"
      aria-labelledby="visits"
    />
    <h3 class="text-left my-3">Canaux d'acquisition</h3>
    <iframe
      width="100%"
      height="350"
      :src="channel"
      scrolling="yes"
      frameborder="0"
      marginheight="0"
      marginwidth="0"
      aria-labelledby="channels"
    />
    <h3 class="text-left my-3">Pages visitées (total)</h3>
    <iframe
      id="matomo-pages"
      width="100%"
      height="400"
      :src="pages"
      scrolling="yes"
      frameborder="0"
      marginheight="0"
      marginwidth="0"
      aria-labelledby="pages"
    />
  </div>
</template>

<script>
const MATOMO_ID = 162

export default {
  computed: {
    visits() {
      return (
        `https://stats.data.gouv.fr/index.php?module=Widgetize&action=iframe&forceView=1&viewDataTable=graphEvolution&disableLink=0&` +
        `widget=1&moduleToWidgetize=VisitsSummary&actionToWidgetize=getEvolutionGraph&idSite=${MATOMO_ID}&period=day&date=yesterday&disableLink=1&widget=1`
      )
    },
    channel() {
      return (
        `https://stats.data.gouv.fr/index.php?module=Widgetize&action=iframe&disableLink=0&widget=1&viewDataTable=graphPie&` +
        `moduleToWidgetize=Referrers&actionToWidgetize=getReferrerType&idSite=${MATOMO_ID}&period=year&date=yesterday&disableLink=1&widget=1`
      )
    },
    pages() {
      return (
        `https://stats.data.gouv.fr/index.php?module=Widgetize&action=iframe&disableLink=0&widget=1&moduleToWidgetize=Actions&` +
        `actionToWidgetize=getPageUrls&idSite=${MATOMO_ID}&period=year&date=yesterday&disableLink=1&widget=1`
      )
    },
  },
}
</script>
