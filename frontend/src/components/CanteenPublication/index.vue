<template>
  <div class="text-left">
    <v-col v-if="canteen && canteen.publicationComments && !editDescription" cols="12" sm="6" class="px-0">
      <h2 class="fr-text grey--text text--darken-4 mb-6">
        Description de l'établissement
      </h2>
      <div class="ml-n8">
        <DsfrHighlight>
          <p>
            {{ canteen.publicationComments }}
          </p>
        </DsfrHighlight>
      </div>
      <v-btn
        v-if="editable"
        @click="
          editDescription = true
          oldPublicationComments = canteen.publicationComments
        "
        outlined
        small
        color="primary"
        class="fr-btn--tertiary px-2 mt-4"
      >
        <v-icon primary x-small class="mr-1">mdi-pencil-outline</v-icon>
        Modifier la description
      </v-btn>
    </v-col>
    <v-col v-else-if="canteen && editable" cols="12" sm="6">
      <v-form v-model="publicationFormIsValid" ref="publicationCommentsForm">
        <DsfrTextarea
          class="mt-2"
          rows="5"
          counter="500"
          v-model="canteen.publicationComments"
          :rules="[validators.maxChars(500)]"
        >
          <template v-slot:label>
            <span class="fr-label mb-1">Déscription de l'établissement</span>
            <span class="fr-hint-text mb-2">
              Si vous le souhaitez, personnalisez votre affiche en écrivant quelques mots sur votre établissement : son
              fonctionnement, l'organisation, l'historique...
            </span>
          </template>
        </DsfrTextarea>
        <v-btn @click="saveDescription" class="primary">Enregistrer</v-btn>
      </v-form>
    </v-col>
    <h2 class="mt-12 mb-8">Où en-sommes nous de notre transition alimentaire ?</h2>
    <DsfrAccordion :items="badgeItems" :openPanelIndex="editable ? undefined : 0" class="mt-4">
      <template v-slot:title="{ item }">
        <span class="d-flex align-center">
          <v-img
            width="40"
            max-width="40"
            contain
            :src="`/static/images/badges/${item.badgeId}${item.earned ? '' : '-disabled'}.svg`"
            alt=""
            class="mr-3"
          ></v-img>
          {{ item.shortTitle }}
        </span>
      </template>
      <template v-slot:content="{ item }">
        <component
          :is="`${item.baseComponent}Results`"
          :badge="item"
          :canteen="canteen"
          :diagnosticSet="diagnosticSet"
        />
        <p class="mb-0">
          Se renseigner sur
          <router-link :to="{ name: 'KeyMeasurePage', params: { id: item.id } }">
            la réglementation de la mesure « {{ item.shortTitle }} »
          </router-link>
        </p>
      </template>
    </DsfrAccordion>

    <div v-if="!editable && canteen.images && canteen.images.length > imageLimit">
      <h2 class="font-weight-black text-h6 grey--text text--darken-4 mt-8 mb-0">
        Galerie
      </h2>
      <p class="body-2">
        Cliquez sur une image pour l'agrandir
      </p>
      <div>
        <ImageGallery :images="canteen.images.slice(imageLimit)" />
      </div>
    </div>
  </div>
</template>

<script>
import keyMeasures from "@/data/key-measures.json"
import { badges, latestCreatedDiagnostic, applicableDiagnosticRules } from "@/utils"
import ImageGallery from "@/components/ImageGallery"
import DsfrHighlight from "@/components/DsfrHighlight"
import DsfrTextarea from "@/components/DsfrTextarea"
import DsfrAccordion from "@/components/DsfrAccordion"
import Constants from "@/constants"
import validators from "@/validators"

import QualityMeasureResults from "./ResultsComponents/QualityMeasureResults"
import DiversificationMeasureResults from "./ResultsComponents/DiversificationMeasureResults"
import InformationMeasureResults from "./ResultsComponents/InformationMeasureResults"
import NoPlasticMeasureResults from "./ResultsComponents/NoPlasticMeasureResults"
import WasteMeasureResults from "./ResultsComponents/WasteMeasureResults"

