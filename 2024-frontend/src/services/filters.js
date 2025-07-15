import canteenCharacteristics from "@/constants/canteen-establishment-form-options.js"
import sectorsService from "@/services/sectors"
import stringsService from "@/services/strings"
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
  const economicModelOptions = canteenCharacteristics.economicModel.map((option) => {
    option.hint = ""
    option.id = option.value
    return option
  })

  const managementTypeOptions = canteenCharacteristics.managementType.map((option) => {
    option.name = "managementType"
    option.id = option.value
    return option
  })

  const productionTypeOptions = [
    { label: "Site", value: "site", id: "site" },
    { label: "Satellite", value: "site_cooked_elsewhere", id: "site_cooked_elsewhere" },
    { label: "Centrale", value: "central", id: "central" },
    { label: "Centrale et site", value: "central_serving", id: "central_serving" },
  ]

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
  let departmentsList = departements
  if (search) {
    departmentsList = departmentsList.filter((department) => stringsService.checkIfStartsWith(department.nom, search))
  }
  return departmentsList.map((department) => {
    return { label: `${department.nom} (${department.code})`, value: department.code, id: department.code }
  })
}

const getRegionsOptionsFromSearch = (search) => {
  let regionList = regionsSortedByName
  if (search) {
    regionList = regionList.filter((region) => stringsService.checkIfStartsWith(region.nom, search))
  }
  return regionList.map((region) => {
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
