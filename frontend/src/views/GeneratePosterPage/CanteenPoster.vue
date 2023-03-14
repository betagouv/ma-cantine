<template>
  <div class="poster-contents" :class="{ small: isHighContent, big: isLowContent }">
    <div class="spacer"></div>
    <div id="heading">
      <div>
        <h2>Manger plus saine et écolo</h2>
        <h3 v-if="canteen.name">{{ canteen.name }}</h3>
        <div id="indicators">
          <CanteenIndicators :canteen="canteen" :singleLine="isHighContent" />
        </div>
      </div>
      <div class="spacer"></div>
      <img v-if="canteen.logo" :src="canteen.logo" :alt="`Logo ${canteen.name}`" class="canteen-image" />
    </div>

    <div class="spacer"></div>

    <p id="introduction" v-if="!hasCurrentYearData">
      Nous n'avons pas de données renseignées pour cet établissement pour l’année {{ infoYear }}.
    </p>
    <div v-else>
      <h3>Qualité de la nourriture en {{ infoYear }}</h3>
      <div id="quality-data">
        <div :class="!isLowContent ? 'd-flex justify-space-between' : ''">
          <div class="appro-box">
            <p>
              <span class="percent">{{ bioPercent }} %</span>
              <span class="appro-label">
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

          <div class="appro-box" :class="!isLowContent ? '' : 'mt-4'">
            <p>
              <span class="percent">{{ sustainablePercent }} %</span>
              <span class="appro-label">
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
    </div>

    <div class="spacer" v-if="showPreviousDiagnostic"></div>

    <p class="previous-year" v-if="showPreviousDiagnostic">
      En {{ infoYear - 1 }}, nos produits étaient à {{ previousBioPercent }}&nbsp;% bio et
      {{ previousSustainablePercent }}&nbsp;% durables et de qualité (hors bio).
    </p>

    <div class="spacer" v-if="patPercentage || patName"></div>

    <p class="pat-heading" v-if="patPercentage || patName">Projet Alimentaires Territoriaux</p>
    <p class="pat" v-if="patPercentage && patName">
      {{ patPercentage }} % de nos produits proviennent du PAT « {{ patName }} »
    </p>
    <p class="pat" v-else-if="patPercentage">{{ patPercentage }} % de nos produits proviennent d'un PAT</p>
    <p class="pat" v-else-if="patName">Certains de nos produits proviennent du PAT « {{ patName }} »</p>

    <div class="spacer" v-if="hasBadges"></div>

    <div v-if="hasBadges" class="badge-container">
      <h3 class="badge-heading">Nos succès</h3>
      <div v-for="(badge, key) in earnedBadges" :key="key" class="d-flex" style="margin-bottom: 14px;">
        <img :width="isHighContent ? 25 : 38" contain :src="`/static/images/badges/${key}.svg`" alt="" />
        <div
          class="badge-description"
          v-text="badge.subtitle"
          v-if="key !== 'appro' || applicableRules.qualityThreshold === 50"
        ></div>
        <div class="badge-description" v-else>
          Ce qui est servi dans les assiettes est au moins à
          {{ applicableRules.qualityThreshold }}&nbsp;% de produits durables et de qualité, dont
          {{ applicableRules.bioThreshold }}&nbsp;% bio, en respectant les seuils d'Outre-mer.
        </div>
      </div>
    </div>

    <div class="spacer" v-if="customText"></div>

    <h3 v-if="customText">Un mot du gestionnaire</h3>
    <p id="custom-text">{{ customText }}</p>

    <div class="spacer"></div>
    <div class="spacer"></div>
    <div id="about">
      <v-row align="start">
        <v-col align="center" v-if="isHighContent">
          <qrcode-vue
            :value="canteen.publicationStatus === 'published' ? canteenUrl : 'https://ma-cantine.agriculture.gouv.fr'"
            id="qr-code"
          ></qrcode-vue>
        </v-col>
        <v-col :cols="isHighContent ? 9 : 12">
          <h3>Pourquoi je vois cette affiche ?</h3>
          <p class="footer-text">
            L’objectif de cet affichage est de rendre plus transparentes l’origine et la qualité des produits composant
            les menus et de soutenir l’objectif d’une alimentation plus saine et plus durable dans les restaurants.
          </p>
          <p class="footer-text" v-if="isHighContent">
            <a href="https://ma-cantine.agriculture.gouv.fr/">ma-cantine.agriculture.gouv.fr</a>
          </p>
        </v-col>
        <v-col v-if="!isHighContent">
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
import { lastYear, getPercentage, getSustainableTotal, badges, applicableDiagnosticRules } from "@/utils"
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
    patPercentage: [String, Number],
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
    earnedBadges() {
      if (!Object.keys(this.canteen).length) return {}
      const canteenBadges = badges(this.canteen, this.diagnostic, this.$store.state.sectors)
      let earnedBadges = {}
      Object.keys(canteenBadges).forEach((key) => {
        if (canteenBadges[key].earned) earnedBadges[key] = canteenBadges[key]
      })
      return earnedBadges
    },
    applicableRules() {
      return applicableDiagnosticRules(this.canteen)
    },
    hasBadges() {
      return !!Object.keys(this.earnedBadges).length
    },
    contentLength() {
      // this is an estimation of lines, not literal
      let linesOfVariableContent = 0
      // canteen indicators
      linesOfVariableContent += !!this.canteen.dailyMealCount && 1
      linesOfVariableContent += !!this.canteen.sectors?.length && 1
      linesOfVariableContent += !!this.canteen.satelliteCanteensCount && 1
      linesOfVariableContent += !!this.canteen.city && 1

      linesOfVariableContent += !!this.patPercentage && 1
      linesOfVariableContent += !!this.patName && 1

      linesOfVariableContent += this.hasCurrentYearData && 4
      linesOfVariableContent += this.showPreviousDiagnostic && 1

      linesOfVariableContent += this.hasBadges && Object.keys(this.earnedBadges).length
      const charactersPerLine = 80 // estimate, changes based on font size
      linesOfVariableContent += this.customText?.length / charactersPerLine || 0
      // range from 0 - approx 25
      return linesOfVariableContent
    },
    isHighContent() {
      return this.contentLength >= 20
    },
    isLowContent() {
      return this.contentLength <= 10
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
  font-family: "Marianne" !important;
  // copy vuetify styling to have on generated PDF
  p {
    margin-bottom: 0;
    font-size: 100%; // 16px
  }
  i {
    background: white;
  }
  h3 {
    font-size: 1.5em;
  }
}
.poster-contents.small {
  font-size: 90%;
}
.poster-contents.big {
  font-size: 110%;
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
    font-size: 2em;
    margin-bottom: 16px;
  }

  h3 {
    font-weight: normal;
  }
}

