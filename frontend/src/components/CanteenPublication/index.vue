<template>
  <div class="text-left" v-if="canteen">
    <EditableCommentsField
      v-if="canteen"
      :canteen="canteen"
      valueKey="publicationComments"
      :editable="editable"
      label="Description de l'établissement"
      cta="Modifier la description"
      :charLimit="500"
    >
      <template v-slot:help-text>
        <span class="fr-hint-text mb-2">
          Si vous le souhaitez, personnalisez votre affiche en écrivant quelques mots sur votre établissement&nbsp;: son
          fonctionnement, l'organisation, l'historique...
        </span>
      </template>
    </EditableCommentsField>

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
          :approDiagnostics="approDiagnostics"
          :serviceDiagnostics="serviceDiagnostics"
          :editable="editable"
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
import { badges } from "@/utils"
import ImageGallery from "@/components/ImageGallery"
import EditableCommentsField from "./EditableCommentsField"
import DsfrAccordion from "@/components/DsfrAccordion"

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
  components: {
    ImageGallery,
    EditableCommentsField,
    DsfrAccordion,
    QualityMeasureResults,
    DiversificationMeasureResults,
    InformationMeasureResults,
    NoPlasticMeasureResults,
    WasteMeasureResults,
  },
  computed: {
    approDiagnostics() {
      return this.canteen?.approDiagnostics
    },
    serviceDiagnostics() {
      return this.canteen?.serviceDiagnostics
    },
    canteenBadges() {
      const canteenBadges = badges(this.canteen)
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
    imageLimit() {
      return this.$vuetify.breakpoint.xs ? 0 : 3
    },
  },
}
</script>
