const trackEvent = (params) => {
  if (window.MATOMO_ID) {
    const { category, action, value } = params
    window._paq.push(["trackEvent", category, action, value])
  }
}

const showContent = () => {
  window.showContent(window.MatomoConsent.hasConsent())
}

export { trackEvent, showContent }
