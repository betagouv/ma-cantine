<template>
  <DsfrAutocomplete
    hide-details="auto"
    :loading="loadingCommunes"
    :items="communes"
    :search-input.sync="search"
    auto-select-first
    cache-items
    v-model="cityAutocompleteChoice"
    no-data-text="Pas de résultats. Veuillez renseigner votre ville"
    v-bind="$attrs"
    v-on="$listeners"
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
    value: {
      required: false,
    },
  },
  data() {
    return {
      cityAutocompleteChoice: null,
      communes: [],
      loadingCommunes: false,
      search: null,
    }
  },
  methods: {
    queryCommunes(val) {
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
      }
    },
  },
  beforeMount() {
    if (this.location.city) {
      this.populateCityAutocomplete()
    }
  },
  watch: {
    search(val) {
      return val && val !== this.location.city && this.queryCommunes(val)
    },
    cityAutocompleteChoice(val) {
      if (val?.label) {
        const jsonRepresentation = {
          city: val.label,
          cityInseeCode: val.citycode,
          postalCode: val.postcode,
          department: val.context.split(",")[0],
        }
        const inseeCode = val.citycode
        this.$emit("locationUpdate", jsonRepresentation)
        this.$emit("input", inseeCode)
      }

      this.search = this.location.city
    },
  },
}
</script>
