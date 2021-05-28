<template>
  <div id="stats">
    <h1>Statistiques</h1>
    <div class="infogram-embed" data-id="d79b1af3-0ab5-4338-a1c9-553d9e0d050e" data-type="interactive" />
    <h2>👾 Statistiques d’usage et de comportement des personnes utilisatrices de la plateforme</h2>
    <h3 id="visits">Nombre de visites dans le mois dernier</h3>
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
    <h3 id="channels">Canaux d'acquisition</h3>
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
    <h3 id="pages">Pages visitées (total)</h3>
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
  created() {
    const script = document.createElement("script")
    script.type = "text/javascript"
    script.text =
      '!function(e,i,n,s){var t="InfogramEmbeds",d=e.getElementsByTagName("script")[0];if(window[t]&&window[t].initialized)window[t].process&&window[t].process();' +
      'else if(!e.getElementById(n)){var o=e.createElement("script");o.async=1,o.id=n,o.src="https://e.infogram.com/js/dist/embed-loader-min.js",d.parentNode.insertBefore(o,d)}}(document,0,"infogram-async");'
    document.body.appendChild(script)
  },
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

<style scoped lang="scss">
#stats {
  padding: 2em;
  max-width: 900px;
  margin: auto;
  text-align: left;

  .infogram-embed {
    margin-bottom: 4rem;
  }
}
</style>
