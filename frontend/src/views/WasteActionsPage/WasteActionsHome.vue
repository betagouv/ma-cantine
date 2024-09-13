<template>
  <div id="wasteactions-home" class="text-left">
    <BreadcrumbsNav />
    <h1 class="fr-h1 mb-4">
      Lutter contre le gaspillage alimentaire
    </h1>
    <div v-if="loading" class="mt-8">
      <v-progress-circular indeterminate></v-progress-circular>
    </div>
    <div v-else-if="wasteActions.length > 0 || hasFilter">
      <div class="d-flex justify-end">
        <DsfrSegmentedControl v-model="viewStyle" legend="Vue" :noLegend="true" :items="viewStyles" />
      </div>
      <v-row class="mb-4">
        <v-col>
          <p class="mb-2">Taille d'action</p>
          <DsfrTagGroup :tags="wasteActionEfforts" @clickTag="(tag) => addFilterTag('effort', tag)" />
        </v-col>
        <v-col>
          <p class="mb-2">Origine du gaspillage</p>
          <DsfrTagGroup :tags="wasteOrigins" @clickTag="(tag) => addFilterTag('wasteOrigins', tag)" />
        </v-col>
      </v-row>
      <div v-if="wasteActions.length > 0">
        <div v-if="viewStyle === 'card'">
          <v-row class="mt-2">
            <v-col vols="12" sm="6" md="4" v-for="wasteAction in wasteActions" :key="wasteAction.id">
              <WasteActionCard :wasteAction="wasteAction" />
            </v-col>
          </v-row>
        </div>
        <div v-else>
          <WasteActionsListView :wasteActions="wasteActions" class="mt-4" />
        </div>
        <DsfrPagination class="my-6" v-model="page" :length="Math.ceil(wasteActionsCount / limit)" />
      </div>
      <div v-else class="d-flex flex-column align-center py-10">
        <v-icon large>mdi-inbox-remove</v-icon>
        <p class="text-body-1 grey--text text--darken-1 my-2">
          Nous n'avons pas trouvé des actions avec ces paramètres
        </p>
        <v-btn color="primary" text @click="clearFilters" class="text-decoration-underline">
          Désactiver tous les filtres
        </v-btn>
      </div>
    </div>
    <div v-else>
      <p>
        Contenu en cours de construction
      </p>
    </div>
  </div>
</template>
<script>
import WasteActionCard from "./WasteActionCard"
import WasteActionsListView from "./WasteActionsListView"
import DsfrPagination from "@/components/DsfrPagination"
import BreadcrumbsNav from "@/components/BreadcrumbsNav"
import DsfrSegmentedControl from "@/components/DsfrSegmentedControl"
import DsfrTagGroup from "@/components/DsfrTagGroup"
import Constants from "@/constants"

export default {
  name: "WasteActionsHome",
  components: {
    WasteActionCard,
    WasteActionsListView,
    DsfrPagination,
    BreadcrumbsNav,
    DsfrSegmentedControl,
    DsfrTagGroup,
  },
  data() {
    return {
      limit: 6,
      page: null,
      wasteActions: [],
      wasteActionsCount: null,
      viewStyles: [
        {
          text: "Vue cartes",
          icon: "$layout-grid-fill",
          value: "card",
        },
        {
          text: "Vue liste",
          icon: "$list-check",
          value: "list",
        },
      ],
      viewStyle: "card",
      filters: {
        effort: {
          apiKey: "effort",
          value: [],
          default: [],
        },
        wasteOrigins: {
          apiKey: "waste_origins",
          value: [],
          default: [],
        },
      },
    }
  },
  computed: {
    loading() {
      return this.wasteActionsCount === null
    },
    offset() {
      return (this.page - 1) * this.limit
    },
    wasteOrigins() {
      return Constants.WasteActionOrigins.map((item) => ({
        ...item,
        id: item.value,
        selected: this.filters.wasteOrigins.value.includes(item.value),
      }))
    },
    wasteActionEfforts() {
      return Constants.WasteActionEffortLevels.map((item) => ({
        ...item,
        id: item.value,
        selected: this.filters.effort.value.includes(item.value),
      }))
    },
    hasFilter() {
      return Object.values(this.filters).some((filter) => filter.value.length)
    },
  },

  methods: {
    fetchCurrentPage() {
      this.wasteActionsCount = null
      this.$store
        .dispatch("fetchWasteActions", {
          offset: this.offset,
          limit: this.limit,
          filters: this.filters,
        })
        .then((response) => {
          this.wasteActions = response.results
          this.wasteActionsCount = response.count
        })
        .catch(() => {
          this.$store.dispatch("notifyServerError")
        })
    },
    updateRoute() {
      let query = { page: this.page }
      // The empty catch is the suggested error management here : https://github.com/vuejs/vue-router/issues/2872#issuecomment-519073998
      if (this.$route.query.page) {
        this.$router.push({ query }).catch(() => {})
      } else {
        this.$router.replace({ query }).catch(() => {})
      }
    },
    addFilterTag(filterKey, tag) {
      const idx = this.filters[filterKey].value.findIndex((i) => i === tag.value)
      if (idx === -1) this.filters[filterKey].value.push(tag.value)
      else this.filters[filterKey].value.splice(idx, 1)
      this.fetchCurrentPage()
    },
    clearFilters() {
      Object.values(this.filters).forEach((filter) => (filter.value = Array.from(filter.default)))
      this.fetchCurrentPage()
    },
  },
  watch: {
    page() {
      this.updateRoute()
    },
    $route() {
      this.fetchCurrentPage()
    },
  },
  mounted() {
    this.page = this.$route.query.page ? parseInt(this.$route.query.page) : 1
    this.fetchCurrentPage()
  },
}
</script>
