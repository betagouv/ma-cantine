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

/* Clean dataset */
const regionsSortedByName = regions.sort((regionBefore, regionAfter) => {
  const cleanedRegionBeforeName = stringsService.removeSpecialChars(regionBefore.nom)
  const cleanedRegionAfterName = stringsService.removeSpecialChars(regionAfter.nom)
  if (cleanedRegionBeforeName < cleanedRegionAfterName) return -1
  else if (cleanedRegionBeforeName > cleanedRegionAfterName) return 1
  else return 0
})

/* Exported functions */
const getYearsOptions = () => {
  const startYear = 2021
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
    option.value = { value: option.value, label: option.label }
    return option
  })

  const managementTypeOptions = cantines.managementType.map((option) => {
    option.name = "managementType"
    option.value = { value: option.value, label: option.label }
    return option
  })

  const productionTypeOptions = cantines.productionType.map((option) => {
    option.hint = ""
    option.value = { value: option.value, label: option.label }
    return option
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
    const label = `${sector.categoryName} - ${sector.name}`
    const option = {
      label,
      value: { value: sector.id, label },
    }
    sectorsOptions.push(option)
  })
  return sectorsOptions
}

const getCitiesOptionsFromSearch = (search) => {
  const filteredCities = communes.filter((city) => stringsService.checkIfStartsWith(city.nom, search))
  const firstTenCities = filteredCities.slice(0, 9)
  const options = firstTenCities.map((city) => {
    const label = `${city.nom} (${city.codeDepartement})`
    return {
      label,
      value: { value: city.code, label },
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
      value: { value: pat.code, label: pat.nom },
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
      value: { value: epci.code, label: epci.nom },
    }
  })
  return options
}

const getDepartmentsOptionsFromSearch = (search) => {
  const departmentsOptions = search
    ? departements.filter(
        (department) =>
          stringsService.checkIfContains(department.nom, search) ||
          stringsService.checkIfStartsWith(department.code, search)
      )
    : departements
  return departmentsOptions.map((department) => {
    return {
      label: `${department.nom} (${department.code})`,
      value: { value: department.code, label: department.nom },
    }
  })
}

const getRegionsOptionsFromSearch = (search) => {
  const regionsOptions = search
    ? regionsSortedByName.filter((region) => stringsService.checkIfContains(region.nom, search))
    : regionsSortedByName
  return regionsOptions.map((region) => {
    return { label: region.nom, value: { value: region.code, label: region.nom } }
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