.canteen-image {
  max-width: 200px;
  max-height: 150px;
  margin-right: 10px;
  object-fit: contain;
}

#indicators {
  font-size: 0.875em;
  color: rgba(0, 0, 0, 0.54);
  display: flex;
  align-items: center;
}

#hat {
  width: 150px;
  height: 112px;
  margin-left: 1em;
}

.badge-description {
  margin-left: 8px;
  display: flex;
  justify-content: center;
  flex-direction: column;
  font-size: 1em;
}

.pat-heading {
  margin-bottom: 0 !important;
  font-weight: bold;
}

.pat {
  margin-bottom: 0 !important;
}

#logos {
  width: 440px;
  margin-bottom: 1.5em;
  margin-left: auto;
  margin-right: auto;
  align-self: center;
}

#quality-data {
  align-self: center;
  display: flex;
  align-items: center;
  margin-bottom: 1em;
  margin-top: 1em;
  width: 100%;
}

#quality-data > div {
  width: 100%;
}

.appro-box {
  text-align: center;
  border: solid 1px #ccc;
  width: 49%;
  padding: 0.625em;

  p {
    margin-bottom: 0.5em;
  }

  .percent {
    font-size: 1.5em;
    font-weight: 900;
    line-height: 1.8em;
    letter-spacing: normal;
    color: #464646;
    margin-right: 4px;
  }

  .appro-label {
    color: #464646;
    font-size: 1em;
    font-weight: 400;
    letter-spacing: 0.0333333333em;
    line-height: 1.25em;
  }
}
#custom-text {
  font-size: 0.9em;
  overflow-wrap: break-word;
  hyphens: auto;
  margin-top: 8px;
}

#about {
  width: 100%;
  text-align: left;

  h3 {
    margin-bottom: 8px;
    font-size: 1em;
    font-weight: bold;
  }

  a {
    color: $ma-cantine-grey;
    font-weight: bold;
  }

  .footer-text {
    font-size: 0.875em;
    margin: 0;
    margin-top: 0.3em;
  }

  #qr-code {
    padding-top: 0.4em;
  }
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
.badge-heading {
  margin-bottom: 0.5em;
}
.poster-explainer {
  margin-top: 0.75em;
}
.mt-4 {
  margin-top: 1em;
}
</style>
