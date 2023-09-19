import "@/styles/main.scss"
import { createVuetify } from "vuetify"
import * as components from "vuetify/components"
import * as directives from "vuetify/directives"
import remixJson from "./remix.json"
// import { mdi } from "vuetify/iconsets/mdi-svg"

const dsfrLightTheme = {
  dark: false,
  colors: {
    primary: "#000091",
    "primary-lighten-5": "#e0e0f2",
    "primary-lighten-4": "#cacafb",
    "primary-lighten-3": "#8080c8",
    "primary-lighten-2": "#4d4db2",
    "primary-lighten-1": "#2626a2",
    "primary-darken-1": "#000089",
    "primary-darken-2": "#00007e",
    "primary-darken-3": "#000074",
    "primary-darken-4": "#000062",

    secondary: "#ce614a",
    "secondary-lighten-5": "#f9ece9",
    "secondary-lighten-4": "#f0d0c9",
    "secondary-lighten-3": "#e7b0a5",
    "secondary-lighten-2": "#dd9080",
    "secondary-lighten-1": "#d57965",
    "secondary-darken-1": "#c95943",
    "secondary-darken-2": "#c24f3a",
    "secondary-darken-3": "#bc4532",
    "secondary-darken-4": "#b03322",

    error: "#df3232",
  },
}

export default createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: "dsfrLightTheme",
    themes: {
      dsfrLightTheme,
    },
  },
  display: {
    mobileBreakpoint: "sm",
  },
  /*
  remixJson contains a key-value pair of icon names and svg paths. These correspond to the icons
  on https://www.systeme-de-design.gouv.fr/elements-d-interface/fondamentaux-techniques/icones.
  To use them, instead of using the "mdi-" prefix, just append a dollar sign. For example, to use
  icon "cloudy-2-fill" you can use "<v-icon icon="$cloudy-2-fill"></v-icon>".

  Note that not all Remix icons are included, only those chosen by the DSFR. MDI icons are still
  available.
  */

  icons: {
    //   // defaultSet: "mdi",
    //   // iconset: "mdi",
    aliases: {
      // ...aliases,
      ...remixJson,
    },
    sets: {
      // mdi,
      // remixJson,
    },
  },
})
