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

export { getYearsOptions }
