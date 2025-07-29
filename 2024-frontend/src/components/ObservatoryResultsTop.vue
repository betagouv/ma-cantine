<script setup>
import { ref, computed, watch } from "vue"
import { useStoreFilters } from "@/stores/filters"

/* Props */
const props = defineProps(["canteensCount", "teledeclarationsCount"])

/* Filters */
const storeFilters = useStoreFilters()
const filtersParams = storeFilters.getAll()

/* Canteen */
const nowYear = new Date().getFullYear()
const filterYear = computed(() => storeFilters.get("year"))
const canteenDescription = computed(() => {
  const endSentend =
    filterYear.value >= nowYear ? "à ce jour" : `à la fin de la campagne de télédéclaration ${filterYear.value}`
  const startSentend = props.canteensCount <= 1 ? "Nombre de cantine créée" : "Nombre de cantines créées"
  return `${startSentend} ${endSentend}`
})

/* Teledeclaration */
const percent = computed(() => Math.round(props.teledeclarationsCount / props.canteensCount))
const teledeclarationTitle = computed(() =>
  props.teledeclarationsCount <= 1 ? "site télédéclaré" : "sites télédéclarés"
)

/* Tile */
const titleImgSrc = "/static/images/picto-dsfr/school.svg"
const tileQuery = ref({})

watch(filtersParams, () => {
  const params = {}
  if (filtersParams.sectors.length > 0) params.secteurs = filtersParams.sectors.map((item) => item.value)
  if (filtersParams.cities.length > 0) params.commune = filtersParams.cities.map((item) => item.value)
  if (filtersParams.departments.length > 0) params.departement = filtersParams.departments.map((item) => item.value)
  if (filtersParams.regions.length > 0) params.region = filtersParams.regions.map((item) => item.value)
  if (filtersParams.managementType.length > 0) {
    let isDirect = false
    let isConceded = false
    filtersParams.managementType.forEach((item) => {
      if (item.value === "direct") isDirect = true
      if (item.value === "conceded") isConceded = true
    })
    if (isDirect && !isConceded) params.modeDeGestion = "direct"
    if (isConceded && !isDirect) params.modeDeGestion = "conceded"
    // if (isDirect && isConceded) no filter to send
  }
  if (filtersParams.productionType.length > 0) {
    let isCentral = false
    let isSite = false
    filtersParams.productionType.forEach((item) => {
      if (item.value === "central" || item.value === "central_serving") isCentral = true
      if (item.value === "site" || item.value === "site_cooked_elsewhere") isSite = true
    })
    if (isCentral && !isSite) params.typeEtablissement = ["central,central_serving"]
    if (isSite && !isCentral) params.typeEtablissement = ["site,site_cooked_elsewhere"]
    // if (isSite && isCentral) no filter to send
  }

  tileQuery.value = params
})
</script>
<template>
  <ul class="observatory-results-top ma-cantine--unstyled-list fr-grid-row fr-grid-row--gutters">
    <li class="fr-col-12 fr-col-lg-4">
      <div class="observatory-results-top__card fr-card fr-p-4w">
        <p class="fr-h5 fr-mb-1w">{{ canteensCount }}</p>
        <p class="fr-mb-2w">Nombre de cantines</p>
        <p class="fr-text--xs fr-mb-0">{{ canteenDescription }}</p>
      </div>
    </li>
    <li class="fr-col-12 fr-col-lg-4">
      <div class="observatory-results-top__card fr-card fr-p-4w">
        <p class="fr-h5 fr-mb-1w">{{ teledeclarationsCount }}</p>
        <p class="fr-mb-2w">{{ teledeclarationTitle }}</p>
        <p class="fr-text--xs fr-mb-0">Soit un pourcentage de {{ percent }}%</p>
      </div>
    </li>
    <li class="fr-col-12 fr-col-lg-4">
      <DsfrTile
        :imgSrc="titleImgSrc"
        :horizontal="true"
        title="Voir les cantines"
        description="Retrouvez les cantines correspondantes à votre recherche"
        details="Aller à la page “Trouver une cantine”"
        :to="{ name: 'CanteensHome', query: tileQuery }"
      />
    </li>
  </ul>
</template>

<style lang="scss">
.observatory-results-top {
  &__card {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
  }
}
</style>