export default {
  props: {
    canteen: Object,
    editable: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      editDescription: false,
      publicationFormIsValid: true,
      oldPublicationComments: undefined,
    }
  },
  components: {
    ImageGallery,
    DsfrHighlight,
    DsfrTextarea,
    DsfrAccordion,
    QualityMeasureResults,
    DiversificationMeasureResults,
    InformationMeasureResults,
    NoPlasticMeasureResults,
    WasteMeasureResults,
  },
  computed: {
    validators() {
      return validators
    },
    diagnosticSet() {
      if (!this.canteen) return
      if (!this.usesCentralKitchenDiagnostics) return this.canteen.diagnostics

      // Since the central kitchen might only handle the appro values, we will merge the diagnostics
      // from the central and satellites when necessary to show the whole picture
      return this.canteen.centralKitchenDiagnostics.map((centralDiag) => {
        const satelliteMatchingDiag = this.canteen.diagnostics.find((x) => x.year === centralDiag.year)
        if (centralDiag.centralKitchenDiagnosticMode === "APPRO" && satelliteMatchingDiag) {
          const satelliteDiagCopy = Object.assign({}, satelliteMatchingDiag)
          this.approFields.forEach((x) => delete satelliteDiagCopy[x])
          return Object.assign(satelliteDiagCopy, centralDiag)
        }
        return centralDiag
      })
    },
    approFields() {
      const approSimplifiedFields = [
        "valueTotalHt",
        "valueBioHt",
        "valueSustainableHt",
        "valueExternalityPerformanceHt",
        "valueEgalimOthersHt",
      ]
      const characteristicGroups = Constants.TeledeclarationCharacteristicGroups
      const approFields = characteristicGroups.egalim.fields
        .concat(characteristicGroups.outsideLaw.fields)
        .concat(characteristicGroups.nonEgalim.fields)
        .concat(approSimplifiedFields)
      const percentageApproFields = approFields.map((x) => `percentage${x.charAt(0).toUpperCase() + x.slice(1)}`)
      return approFields.concat(percentageApproFields)
    },
    diagnostic() {
      if (!this.diagnosticSet) return
      return latestCreatedDiagnostic(this.diagnosticSet)
    },
    usesCentralKitchenDiagnostics() {
      return (
        this.canteen?.productionType === "site_cooked_elsewhere" && this.canteen?.centralKitchenDiagnostics?.length > 0
      )
    },
    publicationYear() {
      return this.diagnostic?.year
    },
    canteenBadges() {
      const canteenBadges = badges(this.canteen, this.diagnostic, this.$store.state.sectors)
      Object.entries(canteenBadges).forEach(([key, badge]) => {
        const km = keyMeasures.find((k) => k.badgeId === key)
        Object.assign(badge, km)
      })
      return canteenBadges
    },
    badgeItems() {
      const items = JSON.parse(JSON.stringify(Object.values(this.canteenBadges)))
      items.map((item) => delete item.title)
      return items
    },
    earnedBadges() {
      let earnedBadges = {}
      Object.keys(this.canteenBadges).forEach((key) => {
        if (this.canteenBadges[key].earned) earnedBadges[key] = this.canteenBadges[key]
      })
      return earnedBadges
    },
    applicableRules() {
      return applicableDiagnosticRules(this.canteen)
    },
    imageLimit() {
      return this.$vuetify.breakpoint.xs ? 0 : 3
    },
  },
  methods: {
    saveDescription() {
      if (this.canteen.publicationComments === this.oldPublicationComments) {
        this.editDescription = false
        return
      }
      this.$refs.publicationCommentsForm.validate()
      if (!this.publicationFormIsValid) {
        this.$store.dispatch("notifyRequiredFieldsError")
        return
      }
      this.$store
        .dispatch("updateCanteen", {
          id: this.canteen.id,
          payload: { publicationComments: this.canteen.publicationComments },
        })
        .then(() => {
          this.$store.dispatch("notify", {
            status: "success",
            message: "Description mise à jour",
          })
          this.editDescription = false
        })
        .catch(() => {
          this.$store.dispatch("notifyServerError")
        })
    },
  },
}
</script>
