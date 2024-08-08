import { createI18n } from "vue-i18n"
import fr from "./locales/fr.json"

// https://stackoverflow.com/a/70454910/3845770
const i18n = createI18n({
  legacy: false,
  locale: "fr",
  fallbackLocale: "en",
  messages: {
    fr,
  },
})

export default i18n
