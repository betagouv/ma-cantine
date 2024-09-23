<template>
  <div id="wasteactions-home" class="text-left">
    <BreadcrumbsNav />
    <h1 class="fr-h1 mb-4">
      Lutter contre le gaspillage alimentaire
    </h1>
    <div class="d-flex justify-end">
      <DsfrSegmentedControl v-model="viewStyle" legend="Vue" :noLegend="true" :items="viewStyles" />
    </div>
    <v-row class="mb-4 align-end">
      <v-col>
        <p class="mb-2">Taille d'action</p>
        <DsfrTagGroup :tags="wasteActionEfforts" @clickTag="(tag) => addFilterTag('effort', tag)" />
      </v-col>
      <v-col>
        <p class="mb-2">Origine du gaspillage</p>
        <DsfrTagGroup :tags="wasteOrigins" @clickTag="(tag) => addFilterTag('wasteOrigins', tag)" />
      </v-col>
      <v-col cols="12" md="4">
        <DsfrSearchField
          v-model="filters.search.provisionalValue"
          @search="applyProvisionalValue(filters.search)"
          clearable
          @clear="clearFilterField(filters.search)"
          placeholder="Rechercher par titre"
          hide-details="auto"
        />
      </v-col>
    </v-row>
    <div v-if="loading" class="d-flex flex-column align-center placeholder-height">
      <v-progress-circular indeterminate class="mt-10"></v-progress-circular>
    </div>
    <div v-else-if="wasteActions.length > 0">
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
      <DsfrPagination
        class="my-6"
        v-model="page"
        :length="Math.ceil(wasteActionsCount / limit)"
        @input="fetchCurrentPage"
      />
    </div>
    <div v-else-if="hasFilter" class="d-flex flex-column align-center placeholder-height">
      <v-icon large class="mt-10">mdi-inbox-remove</v-icon>
      <p class="text-body-1 grey--text text--darken-1 my-2">
        Nous n'avons pas trouvé des actions avec ces paramètres
      </p>
      <v-btn color="primary" text @click="clearFilters" class="text-decoration-underline">
        Désactiver tous les filtres
      </v-btn>
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
import DsfrSearchField from "@/components/DsfrSearchField"
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
    DsfrSearchField,
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
        search: {
          urlParam: "recherche",
          apiKey: "search",
          value: null,
          provisionalValue: null,
          default: null,
        },
        effort: {
          urlParam: "effort",
          apiKey: "effort",
          value: [],
          default: [],
        },
        wasteOrigins: {
          urlParam: "origine",
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
      this.updateRouter()
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
    addFilterTag(filterKey, tag) {
      const idx = this.filters[filterKey].value.findIndex((i) => i === tag.value)
      if (idx === -1) this.filters[filterKey].value.push(tag.value)
      else this.filters[filterKey].value.splice(idx, 1)
      this.page = 1
      this.fetchAfterFiltering()
    },
    clearFilters() {
      Object.values(this.filters).forEach((filter) => (filter.value = Array.from(filter.default)))
      this.fetchAfterFiltering()
    },
    fetchAfterFiltering() {
      // go to first page and trigger loading indication to show the user something happened
      this.page = 1
      this.wasteActionsCount = null
      this.fetchCurrentPage()
    },
    updateRouter() {
      const query = { page: this.page }
      Object.values(this.filters).forEach((filter) => {
        if (filter.value?.length) {
          query[filter.urlParam] = filter.value
        }
      })
      this.$router.push({ query }).catch(() => {})
    },
    parseQueryParams() {
      this.page = +this.$route.query.page || 1
      Object.values(this.filters).forEach((filter) => {
        const queryValue = this.$route.query[filter.urlParam]
        if (queryValue && queryValue.length) {
          if (Array.isArray(filter.default) && !Array.isArray(queryValue)) {
            filter.value = [queryValue]
          } else {
            filter.value = queryValue
            filter.provisionalValue = queryValue
          }
        }
      })
    },
    applyProvisionalValue(filterTerm) {
      filterTerm.value = filterTerm.provisionalValue
      this.fetchAfterFiltering()
    },
    clearFilterField(filterTerm) {
      filterTerm.provisionalValue = filterTerm.default
      filterTerm.value = filterTerm.provisionalValue
      this.fetchAfterFiltering()
    },
  },
  mounted() {
    this.parseQueryParams()
    this.fetchCurrentPage()
  },
}
</script>

<style scoped>
div.placeholder-height {
  height: 1200px;
}
</style>
