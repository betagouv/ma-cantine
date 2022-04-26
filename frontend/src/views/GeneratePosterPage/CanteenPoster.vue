<template>
  <div class="poster-contents">
    <div class="spacer"></div>
    <div id="heading">
      <div>
        <h2>Qualité des approvisionnements dans l’établissement {{ canteen.name || "_________" }}</h2>
        <div id="indicators">
          <!-- Can't use <img> because the object-fit is not respected in the PDF generation -->
          <div :style="`background-image: url('${canteen.logo}')`" v-if="canteen.logo" class="cantine-image" alt="" />

          <CanteenIndicators :canteen="canteen" />
        </div>
      </div>
      <div class="spacer"></div>
      <img src="/static/images/doodles/primary/CoffeeDoodle.png" id="hat" alt="" />
    </div>
    <div class="spacer"></div>

    <p id="introduction">
      Sur les {{ canteen.dailyMealCount }} repas servis aux convives, pour l’année {{ infoYear }}, voici la répartition,
      en valeur d’achat, des produits bio, de qualité et durables (liste de labels ci-dessous) utilisés dans la
      confection des repas
    </p>

    <div class="spacer"></div>
    <div id="graphs">
      <div>
        <p class="graph-title">Approvisionnement {{ infoYear }}</p>
        <SummaryStatistics
          :width="showPreviousDiagnostic ? 300 : 450"
          :qualityDiagnostic="diagnostic"
          class="summary-statistics"
          :hideLegend="showPreviousDiagnostic"
        />
      </div>
      <div v-if="showPreviousDiagnostic">
        <p class="graph-2-title">Rappel {{ infoYear - 1 }}</p>

        <SummaryStatistics :width="390" :qualityDiagnostic="previousDiagnostic" class="summary-statistics" />
      </div>
    </div>

    <LogoList id="logos" />
    <div class="spacer"></div>

    <p id="custom-text">{{ customText }}</p>

    <div class="spacer"></div>
    <div id="about">
      <v-row align="start">
        <v-col :cols="customText ? 9 : 12">
          <h3>Pourquoi je vois cette affiche ?</h3>
          <p class="footer-text">
            L’objectif de cet affichage est de rendre plus transparentes l’origine et la qualité des produits composant
            les menus et de soutenir l’objectif d’une alimentation plus saine et plus durable dans les restaurants. En
            partenariat avec « ma cantine », plateforme gouvernementale, cet établissement a rempli ses obligations
            d’information des convives.
          </p>
        </v-col>
        <v-col :align="customText ? 'center' : ''">
          <qrcode-vue
            :value="canteen.publicationStatus === 'published' ? canteenUrl : 'https://ma-cantine.beta.gouv.fr'"
            id="qr-code"
          ></qrcode-vue>
          <p class="footer-text"><a href="https://ma-cantine.beta.gouv.fr/">ma-cantine.beta.gouv.fr</a></p>
        </v-col>
      </v-row>
    </div>
    <div class="spacer"></div>
  </div>
</template>

<script>
import LogoList from "@/components/LogoList"
import SummaryStatistics from "./SummaryStatistics"
import CanteenIndicators from "@/components/CanteenIndicators"
import QrcodeVue from "qrcode.vue"
import { lastYear } from "@/utils"

export default {
  components: {
    LogoList,
    SummaryStatistics,
    CanteenIndicators,
    QrcodeVue,
  },
  props: {
    canteen: Object,
    diagnostic: Object,
    previousDiagnostic: Object,
    customText: String,
  },
  computed: {
    showPreviousDiagnostic() {
      if (!this.previousDiagnostic) return false
      return !!this.previousDiagnostic.valueTotalHt
    },
    canteenUrl() {
      const baseUrl = window.location.toString().replace(window.location.pathname, "")
      const fullPath = this.$router.resolve({
        name: "CanteenPage",
        params: { canteenUrlComponent: this.$store.getters.getCanteenUrlComponent(this.canteen) },
      }).href
      return baseUrl + fullPath
    },
    infoYear() {
      return this.diagnostic.year || lastYear()
    },
  },
}
</script>

<style scoped lang="scss">
.poster-contents {
  display: flex;
  flex-direction: column;
  height: 296mm;
  overflow: hidden; // to show how it will be on paper
  padding: 14mm;
  // Need to repeat some styling directly here for PDF generation
  font-family: "Marianne";
}

// copy vuetify styling to have on generated PDF
p {
  margin-bottom: 16px;
}
i {
  background: white;
}

.spacer {
  flex-grow: 1;
}

#heading {
  display: flex;
  align-items: top;

  div {
    text-align: left;
  }

  h2 {
    font-size: 25px;
  }
}

.cantine-image {
  width: 150px;
  height: 75px;
  border-radius: 4px;
  margin-right: 8px;
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}

#indicators {
  margin: 16px 0px 12px 0;
  font-size: 12px;
  line-height: 20px;
  color: rgba(0, 0, 0, 0.54);
  display: flex;
  align-items: center;
}

#hat {
  width: 150px;
  height: 112px;
  margin-left: 1em;
}

#introduction {
  font-size: 14px;
}

#logos {
  width: 440px;
  margin-bottom: 1.5em;
  margin-left: auto;
  margin-right: auto;
  align-self: center;
}

#graphs {
  align-self: center;
  display: flex;
  align-items: center;
  margin-bottom: 1em;
}

.graph-title {
  text-align: center;
  font-weight: bold;
  margin-bottom: 8px;
  margin-left: 16px;
  margin-right: 16px;
}

.graph-2-title {
  font-weight: bold;
  margin-bottom: 8px;
  margin-left: 24px;
}

#custom-text {
  font-size: 14px;
  overflow-wrap: break-word;
  hyphens: auto;
}

#about {
  width: 100%;
  text-align: left;

  h3 {
    margin-bottom: 8px;
    font-size: 1rem;
    font-weight: bold;
  }

  a {
    color: $ma-cantine-grey;
    font-weight: bold;
  }

  .footer-text {
    font-size: 12px;
    margin: 0;
  }

  #qr-code {
    padding-top: 14px;
  }
}
</style>
