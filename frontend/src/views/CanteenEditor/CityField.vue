<template>
  <DsfrAutocomplete
    hide-details="auto"
    :loading="loadingCommunes"
    :items="communes"
    :search-input.sync="search"
    auto-select-first
    cache-items
    @click:clear="$emit('update:inseeCode', null)"
    v-model="cityAutocompleteChoice"
    :no-data-text="noDataText"
    v-bind="$attrs"
    v-on="$listeners"
    ref="autocomplete"
  />
</template>

<script>
import DsfrAutocomplete from "@/components/DsfrAutocomplete"

export default {
  name: "CityField",
  components: { DsfrAutocomplete },
  props: {
    location: {
      default: () => ({}),
    },
    inseeCode: {
      required: false,
    },
  },
  data() {
    return {
      cityAutocompleteChoice: null,
      communes: [],
      loadingCommunes: false,
      search: null,
      disableSearchWatcher: false,
    }
  },
  computed: {
    noDataText() {
      if (!this.search || this.search.length < 3) {
        return "Veuillez rentrer au moins trois caractères"
      }
      return this.loadingCommunes ? "Chargement en cours..." : "Pas de résultats"
    },
  },
  methods: {
    queryCommunes(val) {
      if (val?.length < 3) return
      this.loadingCommunes = true
      const queryUrl = "https://api-adresse.data.gouv.fr/search/?q=" + val + "&type=municipality&autocomplete=1"
      return fetch(queryUrl)
        .then((response) => response.json())
        .then((response) => {
          const communes = response.features
          this.communes = communes.map((commune) => {
            return { text: `${commune.properties.label} (${commune.properties.context})`, value: commune.properties }
          })
          this.loadingCommunes = false
        })
        .catch((error) => {
          console.log(error)
        })
    },
    populateCityAutocomplete() {
      if (this.location.city && this.location.cityInseeCode && this.location.postalCode && this.location.department) {
        const initialCityAutocomplete = {
          text: this.location.city,
          value: {
            label: this.location.city,
            citycode: this.location.cityInseeCode,
            postcode: this.location.postalCode,
            context: this.location.department,
          },
        }
        this.communes.push(initialCityAutocomplete)
        this.cityAutocompleteChoice = initialCityAutocomplete.value
      } else if (this.inseeCode && !this.cityAutocompleteChoice) {
        return this.fillFromInseeCode(this.inseeCode)
      }
    },
    fillFromInseeCode(inseeCode) {
      this.loadingCommunes = true
      this.disableSearchWatcher = true
      const queryUrl = `https://api-adresse.data.gouv.fr/search/?q=${inseeCode}&type=municipality&citycode=${inseeCode}`
      return fetch(queryUrl)
        .then((response) => response.json())
        .then((response) => {
          const communes = response.features.map((commune) => {
            return { text: `${commune.properties.label} (${commune.properties.context})`, value: commune.properties }
          })
          const communeLabel = communes.length > 0 ? communes[0].text : `Code INSEE : ${this.inseeCode}`
          const initialCityAutocomplete = {
            text: communeLabel,
            value: {
              label: communeLabel,
              citycode: this.inseeCode,
              postcode: null,
              context: null,
            },
          }
          this.communes.push(initialCityAutocomplete)
          this.cityAutocompleteChoice = initialCityAutocomplete.value
        })
        .then(this.$nextTick)
        .catch((error) => {
          console.log(error)
        })
        .finally(() => {
          this.disableSearchWatcher = false
          this.loadingCommunes = false
        })
    },
  },
  beforeMount() {
    if (this.location.city || this.inseeCode) {
      return this.populateCityAutocomplete()
    }
  },
  watch: {
    search(val) {
      return val && !this.disableSearchWatcher && val !== this.location.city && this.queryCommunes(val)
    },
    cityAutocompleteChoice(val) {
      if (val?.label && val?.context) {
        const jsonRepresentation = {
          city: val.label,
          cityInseeCode: val.citycode,
          postalCode: val.postcode,
          department: val.context.split(",")[0],
        }
        const inseeCode = val.citycode
        this.$emit("locationUpdate", jsonRepresentation)
        this.$emit("update:inseeCode", inseeCode)
      }

      this.search = this.location.city
    },
    inseeCode() {
      if (!this.location || !this.location.city) this.populateCityAutocomplete()
    },
  },
}
</script>
