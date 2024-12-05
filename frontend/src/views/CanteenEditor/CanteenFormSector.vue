<template>
  <v-row>
    <v-col cols="12" class="mt-4">
      <v-divider aria-hidden="true" role="presentation"></v-divider>
    </v-col>
    <v-col cols="12" sm="6" md="4">
      <DsfrNativeSelect
        label="Catégorie de secteur"
        labelClasses="body-2 mb-2"
        :items="sectorCategories"
        v-model="sectorCategory"
      />
    </v-col>
    <v-col cols="12" md="6">
      <div>
        <DsfrNativeSelect
          label="Secteurs d'activité"
          labelClasses="body-2 mb-2"
          :items="filteredSectors"
          v-model="chosenSector"
          item-text="name"
          item-value="id"
          no-data-text="Veuillez séléctionner la catégorie de secteur"
          :rules="canteenSectors && canteenSectors.length ? [] : [validators.required]"
        />
        <DsfrTagGroup :tags="sectorTags" :closeable="true" @closeTag="(tag) => removeSector(tag.id)" />
      </div>
    </v-col>
    <v-col v-if="showMinistryField" cols="12" md="10">
      <DsfrNativeSelect
        label="Administration générale de tutelle (ministère ou ATE)"
        hint="Hors fonction publique territoriale et hospitalière"
        labelClasses="body-2 mb-2"
        :items="ministries"
        v-model="lineMinistry"
        :rules="[validators.required]"
        placeholder="Sélectionnez l'administration générale de tutelle (ministère ou ATE) hors fonction publique territoriale et hospitalière."
      />
    </v-col>
  </v-row>
</template>

<script>
import { sectorsSelectList } from "@/utils"
import validators from "@/validators"
import Constants from "@/constants"
import DsfrTagGroup from "@/components/DsfrTagGroup"
import DsfrNativeSelect from "@/components/DsfrNativeSelect"

// TODO renvoyer l'info au changement au parent
// Afficher le champ tutelle en fonction du sectur sélectionné
// Remplacte le this.canteenSectors par canteenSectors

/* Comportemnt du composant :
- à la création d'une cantine il est vide
- à la modification d'une cantine il est pré-rempli
- on sélectionne une secteur
- à partir de ce secteur on affiche l'activité
- si l'activité le demande on affiche l'établissement de tutelle
- on renvoit bien l'info au parent dès qu'il y a un changement
*/

export default {
  name: "CanteenFormSector",
  props: {
    canteenSectors: {
      type: Array,
      default: () => [],
    },
  },
  components: {
    DsfrNativeSelect,
    DsfrTagGroup,
  },
  data() {
    return {
      sectorCategory: null,
      chosenSector: null,
      ministries: this.$store.state.lineMinistries,
      lineMinistry: false,
    }
  },

  computed: {
    validators() {
      return validators
    },
    sectors() {
      return this.$store.state.sectors
    },
    sectorCategories() {
      const displayValueMap = Constants.SectorCategoryTranslations
      const categoriesInUse = this.sectors.map((s) => s.category)
      const uniqueCategories = categoriesInUse.filter((c, idx) => categoriesInUse.indexOf(c) === idx)
      const categories = uniqueCategories.map((c) => ({ value: c, text: displayValueMap[c] }))
      categories.sort((a, b) => {
        if (a.value === "autres" && b.value === "inconnu") return 0
        else if (a.value === "autres") return 1
        else if (a.value === "inconnu") return 1
        else if (b.value === "autres") return -1
        else if (b.value === "inconnu") return -1
        return a.text.localeCompare(b.text)
      })
      return categories
    },
    filteredSectors() {
      if (!this.sectorCategory) return []
      return sectorsSelectList(this.sectors, this.sectorCategory).filter((s) => !s.header)
    },
    sectorTags() {
      return this.canteenSectors.map((sectorId) => ({
        text: this.sectorName(sectorId),
        id: sectorId,
      }))
    },
    showMinistryField() {
      const concernedSectors = this.sectors.filter((x) => !!x.hasLineMinistry).map((x) => x.id)
      if (concernedSectors.length === 0) return false
      return this.canteenSectors?.some((x) => concernedSectors.indexOf(parseInt(x, 10)) > -1)
    },
  },
  methods: {
    addSector(id) {
      id = +id
      if (!id || id < 0) return
      if (!this.canteenSectors) this.canteenSectors = []
      if (this.canteenSectors.indexOf(id) === -1) this.canteenSectors.push(id)
      this.$nextTick(() => {
        this.chosenSector = null
      })
    },
    removeSector(id) {
      this.canteenSectors?.splice(this.canteenSectors?.indexOf(id), 1)
    },
    sectorName(id) {
      id = parseInt(id, 10) || id
      return this.sectors.find((s) => s.id === id)?.name || id
    },
  },
  watch: {
    chosenSector(newValue) {
      this.addSector(newValue)
    },
  },
}
</script>
