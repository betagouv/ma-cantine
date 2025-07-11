import canteenCharacteristics from "@/constants/canteen-establishment-form-options.js"
import sectorsService from "@/services/sectors"
import communes from "@/data/communes.json"
import pats from "@/data/pats.json"

const getYearsOptions = () => {
  const startYear = 2020
  const endYear = new Date().getFullYear()
  const yearsOptions = []
  for (let i = startYear; i <= endYear; i++) {
    const yearInfo = {
      name: "year",
      label: i,
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

const cleanString = (string) => {
  // TODO à améliorer et compléter
  return string
    .toLowerCase()
    .replaceAll("-", " ")
    .replaceAll("'", " ")
}

const getCitiesOptionsFromSearch = (search) => {
  const cleanSearch = cleanString(search)
  const filteredCities = communes.filter((city) => {
    const cleanName = cleanString(city.nom)
    return cleanName.startsWith(cleanSearch)
  })
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
  const cleanSearch = cleanString(search)
  const filteredPats = pats.filter((project) => {
    const cleanName = cleanString(project.nom)
    return cleanName.indexOf(cleanSearch) >= 0
  })
  const firstTenPAT = filteredPats.slice(0, 9)
  const options = firstTenPAT.map((project) => {
    return {
      label: project.nom,
      value: project.code,
      id: project.code,
    }
  })
  return options
}

export {
  getYearsOptions,
  getCharacteristicsOptions,
  getSectorsOptions,
  getCitiesOptionsFromSearch,
  getPATOptionsFromSearch,
}
