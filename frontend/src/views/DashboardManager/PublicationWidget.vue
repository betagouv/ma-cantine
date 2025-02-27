<template>
  <v-card outlined class="fill-height d-flex flex-column dsfr no-hover pa-sm-6">
    <v-card-title>
      <h3 class="fr-h4 mb-0">
        Mon affiche
      </h3>
    </v-card-title>
    <v-spacer></v-spacer>
    <v-card-text class="fr-text grey--text text--darken-2">
      <p class="publication-detail">
        Statut
        <PublicationBadge :isPublished="isPublished" />
      </p>
      <p class="publication-detail">
        Dernière mise à jour
        <span class="font-weight-bold fr-text-xs">{{ publicationUpdateDate }}</span>
      </p>
      <p class="publication-detail">
        Visiteurs (année en cours)
        <span class="font-weight-bold fr-text-xs">
          {{ isPublished && viewCount > 0 ? viewCount : "-" }}
        </span>
      </p>
    </v-card-text>
    <v-spacer></v-spacer>
    <v-card-actions class="flex-wrap flex-lg-nowrap">
      <p v-if="isPublished" class="mx-2 mb-2">
        <v-btn
          :to="{
            name: 'PublicationForm',
            params: { canteenUrlComponent: $store.getters.getCanteenUrlComponent(canteen) },
          }"
          color="primary"
          class="px-3"
          outlined
        >
          Éditer mon affiche
        </v-btn>
      </p>
      <p class="mx-2 mb-2">
        <v-btn outlined color="primary" class="fr-btn--tertiary px-3" :to="{ name: 'CanteenGeneratePoster' }">
          Générer mon affiche
        </v-btn>
      </p>
    </v-card-actions>
  </v-card>
</template>

<script>
import PublicationBadge from "@/components/PublicationBadge"
import { formatDate, lastYear } from "@/utils"

export default {
  name: "PublicationWidget",
  props: {
    canteen: {
      type: Object,
      required: true,
    },
  },
  components: { PublicationBadge },
  data() {
    return {
      viewCount: null,
      year: lastYear(),
    }
  },
  computed: {
    diagnostic() {
      return this.canteen?.diagnostics.find((x) => x.year === this.year)
    },
    isPublished() {
      return this.canteen?.publicationStatus === "published"
    },
    publicationUpdateDate() {
      if (!this.canteen || !this.isPublished) return "jamais"
      let date = new Date(this.canteen.modificationDate)
      if (this.diagnostic) {
        let diagDate = new Date(this.diagnostic.modificationDate)
        if (diagDate > date) date = diagDate
      }
      return formatDate(date.toISOString())
    },
    hasPublicationData() {
      return !!this.diagnostic?.valueTotalHt
    },
  },
  methods: {
    getPublishedPageViewCount() {
      if (!this.isPublished) this.viewCount = null
      if (!this.$matomo) this.viewCount = null
      const pageUrl =
        `${window.origin}${this.$router.resolve({ name: "CanteensHome" }).href}` +
        // Do not include the title part of the URL to handle A) name changes and B) / or no / ending
        `${this.canteen.id}--`
      const currentYear = this.year + 1
      const url =
        "https://stats.beta.gouv.fr/index.php?module=API&method=VisitsSummary.getVisits&format=JSON&token_auth=anonymous&period=range&" +
        `date=${currentYear}-01-01,today&` +
        `idSite=${window.MATOMO_ID}&` +
        `segment=pageUrl=^${encodeURIComponent(pageUrl)}`
      return fetch(url)
        .then((response) => {
          if (response.status < 200 || response.status >= 400) throw new Error(`Error encountered : ${response}`)
          return response.json()
        })
        .then((response) => {
          this.viewCount = response.value
        })
        .catch(() => {
          console.warn("Error when fetching page visits for url", url)
          this.viewCount = null
        })
    },
  },
  mounted() {
    this.getPublishedPageViewCount()
  },
  watch: {
    canteen(newCanteen, oldCanteen) {
      if (newCanteen && newCanteen.id !== oldCanteen?.id) {
        this.getPublishedPageViewCount()
      }
    },
  },
}
</script>

<style scoped>
p.publication-detail > span {
  float: right;
}
</style>
