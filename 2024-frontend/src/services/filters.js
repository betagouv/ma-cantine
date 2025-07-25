/* Services */
import sectorsService from "@/services/sectors"
import stringsService from "@/services/strings"

/* Dataset */
import cantines from "@/data/cantines.json"
import communes from "@/data/communes.json"
import pats from "@/data/pats.json"
import epcis from "@/data/epcis.json"
import departements from "@/data/departements.json"
import regions from "@/data/regions.json"
const regionsSortedByName = regions.sort((regionBefore, regionAfter) => {
  if (regionBefore.nom < regionAfter.nom) return -1
  else if (regionBefore.nom > regionAfter.nom) return 1
  else return 0
})

/* Exported functions */
const getYearsOptions = () => {
  const startYear = 2020
  const endYear = new Date().getFullYear()
  const yearsOptions = []
  for (let i = endYear; i >= startYear; i--) {
    const yearInfo = {
      name: "year",
      label: `Année ${i} (télédéclarée en ${i + 1})`,
      value: i,
    }
    yearsOptions.push(yearInfo)
  }
  return yearsOptions
}

const getCharacteristicsOptions = () => {
  const economicModelOptions = cantines.economicModel.map((option) => {
    option.hint = ""
    option.id = option.value
    return option
  })

  const managementTypeOptions = cantines.managementType.map((option) => {
    option.name = "managementType"
    option.id = option.value
    return option
  })

  const productionTypeOptions = cantines.productionType.map((option) => {
    return { label: option.label, value: option.value, id: option.value }
  })

  const characteristicsOptions = {
    economicModel: economicModelOptions,
    managementType: managementTypeOptions,
    productionType: productionTypeOptions,
  }
  return characteristicsOptions
}

const getSectorsOptions = async () => {
  const sectorsBackend = await sectorsService.getSectors()
  const sectorsOptions = []
  sectorsBackend.forEach((sector) => {
    const option = {
      id: sector.id,
      label: `${sector.categoryName} - ${sector.name}`,
      value: sector.id,
    }
    sectorsOptions.push(option)
  })
  return sectorsOptions
}

const getCitiesOptionsFromSearch = (search) => {
  const filteredCities = communes.filter((city) => stringsService.checkIfStartsWith(city.nom, search))
  const firstTenCities = filteredCities.slice(0, 9)
  const options = firstTenCities.map((city) => {
    return {
      label: `${city.nom} (${city.codeDepartement})`,
      value: city.code,
      id: city.code,
    }
  })
  return options
}

const getPATOptionsFromSearch = (search) => {
  const filteredPats = pats.filter((pat) => stringsService.checkIfContains(pat.nom, search))
  const firstTenPAT = filteredPats.slice(0, 9)
  const options = firstTenPAT.map((pat) => {
    return {
      label: pat.nom,
      value: pat.code,
      id: pat.code,
    }
  })
  return options
}

const getEPCIOptionsFromSearch = (search) => {
  const filteredEPCI = epcis.filter((epci) => stringsService.checkIfContains(epci.nom, search))
  const firstTenEPCI = filteredEPCI.slice(0, 9)
  const options = firstTenEPCI.map((epci) => {
    return {
      label: epci.nom,
      value: epci.code,
      id: epci.code,
    }
  })
  return options
}

const getDepartmentsOptionsFromSearch = (search) => {
  const departmentsOptions = search
    ? departements.filter((department) => stringsService.checkIfStartsWith(department.nom, search))
    : departements
  return departmentsOptions.map((department) => {
    return { label: `${department.nom} (${department.code})`, value: department.code, id: department.code }
  })
}

const getRegionsOptionsFromSearch = (search) => {
  const regionsOptions = search
    ? regionsSortedByName.filter((region) => stringsService.checkIfStartsWith(region.nom, search))
    : regionsSortedByName
  return regionsOptions.map((region) => {
    return { label: region.nom, value: region.code, id: region.code }
  })
}

export {
  getYearsOptions,
  getCharacteristicsOptions,
  getSectorsOptions,
  getCitiesOptionsFromSearch,
  getPATOptionsFromSearch,
  getEPCIOptionsFromSearch,
  getDepartmentsOptionsFromSearch,
  getRegionsOptionsFromSearch,
}
