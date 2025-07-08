import canteenCharacteristics from "@/constants/canteen-establishment-form-options.js"

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
export { getYearsOptions, getCharacteristicsOptions }
