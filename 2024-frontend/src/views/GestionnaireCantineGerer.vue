<script setup>
import { computedAsync } from "@vueuse/core"
import { useRoute } from "vue-router"
import urlService from "@/services/urls.js"
import canteenService from "@/services/canteens.js"
import sectorService from "@/services/sectors.js"
import cantines from "@/data/cantines.json"
import AppLinkRouter from "@/components/AppLinkRouter.vue"

/* Router */
const route = useRoute()

/* Canteen informations */
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
  // Required field for all canteen
  const fieldsName = ["name"]
  // SIRET is the default
  if (canteenInfos.sirenUniteLegale) fieldsName.push("sirenUniteLegale", "postalCode", "city")
  else fieldsName.push("siret")
  // Next required field for all canteen
  fieldsName.push("economicModel", "managementType", "productionType", "dailyMealCount", "yearlyMealCount")
  // Required fields for canteen with site
  if (canteenInfos.productionType !== "central") fieldsName.push("sectors")
  if (canteenInfos.lineMinistry) fieldsName.push("lineMinistry")
  // Required field for satellite
  if (canteenInfos.isSatellite) fieldsName.push("centralProducerSiret")
  // Required field for central
  if (canteenInfos.isCentralCuisine) fieldsName.push("satelliteCanteensCount")
  fieldsName.forEach((name) => {
    filteredInfos.push({ name: name, value: canteenInfos[name] })
  })
  return filteredInfos
}

const filterNotEditableInfos = (canteenInfos) => {
  const filteredInfos = []
  // Required field for all canteen
  const fieldsName = ["regionLib", "departmentLib", "epciLib", "patLibList"]
  // Required field for SIRET canteen
  if (canteenInfos.siret) fieldsName.push("city", "postalCode")
  // Next required field for all canteen
  fieldsName.push("cityInseeCode")
  fieldsName.forEach((name) => {
    filteredInfos.push({ name: name, value: canteenInfos[name] })
  })
  return filteredInfos
}

/* Prettify */
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

/* Sectors and ministry */
const sectors = computedAsync(async () => {
  return await sectorService.getSectors()
}, [])
const ministries = computedAsync(async () => {
  return await sectorService.getMinistries()
}, [])

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
    </div>
    <div class="fr-grid-row fr-grid-row--gutters">
      <div class="fr-col-12 fr-col-md-6">
        <div class="fr-card fr-p-2w fr-p-md-6w">
          <h2 class="fr-h6">Informations renseignées</h2>
          <p>Informations renseignées lors de la création de votre établissement.</p>
          <ul class="ma-cantine--flex-grow">
            <li v-for="info in canteenInfos.editable" :key="info.name">
              <p class="fr-mb-0">
                <span class="fr-text--bold">{{ getPrettyName(info.name) }} :</span>
                {{ getPrettyValue(info) }}
              </p>
            </li>
          </ul>
          <div class="fr-grid-row fr-grid-row--center fr-mt-2w">
            <router-link
              class="ma-cantine--unstyled-link"
              :to="{
                name: 'GestionnaireCantineModifier',
                params: { canteenUrlComponent: route.params.canteenUrlComponent },
              }"
            >
              <DsfrButton secondary label="Modifier" />
            </router-link>
          </div>
        </div>
      </div>
      <div class="fr-col-12 fr-col-md-6">
        <div class="fr-card fr-p-2w fr-p-md-6w">
          <h2 class="fr-h6">Informations générées</h2>
          <p>
            À partir des informations renseignées lors de la création de votre établissement, nous avons pu en générer
            de nouvelles en croisant vos données avec nos référentiels.
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
  <section class="fr-container fr-background-alt--red-marianne fr-p-3w fr-mt-2w fr-grid-row fr-grid-row--center">
    <div class="fr-col-12 fr-col-lg-7 fr-background-default--grey fr-p-2w fr-p-md-7w">
      <h2 class="fr-h5 fr-text-default--error">
        <span class="mdi mdi-delete"></span>
        Supprimer cet établissement
      </h2>
      <p class="fr-mb-0">
        Vous ne souhaitez plus faire apparaître cet établissement sur la plateforme ma-cantine, vous pouvez le supprimer
        <AppLinkRouter :to="{ name: 'CanteenDeletion' }" title="en cliquant ici" />
      </p>
    </div>
  </section>
</template>
