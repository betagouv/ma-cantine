<script setup>
import { computedAsync } from "@vueuse/core"
import { useRoute } from "vue-router"
import urlService from "@/services/urls.js"
import canteenService from "@/services/canteens.js"

const route = useRoute()

const canteenInfos = computedAsync(
  async () => {
    const id = urlService.getCanteenId(route.params.canteenUrlComponent)
    const infos = await canteenService.fetchCanteen(id)
    const editableInfos = filterEditableInfos(infos)
    const notEditableInfos = filterNotEditableInfos(infos)
    return { editable: editableInfos, notEditable: notEditableInfos }
  },
  { editable: [], notEditable: [] }
)

const filterEditableInfos = (canteenInfos) => {
  const editableInfos = []
  const editableInfosName = [
    "managementType",
    "economicModel",
    "productionType",
    "siret",
    "sirenUniteLegale",
    "name",
    "dailyMealCount",
    "yearlyMealCount",
    "sectors",
    "lineMinistry",
    "city",
    "postalCode",
    "centralProducerSiret",
    "satelliteCanteensCount",
  ]
  const canteenInfosKeys = Object.keys(canteenInfos)
  const filteredEditableKeys = canteenInfosKeys.filter((key) => editableInfosName.includes(key))
  filteredEditableKeys.forEach((key) => {
    editableInfos.push({ name: key, value: canteenInfos[key] })
  })
  return editableInfos
}

const filterNotEditableInfos = (canteenInfos) => {
  const notEditableInfos = []
  const notEditableInfosName = [
    "epciLib",
    "patLibList",
    "departmentLib",
    "regionLib",
    "city",
    "postalCode",
    "cityInseeCode",
  ]
  const canteenInfosKeys = Object.keys(canteenInfos)
  const filteredNotditableKeys = canteenInfosKeys.filter((key) => notEditableInfosName.includes(key))
  filteredNotditableKeys.forEach((key) => {
    notEditableInfos.push({ name: key, value: canteenInfos[key] })
  })
  return notEditableInfos
}
</script>

<template>
  <section>
    <div class="fr-col-12 fr-col-md-8 fr-mb-3w">
      <h1>{{ route.meta.title }}</h1>
      <p>Retrouver toutes les informations de votre établissement.</p>
    </div>
    <div class="fr-grid-row fr-grid-row--gutters">
      <div class="fr-col-12 fr-col-md-6">
        <div class="fr-card fr-p-2w fr-p-md-6w">
          <h2 class="fr-h6">Informations renseignées</h2>
          <ul>
            <li v-for="info in canteenInfos.editable" :key="info.name">
              <p class="fr-mb-0">{{ info.name }} : {{ info.value }}</p>
            </li>
          </ul>
          <DsfrButton secondary label="Modifier" class="fr-mb-0 fr-mt-2w" />
        </div>
      </div>
      <div class="fr-col-12 fr-col-md-6">
        <div class="fr-card fr-p-2w fr-p-md-6w">
          <h2 class="fr-h6">Informations générées</h2>
          <p>
            À partir des informations renseignées lors de la création de votre établissement, nous avons pu en générer
            de nouvelles en croisant les données avec des référentiels.
          </p>
          <ul>
            <li v-for="info in canteenInfos.notEditable" :key="info.name">
              <p class="fr-mb-0">{{ info.name }} : {{ info.value }}</p>
            </li>
          </ul>
          <DsfrHighlight
            class="fr-ml-0 fr-mb-0 fr-mt-2w ma-cantine--no-mb-p"
            text="Ces informations ne sont pas modifiables, si vous remarquez une erreur merci de nous contacter."
          />
        </div>
      </div>
    </div>
  </section>
</template>
