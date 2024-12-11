export default {
  trackEvent(params) {
    if (window.MATOMO_ID) {
      const { category, action, value } = params
      window._paq.push(["trackEvent", category, action, value])
    }
  },
}
