<template>
  <div class="poster-contents">
    <div class="spacer"></div>
    <div id="heading">
      <div>
        <h2>Qualité des approvisionnements dans l’établissement {{ canteen.name || "_________" }}</h2>
        <div id="indicators">
          <img contain :src="canteen.logo" :alt="`Logo ${canteen.name}`" class="canteen-image" />

          <CanteenIndicators :canteen="canteen" />
        </div>
      </div>
      <div class="spacer"></div>
      <img src="/static/images/doodles-dsfr/primary/CoffeeDoodle.png" id="hat" alt="" />
    </div>
    <div class="spacer"></div>

    <p id="introduction" v-if="hasCurrentYearData">
      {{ introText }}, pour l’année {{ infoYear }}, voici la répartition, en valeur d’achat, des produits bio, de
      qualité et durables (liste de labels ci-dessous) utilisés dans la confection des repas.
    </p>
    <p id="introduction" v-else>
      Nous n'avons pas de données renseignées pour cet établissement pour l’année {{ infoYear }}.
    </p>

    <p class="pat pat-heading" v-if="patPercentage || patName">Projet Alimentaires Territoriaux</p>
    <p class="pat" v-if="patPercentage && patName">
      {{ patPercentage }} % de nos produits proviennent du PAT « {{ patName }} »
    </p>
    <p class="pat" v-else-if="patPercentage">{{ patPercentage }} % de nos produits proviennent d'un PAT</p>
    <p class="pat" v-else-if="patName">Certains de nos produits proviennent du PAT « {{ patName }} »</p>

    <div class="spacer"></div>
    <div id="graphs" v-if="hasCurrentYearData">
      <div class="d-flex justify-space-between">
        <div class="appro-box">
          <p>
            <span class="grey--text text-h5 font-weight-black text--darken-2 mr-1">{{ bioPercent }} %</span>
            <span class="caption grey--text text--darken-2">
              bio
            </span>
          </p>
          <div>
            <img
              contain
              src="/static/images/quality-labels/logo_bio_eurofeuille.png"
              alt="Logo Agriculture Biologique"
              title="Logo Agriculture Biologique"
              height="35"
            />
          </div>
        </div>

        <div class="appro-box">
          <p>
            <span class="grey--text text-h5 font-weight-black text--darken-2 mr-1">{{ sustainablePercent }} %</span>
            <span class="caption grey--text text--darken-2">
              durables et de qualité (hors bio)
            </span>
          </p>
          <div class="d-flex justify-center flex-wrap">
            <img
              contain
              v-for="label in labels"
              :key="label.title"
              :src="`/static/images/quality-labels/${label.src}`"
              :alt="label.title"
              :title="label.title"
              height="33"
            />
          </div>
        </div>
      </div>
    </div>
    <p class="previous-year" v-if="showPreviousDiagnostic">
      En {{ infoYear - 1 }}, nos produits étaient à {{ previousBioPercent }} % Bio et {{ previousSustainablePercent }} %
      de qualité et durables.
    </p>
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
            partenariat avec « ma cantine », plateforme nationale, cet établissement a rempli ses obligations
            d’information des convives.
          </p>
        </v-col>
        <v-col :align="customText ? 'center' : ''">
          <qrcode-vue
            :value="canteen.publicationStatus === 'published' ? canteenUrl : 'https://ma-cantine.agriculture.gouv.fr'"
            id="qr-code"
          ></qrcode-vue>
          <p class="footer-text">
            <a href="https://ma-cantine.agriculture.gouv.fr/">ma-cantine.agriculture.gouv.fr</a>
          </p>
        </v-col>
      </v-row>
    </div>
    <div class="spacer"></div>
  </div>
</template>

<script>
import CanteenIndicators from "@/components/CanteenIndicators"
import QrcodeVue from "qrcode.vue"
import { lastYear, getPercentage, getSustainableTotal } from "@/utils"
import labels from "@/data/quality-labels.json"

export default {
  components: {
    CanteenIndicators,
    QrcodeVue,
  },
  props: {
    canteen: Object,
    diagnostic: Object,
    previousDiagnostic: Object,
    customText: String,
    patPercentage: String,
    patName: String,
  },
  data() {
    return { labels }
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
    introText() {
      if (this.canteen.productionType === "central")
        return `Sur les ${this.canteen.satelliteCanteensCount || ""} cantines satellites déservies`
      if (this.canteen.productionType === "central_serving")
        return `Sur les ${this.canteen.satelliteCanteensCount || ""} cantines satellites déservies et les ${
          this.canteen.dailyMealCount
        } repas servis sur place`
      if (this.canteen.productionType === "site_cooked_elsewhere")
        return `Sur les repas faits par la cuisine central déservant cette cantine`
      else return `Sur les ${this.canteen.dailyMealCount || ""} repas par jour servis aux convives`
    },
    bioPercent() {
      return getPercentage(this.diagnostic.valueBioHt, this.diagnostic.valueTotalHt)
    },
    sustainablePercent() {
      return getPercentage(getSustainableTotal(this.diagnostic), this.diagnostic.valueTotalHt)
    },
    previousBioPercent() {
      return getPercentage(this.previousDiagnostic.valueBioHt, this.previousDiagnostic.valueTotalHt)
    },
    previousSustainablePercent() {
      return getPercentage(getSustainableTotal(this.previousDiagnostic), this.previousDiagnostic.valueTotalHt)
    },
    hasCurrentYearData() {
      if (!this.diagnostic) return false
      return !!this.diagnostic.valueTotalHt
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

.canteen-image {
  max-width: 150px;
  max-height: 150px;
  margin-right: 10px;
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

#introduction,
.pat,
.previous-year {
  font-size: 14px;
}

.pat-heading {
  margin-bottom: 0;
  font-weight: bold;
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
  width: 100%;
}

#graphs > div {
  width: 100%;
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
.appro-box {
  text-align: center;
  border: solid 1px #ccc;
  width: 49%;
  padding: 10px;
}
.d-flex {
  display: flex;
}
.justify-space-between {
  justify-content: space-between !important;
}
.justify-center {
  justify-content: center !important;
}
.flex-wrap {
  flex-wrap: wrap !important;
}
</style>
