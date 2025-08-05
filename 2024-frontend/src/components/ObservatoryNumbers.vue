<script setup>
import { ref, computed, watch } from "vue"
import { useStoreFilters } from "@/stores/filters"

/* Props */
const props = defineProps(["canteensCount", "canteensDescription", "teledeclarationsCount"])

/* Filters */
const storeFilters = useStoreFilters()
const filtersParams = storeFilters.getAllParams()

/* Canteen */
const canteenTitle = computed(() => {
  return props.canteensCount <= 1 ? "Cantine inscrite sur la plateforme" : "Cantines inscrites sur la plateforme"
})

/* Teledeclaration */
const teledeclarationTitle = computed(() => (props.teledeclarationsCount <= 1 ? "Télédéclaration" : "Télédéclarations"))
const hasTeledeclarationCount = computed(() => props.teledeclarationsCount !== null)

/* Tile */
const tileImgSrc = "/static/images/picto-dsfr/school.svg"
const tileQuery = ref({})

const transformFiltersToQuery = () => {
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
  return params
}

watch(filtersParams, () => {
  tileQuery.value = transformFiltersToQuery()
})
</script>
<template>
  <ul class="observatory-numbers ma-cantine--unstyled-list fr-grid-row fr-grid-row--gutters">
    <li
      class="fr-col-12"
      :class="{
        'fr-col-lg-4': hasTeledeclarationCount,
        'fr-col-lg-8': !hasTeledeclarationCount,
      }"
    >
      <div class="observatory-numbers__card fr-card fr-p-4w">
        <p class="fr-h5 fr-mb-1w">{{ canteensCount }}</p>
        <p class="fr-mb-2w">{{ canteenTitle }}</p>
        <p class="fr-text--xs fr-mb-0">{{ canteensDescription }}</p>
      </div>
    </li>
    <li v-if="hasTeledeclarationCount" class="fr-col-12 fr-col-lg-4">
      <div class="observatory-numbers__card fr-card fr-p-4w">
        <p class="fr-h5 fr-mb-1w">{{ teledeclarationsCount }}</p>
        <p class="fr-mb-2w">{{ teledeclarationTitle }}</p>
        <p class="fr-text--xs fr-mb-0"></p>
      </div>
    </li>
    <li class="fr-col-12 fr-col-lg-4">
      <DsfrTile
        :imgSrc="tileImgSrc"
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
.observatory-numbers {
  &__card {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
  }
}
</style>
