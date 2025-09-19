<script setup>
import { computedAsync } from "@vueuse/core"
import { useRoute } from "vue-router"
import urlService from "@/services/urls.js"
import canteenService from "@/services/canteens.js"
import sectorService from "@/services/sectors.js"
import cantines from "@/data/cantines.json"

const route = useRoute()
const sectors = computedAsync(async () => {
  return await sectorService.getSectors()
}, [])
const ministries = computedAsync(async () => {
  return await sectorService.getMinistries()
}, [])

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
  const filteredInfos = []
  const fieldsName = [
    "name",
    "siret",
    "sirenUniteLegale",
    "managementType",
    "economicModel",
    "productionType",
    "dailyMealCount",
    "yearlyMealCount",
    "sectors",
    "lineMinistry",
    "city",
    "postalCode",
    "centralProducerSiret",
    "satelliteCanteensCount",
  ]
  fieldsName.forEach((name) => {
    filteredInfos.push({ name: name, value: canteenInfos[name] })
  })
  return filteredInfos
}

const filterNotEditableInfos = (canteenInfos) => {
  const filteredInfos = []
  const fieldsName = ["regionLib", "departmentLib", "epciLib", "patLibList", "city", "cityInseeCode", "postalCode"]
  fieldsName.forEach((name) => {
    filteredInfos.push({ name: name, value: canteenInfos[name] })
  })
  return filteredInfos
}

const getPrettyName = (name) => {
  if (typeof cantines[name] === "string") return cantines[name]
  if (typeof cantines[name] === "object") return cantines[`${name}Name`] // TODO : refactor json file to group name and options props
}

const getPrettyValue = (info) => {
  const { name, value } = info
  let prettyValue = null
  switch (true) {
    case name === "lineMinistry": {
      prettyValue = getMinistrieName(value)
      break
    }
    case name === "sectors": {
      prettyValue = getSectorsNames(value)
      break
    }
    case typeof cantines[name] === "object": {
      const index = cantines[name].findIndex((option) => option.value === value)
      if (index >= 0) prettyValue = cantines[name][index].label
      break
    }
    case value && value.length === 0: {
      prettyValue = ""
      break
    }
    default: {
      prettyValue = value
    }
  }
  return prettyValue || "Non renseigné"
}

const getSectorsNames = (canteenSectorsIds) => {
  const filteredSectors = sectors.value.filter((sector) => canteenSectorsIds.includes(sector.id))
  const sectorsName = filteredSectors.map((filter) => filter.name)
  return sectorsName.join(" ; ")
}

const getMinistrieName = (canteenMinistrySlug) => {
  const index = ministries.value.findIndex((ministry) => ministry.value === canteenMinistrySlug)
  return index >= 0 ? ministries.value[index].name : "Erreur sur le champ, contacter le support"
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
          <ul class="ma-cantine--flex-grow">
            <li v-for="info in canteenInfos.editable" :key="info.name">
              <p class="fr-mb-0">
                <span class="fr-text--bold">{{ getPrettyName(info.name) }} :</span>
                {{ getPrettyValue(info) }}
              </p>
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
          <ul class="ma-cantine--flex-grow">
            <li v-for="info in canteenInfos.notEditable" :key="info.name">
              <p class="fr-mb-0">
                <span class="fr-text--bold">{{ getPrettyName(info.name) }} :</span>
                {{ getPrettyValue(info) }}
              </p>
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
