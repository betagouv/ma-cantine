<template>
  <div
    id="matomo-opt-out"
    style="font-size: 12px; font-family: Arial; color: #000000; background-color: #FFFFFF; "
  ></div>
</template>

<script>
export default {
  mounted() {
    window.showContent(window.MatomoConsent.hasConsent())
  },
}
</script>
