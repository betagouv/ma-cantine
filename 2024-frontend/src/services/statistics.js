import { verifyResponse } from "@/services/api.js"

const formatMultipleValues = (name, list) => {
  let string = ""
  list.forEach((item) => {
    string += `&${name}=${item.value}`
  })
  return string
}

const filtersToQuery = (filters) => {
  let query = "?"
  query += `year=${filters.year}`
  if (filters.sectors.length > 0) query += formatMultipleValues("sectors", filters.sectors)
  if (filters.regions.length > 0) query += formatMultipleValues("region", filters.regions)
  if (filters.departments.length >= 0) query += formatMultipleValues("department", filters.departments)
  if (filters.epcis.length >= 0) query += formatMultipleValues("epci", filters.epcis)
  if (filters.pats.length >= 0) query += formatMultipleValues("pat", filters.pats)
  if (filters.cities.length >= 0) query += formatMultipleValues("city", filters.cities)
  if (filters.economicModel.length >= 0) query += formatMultipleValues("economic_model", filters.economicModel)
  if (filters.managementType.length >= 0) query += formatMultipleValues("management_type", filters.managementType)
  if (filters.productionType.length >= 0) query += formatMultipleValues("production_type", filters.productionType)
  return query
}

const getStatistics = (filters) => {
  const query = filtersToQuery(filters)
  return fetch(`/api/v1/canteenStatistics/${query}`, { method: "GET" })
    .then(verifyResponse)
    .catch((e) => {
      console.error("ERROR /canteenStatistics/ :", e)
    })
}

export default { getStatistics }
