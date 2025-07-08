import canteenCharacteristics from "@/constants/canteen-establishment-form-options.js"
import sectorsService from "@/services/sectors"

const getYearsOptions = () => {
  const startYear = 2020
  const endYear = new Date().getFullYear()
  const yearsOptions = []
  for (let i = startYear; i < endYear; i++) {
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
    option.name = "economicModel"
    return option
  })

  const managementTypeOptions = canteenCharacteristics.managementType.map((option) => {
    option.name = "managementType"
    return option
  })

  const productionTypeOptions = canteenCharacteristics.productionType.map((option) => {
    option.id = option.value
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
    const option = {
      id: sector.id,
      label: `${sector.categoryName} - ${sector.name}`,
      value: sector.id,
    }
    sectorsOptions.push(option)
  })
  return sectorsOptions
}

export { getYearsOptions, getCharacteristicsOptions, getSectorsOptions }
