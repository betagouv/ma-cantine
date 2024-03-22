<template>
  <div class="pa-2 rounded-sm my-4" style="border: solid 1px #e0e0e0;">
    <div id="matomo-opt-out"></div>
  </div>
</template>

<script>
export default {
  mounted() {
    window.showContent(window.MatomoConsent.hasConsent())
  },
}
</script>

<style scoped>
#matomo-opt-out >>> label {
  margin-left: 8px;
}
#matomo-opt-out >>> p {
  margin: 0;
}
</style>
